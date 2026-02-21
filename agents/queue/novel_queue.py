#!/usr/bin/env python3
"""
Novel Queue - เครื่องมือจัดการคิวเขียนนิยาย

วิธีใช้:
  python novel_queue.py add "story-id" --chapters 36 --outline "path/to/outline.md"
  python novel_queue.py status
  python novel_queue.py progress "story-id"
  python novel_queue.py resume
  python novel_queue.py start
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

from job_queue import JobQueue, JobType, JobStatus, get_queue
from auto_resume import AutoResumeWorker, BatchJobCreator, resume_rate_limited_jobs


def print_header(title: str):
    """Print formatted header"""
    print("\n" + "=" * 50)
    print(f"  {title}")
    print("=" * 50)


def print_status():
    """แสดงสถานะคิวทั้งหมด"""
    queue = get_queue()
    status = queue.get_queue_status()

    print_header("สถานะคิวเขียนนิยาย")

    print(f"\n📊 จำนวนงานทั้งหมด: {status['total_jobs']}")
    print("\n📋 แยกตามสถานะ:")

    status_icons = {
        "pending": "⏳",
        "in_progress": "🔄",
        "completed": "✅",
        "failed": "❌",
        "rate_limited": "⏱️",
        "paused": "⏸️"
    }

    status_thai = {
        "pending": "รอดำเนินการ",
        "in_progress": "กำลังทำ",
        "completed": "เสร็จแล้ว",
        "failed": "ล้มเหลว",
        "rate_limited": "รอ Rate Limit",
        "paused": "หยุดชั่วคราว"
    }

    for status_name, count in status["by_status"].items():
        icon = status_icons.get(status_name, "•")
        thai = status_thai.get(status_name, status_name)
        print(f"   {icon} {thai}: {count}")

    # Rate limiter status
    rl = status["rate_limiter"]
    print(f"\n⚡ Rate Limit:")
    print(f"   Requests: {rl['requests_used']}/{rl['requests_limit']} per minute")
    print(f"   สถานะ: {'🟢 พร้อมใช้งาน' if rl['can_proceed'] else '🔴 รอก่อน'}")


def print_progress(story_id: str):
    """แสดง progress ของเรื่อง"""
    creator = BatchJobCreator()
    progress = creator.get_story_progress(story_id)

    print_header(f"Progress: {story_id}")

    bar_width = 30
    filled = int(progress["progress_percent"] / 100 * bar_width)
    bar = "█" * filled + "░" * (bar_width - filled)

    print(f"\n[{bar}] {progress['progress_percent']}%")
    print(f"\n✅ เสร็จแล้ว: {progress['completed']}/{progress['total_jobs']} ตอน")
    print(f"⏳ รอดำเนินการ: {progress['pending']}")
    print(f"❌ ล้มเหลว: {progress['failed']}")

    if progress["completed_chapters"]:
        print(f"\n📝 ตอนที่เสร็จแล้ว: {', '.join(map(str, progress['completed_chapters']))}")

    if progress["failed_chapters"]:
        print(f"\n⚠️ ตอนที่ล้มเหลว: {', '.join(map(str, progress['failed_chapters']))}")


def add_story(story_id: str, chapters: int, outline: str, start: int = 1):
    """เพิ่มเรื่องใหม่เข้าคิว"""
    creator = BatchJobCreator()
    count = creator.create_story_jobs(
        story_id=story_id,
        total_chapters=chapters,
        outline_path=outline,
        start_chapter=start
    )

    print_header("เพิ่มเรื่องใหม่")
    print(f"\n✅ สร้าง {count} งาน สำหรับ: {story_id}")
    print(f"   - ตอนที่ {start} ถึง {chapters}")
    print(f"   - Outline: {outline}")
    print("\n💡 ใช้คำสั่ง 'python novel_queue.py start' เพื่อเริ่มเขียน")


def resume_jobs():
    """Resume งานที่ค้าง"""
    print_header("Resume งานที่ค้าง")

    # Resume rate limited
    count1 = resume_rate_limited_jobs()
    print(f"\n⏱️ Resume งานที่ติด rate limit: {count1}")

    # Retry failed
    queue = get_queue()
    count2 = queue.retry_failed_jobs()
    print(f"❌ Reset งานที่ล้มเหลว: {count2}")

    total = count1 + count2
    if total > 0:
        print(f"\n✅ รวม {total} งาน พร้อมทำใหม่")
    else:
        print("\n✨ ไม่มีงานที่ต้อง resume")


def list_pending():
    """แสดงรายการงานที่รอ"""
    queue = get_queue()
    jobs = queue.get_pending_jobs()

    print_header("งานที่รอดำเนินการ")

    if not jobs:
        print("\n✨ ไม่มีงานในคิว")
        return

    # Group by story
    by_story = {}
    for job in jobs:
        if job.story_id not in by_story:
            by_story[job.story_id] = []
        by_story[job.story_id].append(job)

    for story_id, story_jobs in by_story.items():
        print(f"\n📖 {story_id}:")
        chapters = sorted([j.chapter_num for j in story_jobs if j.chapter_num])
        if chapters:
            print(f"   ตอนที่รอ: {', '.join(map(str, chapters[:10]))}")
            if len(chapters) > 10:
                print(f"   ... และอีก {len(chapters) - 10} ตอน")


def start_worker(n8n_url: str, interval: int):
    """เริ่ม worker"""
    print_header("เริ่ม Auto-Resume Worker")
    print(f"\n🔧 N8n URL: {n8n_url}")
    print(f"⏱️ Check interval: {interval} วินาที")
    print("\n🚀 กำลังเริ่ม... (กด Ctrl+C เพื่อหยุด)")

    worker = AutoResumeWorker(
        n8n_base_url=n8n_url,
        check_interval=interval
    )
    worker.run_continuous()


def main():
    parser = argparse.ArgumentParser(
        description="Novel Queue - เครื่องมือจัดการคิวเขียนนิยาย",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
ตัวอย่างการใช้งาน:
  %(prog)s status                    ดูสถานะคิว
  %(prog)s add story-1 -c 36         เพิ่มเรื่องใหม่ 36 ตอน
  %(prog)s progress story-1          ดู progress ของเรื่อง
  %(prog)s resume                    Resume งานที่ค้าง
  %(prog)s list                      ดูรายการงานที่รอ
  %(prog)s start                     เริ่ม auto-resume worker
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="คำสั่ง")

    # status
    subparsers.add_parser("status", help="ดูสถานะคิว")

    # add
    add_parser = subparsers.add_parser("add", help="เพิ่มเรื่องใหม่")
    add_parser.add_argument("story_id", help="ID ของเรื่อง")
    add_parser.add_argument("-c", "--chapters", type=int, required=True, help="จำนวนตอน")
    add_parser.add_argument("-o", "--outline", default="", help="path ไปยัง outline")
    add_parser.add_argument("-s", "--start", type=int, default=1, help="เริ่มจากตอนที่")

    # progress
    progress_parser = subparsers.add_parser("progress", help="ดู progress")
    progress_parser.add_argument("story_id", help="ID ของเรื่อง")

    # resume
    subparsers.add_parser("resume", help="Resume งานที่ค้าง")

    # list
    subparsers.add_parser("list", help="ดูรายการงานที่รอ")

    # start
    start_parser = subparsers.add_parser("start", help="เริ่ม worker")
    start_parser.add_argument("--n8n-url", default="http://localhost:5678", help="N8n URL")
    start_parser.add_argument("--interval", type=int, default=30, help="Check interval (วินาที)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == "status":
        print_status()
    elif args.command == "add":
        add_story(args.story_id, args.chapters, args.outline, args.start)
    elif args.command == "progress":
        print_progress(args.story_id)
    elif args.command == "resume":
        resume_jobs()
    elif args.command == "list":
        list_pending()
    elif args.command == "start":
        start_worker(args.n8n_url, args.interval)


if __name__ == "__main__":
    main()
