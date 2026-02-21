#!/usr/bin/env python3
"""
Auto-Resume Script
- รันเป็น background process
- ตรวจสอบ job queue ทุก X วินาที
- Auto-retry เมื่อ rate limit หมด
- เรียก n8n workflow หรือ Claude API โดยตรง
"""

import os
import sys
import time
import json
import logging
import requests
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from job_queue import JobQueue, JobType, JobStatus, get_queue

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(Path(__file__).parent / "data" / "auto_resume.log")
    ]
)
logger = logging.getLogger("AutoResume")


class AutoResumeWorker:
    """
    Worker ที่รัน background เพื่อ process jobs อัตโนมัติ
    """

    def __init__(self,
                 n8n_base_url: str = "http://localhost:5678",
                 check_interval: int = 30,
                 rate_limit_wait: int = 60):
        self.queue = get_queue()
        self.n8n_base_url = n8n_base_url
        self.check_interval = check_interval
        self.rate_limit_wait = rate_limit_wait
        self.running = False

        # Workflow endpoints
        self.workflows = {
            JobType.WRITE_CHAPTER.value: "/webhook/chapter-writer",
            JobType.CREATE_CHARACTER.value: "/webhook/character-generator",
            JobType.CREATE_PLOT.value: "/webhook/plot-outliner",
            JobType.QC_CHECK.value: "/webhook/qc-scorer",
        }

    def call_workflow(self, job_type: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """เรียก n8n workflow"""
        endpoint = self.workflows.get(job_type)
        if not endpoint:
            raise ValueError(f"Unknown job type: {job_type}")

        url = f"{self.n8n_base_url}{endpoint}"
        logger.info(f"Calling workflow: {url}")

        try:
            response = requests.post(
                url,
                json=input_data,
                timeout=300  # 5 minutes timeout for long writes
            )

            # Check for rate limit response
            if response.status_code == 429:
                return {"error": "rate_limited", "retry_after": 60}

            # Check for success
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "error": f"HTTP {response.status_code}",
                    "message": response.text[:500]
                }

        except requests.exceptions.Timeout:
            return {"error": "timeout"}
        except requests.exceptions.ConnectionError:
            return {"error": "connection_error", "message": "Cannot connect to n8n"}
        except Exception as e:
            return {"error": "exception", "message": str(e)}

    def process_job(self, job) -> bool:
        """
        Process a single job
        Returns: True if successful, False otherwise
        """
        job_id = job.id
        logger.info(f"Processing job: {job_id}")

        # Start the job
        self.queue.start_job(job_id)

        # Check rate limit
        can_proceed, wait_seconds = self.queue.rate_limiter.can_proceed()
        if not can_proceed:
            logger.warning(f"Rate limited. Marking job for later. Wait: {wait_seconds}s")
            self.queue.fail_job(job_id, "Rate limited", is_rate_limit=True)
            return False

        # Call the workflow
        try:
            result = self.call_workflow(job.job_type, job.input_data)

            # Handle rate limit
            if result.get("error") == "rate_limited":
                self.queue.fail_job(job_id, "Rate limited by API", is_rate_limit=True)
                return False

            # Handle other errors
            if "error" in result:
                error_msg = result.get("message", result.get("error"))
                self.queue.fail_job(job_id, error_msg)
                return False

            # Success!
            self.queue.complete_job(job_id, result)

            # Record the request for rate limiting
            tokens_used = result.get("tokens_used", 5000)
            self.queue.rate_limiter.record_request(tokens_used)

            logger.info(f"Job {job_id} completed successfully")
            return True

        except Exception as e:
            logger.error(f"Job {job_id} failed with exception: {e}")
            self.queue.fail_job(job_id, str(e))
            return False

    def run_once(self) -> Dict[str, Any]:
        """Run one cycle of job processing"""
        results = {
            "processed": 0,
            "succeeded": 0,
            "failed": 0,
            "rate_limited": 0
        }

        # Get next job
        job = self.queue.get_next_job()

        while job:
            # Check rate limit before processing
            can_proceed, wait_seconds = self.queue.rate_limiter.can_proceed()

            if not can_proceed:
                logger.info(f"Rate limit reached. Waiting {wait_seconds}s...")
                results["rate_limited"] += 1
                time.sleep(wait_seconds)
                break

            # Process the job
            success = self.process_job(job)
            results["processed"] += 1

            if success:
                results["succeeded"] += 1
            else:
                results["failed"] += 1

            # Small delay between jobs
            time.sleep(2)

            # Get next job
            job = self.queue.get_next_job()

        return results

    def run_continuous(self):
        """Run continuously, checking for new jobs"""
        self.running = True
        logger.info("Starting Auto-Resume Worker...")
        logger.info(f"Check interval: {self.check_interval}s")
        logger.info(f"N8n URL: {self.n8n_base_url}")

        while self.running:
            try:
                # Check queue status
                status = self.queue.get_queue_status()
                pending = status["by_status"].get("pending", 0)
                rate_limited = status["by_status"].get("rate_limited", 0)

                if pending > 0 or rate_limited > 0:
                    logger.info(f"Queue: {pending} pending, {rate_limited} rate-limited")

                    # Process jobs
                    results = self.run_once()
                    logger.info(f"Cycle results: {results}")
                else:
                    logger.debug("No pending jobs")

                # Wait before next check
                time.sleep(self.check_interval)

            except KeyboardInterrupt:
                logger.info("Received shutdown signal")
                self.stop()
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(10)

    def stop(self):
        """Stop the worker"""
        self.running = False
        logger.info("Auto-Resume Worker stopped")


