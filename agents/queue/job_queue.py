#!/usr/bin/env python3
"""
Job Queue System สำหรับ Novel Writing Automation
จัดการงานที่ค้าง, retry, และ auto-resume
"""

import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Any
from enum import Enum
from dataclasses import dataclass, asdict
import threading
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("JobQueue")


class JobStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    RATE_LIMITED = "rate_limited"
    PAUSED = "paused"


class JobType(Enum):
    WRITE_CHAPTER = "write_chapter"
    CREATE_CHARACTER = "create_character"
    CREATE_PLOT = "create_plot"
    QC_CHECK = "qc_check"
    POLISH_TEXT = "polish_text"


@dataclass
class Job:
    """แต่ละงานในคิว"""
    id: str
    job_type: str
    story_id: str
    chapter_num: Optional[int]
    input_data: Dict[str, Any]
    status: str = JobStatus.PENDING.value
    retry_count: int = 0
    max_retries: int = 3
    created_at: str = ""
    updated_at: str = ""
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error_message: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    priority: int = 5  # 1 = highest, 10 = lowest

    def __post_init__(self):
        now = datetime.now().isoformat()
        if not self.created_at:
            self.created_at = now
        self.updated_at = now


class RateLimiter:
    """Rate Limiter ที่ทำงานจริง"""

    def __init__(self, requests_per_minute: int = 40, tokens_per_minute: int = 100000):
        self.rpm_limit = requests_per_minute
        self.tpm_limit = tokens_per_minute
        self.requests = []  # timestamps of requests
        self.tokens = []    # (timestamp, token_count) tuples
        self.lock = threading.Lock()

    def _cleanup_old_entries(self):
        """ลบ entries ที่เก่ากว่า 1 นาที"""
        cutoff = datetime.now() - timedelta(minutes=1)
        self.requests = [r for r in self.requests if r > cutoff]
        self.tokens = [(t, c) for t, c in self.tokens if t > cutoff]

    def can_proceed(self, estimated_tokens: int = 5000) -> tuple[bool, int]:
        """
        ตรวจสอบว่าสามารถทำ request ได้หรือไม่
        Returns: (can_proceed, wait_seconds)
        """
        with self.lock:
            self._cleanup_old_entries()

            # Check RPM
            if len(self.requests) >= self.rpm_limit:
                oldest = min(self.requests)
                wait_seconds = 60 - (datetime.now() - oldest).seconds + 1
                return False, wait_seconds

            # Check TPM
            total_tokens = sum(c for _, c in self.tokens)
            if total_tokens + estimated_tokens > self.tpm_limit:
                oldest = min(t for t, _ in self.tokens)
                wait_seconds = 60 - (datetime.now() - oldest).seconds + 1
                return False, wait_seconds

            return True, 0

    def record_request(self, tokens_used: int):
        """บันทึก request ที่ทำไป"""
        with self.lock:
            now = datetime.now()
            self.requests.append(now)
            self.tokens.append((now, tokens_used))

    def get_status(self) -> Dict[str, Any]:
        """ดูสถานะ rate limit ปัจจุบัน"""
        with self.lock:
            self._cleanup_old_entries()
            return {
                "requests_used": len(self.requests),
                "requests_limit": self.rpm_limit,
                "tokens_used": sum(c for _, c in self.tokens),
                "tokens_limit": self.tpm_limit,
                "can_proceed": len(self.requests) < self.rpm_limit
            }


