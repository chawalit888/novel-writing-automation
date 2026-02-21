#!/usr/bin/env python3
"""
Fix Chapter Fields Script
เพิ่มฟิลด์ที่ขาดหายไปในไฟล์ chapter JSON ทั้งหมด
- slug
- novelSlug
- publishedAt
"""

import json
from pathlib import Path
from datetime import datetime, timedelta

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
CHAPTERS_DIR = PROJECT_ROOT / "novel-promo-site" / "src" / "content" / "chapters"

def fix_chapters():
    """แก้ไข chapter files ทั้งหมด"""
    print("🔧 กำลังแก้ไข chapter fields...\n")

    base_date = datetime(2025, 2, 1)  # วันเริ่มต้น
    total_fixed = 0
    total_chapters = 0

    # Loop ทุก novel directory
    for novel_dir in sorted(CHAPTERS_DIR.iterdir()):
        if not novel_dir.is_dir() or novel_dir.name.startswith('.'):
            continue

        novel_slug = novel_dir.name
        chapter_files = sorted(novel_dir.glob('*.json'))

        if not chapter_files:
            continue

        print(f"📖 {novel_slug} ({len(chapter_files)} ตอน)")

        for chapter_file in chapter_files:
            total_chapters += 1

            # อ่านไฟล์
            with open(chapter_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # เช็คว่าขาดฟิลด์ไหน
            needs_update = False

            # 1. เพิ่ม slug (จากชื่อไฟล์)
            if 'slug' not in data:
                # ลบ .json ออก
                slug = chapter_file.stem
                data['slug'] = slug
                needs_update = True

            # 2. เพิ่ม novelSlug
            if 'novelSlug' not in data:
                data['novelSlug'] = novel_slug
                needs_update = True

            # 3. เพิ่ม publishedAt
            if 'publishedAt' not in data:
                # ใช้ chapter number เพื่อคำนวณวันที่
                chapter_num = data.get('number', 1)
                published_date = base_date + timedelta(days=chapter_num - 1)
                data['publishedAt'] = published_date.strftime('%Y-%m-%d')
                needs_update = True

            # เขียนกลับถ้ามีการแก้ไข
            if needs_update:
                with open(chapter_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                total_fixed += 1

    # สรุปผล
    print(f"\n{'='*60}")
    print(f"✅ เสร็จสิ้น:")
    print(f"   - ตรวจสอบ: {total_chapters} ตอน")
    print(f"   - แก้ไข: {total_fixed} ตอน")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    fix_chapters()