class BatchJobCreator:
    """Helper class เพื่อสร้าง batch jobs สำหรับเขียนนิยายทั้งเรื่อง"""

    def __init__(self):
        self.queue = get_queue()

    def create_story_jobs(self,
                          story_id: str,
                          total_chapters: int,
                          outline_path: str,
                          start_chapter: int = 1,
                          priority: int = 5) -> int:
        """
        สร้าง jobs สำหรับเขียนนิยายทุกตอน

        Args:
            story_id: ID ของเรื่อง
            total_chapters: จำนวนตอนทั้งหมด
            outline_path: path ไปยังไฟล์ outline
            start_chapter: เริ่มจากตอนที่เท่าไหร่
            priority: ความสำคัญ (1-10)

        Returns:
            จำนวน jobs ที่สร้าง
        """
        count = 0

        for chapter_num in range(start_chapter, total_chapters + 1):
            input_data = {
                "story_id": story_id,
                "chapter_num": chapter_num,
                "outline_path": outline_path,
                "total_chapters": total_chapters
            }

            # ตอนที่ 1-10 priority สูงกว่า (Freemium Strategy)
            chapter_priority = priority - 2 if chapter_num <= 10 else priority

            self.queue.add_job(
                job_type=JobType.WRITE_CHAPTER,
                story_id=story_id,
                input_data=input_data,
                chapter_num=chapter_num,
                priority=chapter_priority
            )
            count += 1

        logger.info(f"Created {count} jobs for story: {story_id}")
        return count

    def get_story_progress(self, story_id: str) -> Dict[str, Any]:
        """ดู progress ของเรื่อง"""
        jobs = self.queue.get_jobs_by_story(story_id)

        completed = [j for j in jobs if j.status == JobStatus.COMPLETED.value]
        pending = [j for j in jobs if j.status == JobStatus.PENDING.value]
        failed = [j for j in jobs if j.status == JobStatus.FAILED.value]
        in_progress = [j for j in jobs if j.status == JobStatus.IN_PROGRESS.value]

        total = len(jobs)
        progress = len(completed) / total * 100 if total > 0 else 0

        return {
            "story_id": story_id,
            "total_jobs": total,
            "completed": len(completed),
            "pending": len(pending),
            "failed": len(failed),
            "in_progress": len(in_progress),
            "progress_percent": round(progress, 1),
            "completed_chapters": sorted([j.chapter_num for j in completed if j.chapter_num]),
            "failed_chapters": sorted([j.chapter_num for j in failed if j.chapter_num])
        }


def resume_rate_limited_jobs():
    """Resume งานที่ติด rate limit"""
    queue = get_queue()
    count = 0

    for job in queue.jobs.values():
        if job.status == JobStatus.RATE_LIMITED.value:
            job.status = JobStatus.PENDING.value
            job.updated_at = datetime.now().isoformat()
            count += 1

    if count > 0:
        queue._save_jobs()
        logger.info(f"Resumed {count} rate-limited jobs")

    return count


# CLI
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Auto-Resume Worker for Novel Writing")
    parser.add_argument("command", choices=["run", "once", "status", "create-story", "progress", "resume-all"],
                        help="Command to execute")
    parser.add_argument("--story-id", help="Story ID for create-story/progress commands")
    parser.add_argument("--chapters", type=int, help="Total chapters for create-story")
    parser.add_argument("--outline", help="Outline file path")
    parser.add_argument("--start", type=int, default=1, help="Start chapter number")
    parser.add_argument("--n8n-url", default="http://localhost:5678", help="N8n base URL")
    parser.add_argument("--interval", type=int, default=30, help="Check interval in seconds")

    args = parser.parse_args()

    if args.command == "run":
        worker = AutoResumeWorker(
            n8n_base_url=args.n8n_url,
            check_interval=args.interval
        )
        worker.run_continuous()

    elif args.command == "once":
        worker = AutoResumeWorker(n8n_base_url=args.n8n_url)
        results = worker.run_once()
        print(json.dumps(results, indent=2))

    elif args.command == "status":
        queue = get_queue()
        status = queue.get_queue_status()
        print(json.dumps(status, indent=2, ensure_ascii=False))

    elif args.command == "create-story":
        if not args.story_id or not args.chapters:
            print("Error: --story-id and --chapters required")
            sys.exit(1)

        creator = BatchJobCreator()
        count = creator.create_story_jobs(
            story_id=args.story_id,
            total_chapters=args.chapters,
            outline_path=args.outline or "",
            start_chapter=args.start
        )
        print(f"Created {count} jobs")

    elif args.command == "progress":
        if not args.story_id:
            print("Error: --story-id required")
            sys.exit(1)

        creator = BatchJobCreator()
        progress = creator.get_story_progress(args.story_id)
        print(json.dumps(progress, indent=2, ensure_ascii=False))

    elif args.command == "resume-all":
        count = resume_rate_limited_jobs()
        queue = get_queue()
        count2 = queue.retry_failed_jobs()
        print(f"Resumed {count} rate-limited + {count2} failed jobs")