class JobQueue:
    """
    Job Queue Manager
    - Track งานที่ค้าง
    - Auto-retry เมื่อ fail
    - Resume เมื่อ rate limit หมด
    """

    def __init__(self, queue_dir: str = None):
        if queue_dir is None:
            queue_dir = Path(__file__).parent / "data"
        self.queue_dir = Path(queue_dir)
        self.queue_dir.mkdir(parents=True, exist_ok=True)

        self.jobs_file = self.queue_dir / "jobs.json"
        self.rate_limiter = RateLimiter(requests_per_minute=40)
        self.lock = threading.Lock()

        # Load existing jobs
        self.jobs: Dict[str, Job] = {}
        self._load_jobs()

    def _load_jobs(self):
        """โหลด jobs จากไฟล์"""
        if self.jobs_file.exists():
            try:
                with open(self.jobs_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for job_id, job_data in data.items():
                        self.jobs[job_id] = Job(**job_data)
                logger.info(f"Loaded {len(self.jobs)} jobs from queue")
            except Exception as e:
                logger.error(f"Failed to load jobs: {e}")
                self.jobs = {}

    def _save_jobs(self):
        """บันทึก jobs ลงไฟล์"""
        with self.lock:
            data = {job_id: asdict(job) for job_id, job in self.jobs.items()}
            with open(self.jobs_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

    def add_job(self,
                job_type: JobType,
                story_id: str,
                input_data: Dict[str, Any],
                chapter_num: int = None,
                priority: int = 5) -> Job:
        """เพิ่มงานใหม่เข้าคิว"""
        job_id = f"{job_type.value}_{story_id}_{chapter_num or 0}_{int(time.time())}"

        job = Job(
            id=job_id,
            job_type=job_type.value,
            story_id=story_id,
            chapter_num=chapter_num,
            input_data=input_data,
            priority=priority
        )

        self.jobs[job_id] = job
        self._save_jobs()
        logger.info(f"Added job: {job_id}")
        return job

    def get_next_job(self) -> Optional[Job]:
        """ดึงงานถัดไปที่พร้อมทำ"""
        # Check rate limit first
        can_proceed, wait_seconds = self.rate_limiter.can_proceed()

        if not can_proceed:
            logger.warning(f"Rate limited. Wait {wait_seconds} seconds.")
            return None

        # Get pending or rate_limited jobs, sorted by priority
        eligible_jobs = [
            job for job in self.jobs.values()
            if job.status in [JobStatus.PENDING.value, JobStatus.RATE_LIMITED.value]
        ]

        if not eligible_jobs:
            return None

        # Sort by priority (lower = higher priority), then by created_at
        eligible_jobs.sort(key=lambda j: (j.priority, j.created_at))

        return eligible_jobs[0]

    def start_job(self, job_id: str):
        """เริ่มทำงาน"""
        if job_id in self.jobs:
            job = self.jobs[job_id]
            job.status = JobStatus.IN_PROGRESS.value
            job.started_at = datetime.now().isoformat()
            job.updated_at = datetime.now().isoformat()
            self._save_jobs()
            logger.info(f"Started job: {job_id}")

    def complete_job(self, job_id: str, result: Dict[str, Any]):
        """งานเสร็จสมบูรณ์"""
        if job_id in self.jobs:
            job = self.jobs[job_id]
            job.status = JobStatus.COMPLETED.value
            job.completed_at = datetime.now().isoformat()
            job.updated_at = datetime.now().isoformat()
            job.result = result
            self._save_jobs()
            logger.info(f"Completed job: {job_id}")

    def fail_job(self, job_id: str, error: str, is_rate_limit: bool = False):
        """งาน fail"""
        if job_id in self.jobs:
            job = self.jobs[job_id]
            job.retry_count += 1
            job.error_message = error
            job.updated_at = datetime.now().isoformat()

            if is_rate_limit:
                # Rate limited - will retry later
                job.status = JobStatus.RATE_LIMITED.value
                logger.warning(f"Job {job_id} rate limited. Will retry.")
            elif job.retry_count >= job.max_retries:
                # Max retries reached
                job.status = JobStatus.FAILED.value
                logger.error(f"Job {job_id} failed after {job.retry_count} retries: {error}")
            else:
                # Will retry
                job.status = JobStatus.PENDING.value
                logger.warning(f"Job {job_id} failed (attempt {job.retry_count}). Will retry: {error}")

            self._save_jobs()

    def pause_job(self, job_id: str):
        """หยุดงานชั่วคราว"""
        if job_id in self.jobs:
            self.jobs[job_id].status = JobStatus.PAUSED.value
            self.jobs[job_id].updated_at = datetime.now().isoformat()
            self._save_jobs()

    def resume_job(self, job_id: str):
        """Resume งานที่หยุดไว้"""
        if job_id in self.jobs:
            self.jobs[job_id].status = JobStatus.PENDING.value
            self.jobs[job_id].updated_at = datetime.now().isoformat()
            self._save_jobs()
            logger.info(f"Resumed job: {job_id}")

    def get_pending_jobs(self) -> List[Job]:
        """ดูงานที่รอดำเนินการ"""
        return [
            job for job in self.jobs.values()
            if job.status in [JobStatus.PENDING.value, JobStatus.RATE_LIMITED.value]
        ]

    def get_failed_jobs(self) -> List[Job]:
        """ดูงานที่ fail"""
        return [
            job for job in self.jobs.values()
            if job.status == JobStatus.FAILED.value
        ]

    def get_jobs_by_story(self, story_id: str) -> List[Job]:
        """ดูงานทั้งหมดของเรื่องหนึ่ง"""
        return [job for job in self.jobs.values() if job.story_id == story_id]

    def retry_failed_jobs(self):
        """Reset failed jobs เพื่อ retry ใหม่"""
        count = 0
        for job in self.jobs.values():
            if job.status == JobStatus.FAILED.value:
                job.status = JobStatus.PENDING.value
                job.retry_count = 0
                job.error_message = None
                job.updated_at = datetime.now().isoformat()
                count += 1

        if count > 0:
            self._save_jobs()
            logger.info(f"Reset {count} failed jobs for retry")

        return count

    def get_queue_status(self) -> Dict[str, Any]:
        """ดูสถานะคิวทั้งหมด"""
        status_counts = {}
        for status in JobStatus:
            status_counts[status.value] = len([
                j for j in self.jobs.values() if j.status == status.value
            ])

        return {
            "total_jobs": len(self.jobs),
            "by_status": status_counts,
            "rate_limiter": self.rate_limiter.get_status()
        }

    def cleanup_old_completed(self, days: int = 7):
        """ลบงานที่เสร็จแล้วนานกว่า X วัน"""
        cutoff = datetime.now() - timedelta(days=days)
        to_remove = []

        for job_id, job in self.jobs.items():
            if job.status == JobStatus.COMPLETED.value:
                if job.completed_at:
                    completed = datetime.fromisoformat(job.completed_at)
                    if completed < cutoff:
                        to_remove.append(job_id)

        for job_id in to_remove:
            del self.jobs[job_id]

        if to_remove:
            self._save_jobs()
            logger.info(f"Cleaned up {len(to_remove)} old completed jobs")


# Singleton instance
_queue_instance: Optional[JobQueue] = None


def get_queue() -> JobQueue:
    """Get singleton queue instance"""
    global _queue_instance
    if _queue_instance is None:
        _queue_instance = JobQueue()
    return _queue_instance


# CLI commands
if __name__ == "__main__":
    import sys

    queue = get_queue()

    if len(sys.argv) < 2:
        print("Usage: python job_queue.py <command>")
        print("Commands: status, pending, failed, retry-all, cleanup")
        sys.exit(1)

    command = sys.argv[1]

    if command == "status":
        status = queue.get_queue_status()
        print(json.dumps(status, indent=2, ensure_ascii=False))

    elif command == "pending":
        jobs = queue.get_pending_jobs()
        for job in jobs:
            print(f"[{job.priority}] {job.id}: {job.job_type} - {job.story_id}")

    elif command == "failed":
        jobs = queue.get_failed_jobs()
        for job in jobs:
            print(f"{job.id}: {job.error_message}")

    elif command == "retry-all":
        count = queue.retry_failed_jobs()
        print(f"Reset {count} jobs for retry")

    elif command == "cleanup":
        queue.cleanup_old_completed()
        print("Cleanup completed")

    else:
        print(f"Unknown command: {command}")
