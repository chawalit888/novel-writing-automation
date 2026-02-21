#!/usr/bin/env python3
"""
Bulk Import Novels Script
อัพโหลดนิยายทั้งหมดขึ้นเว็บพร้อม 10 ตอนแรก (ฟรี)
"""

import json
import re
import sys
from pathlib import Path
import requests
from datetime import datetime

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
PARSED_NOVELS_FILE = PROJECT_ROOT / "parsed-novels.json"
PLATFORM_URLS_FILE = PROJECT_ROOT / "novel-platform-urls.json"
NOVELS_DIR = PROJECT_ROOT / "novels"
NOVELS_NC_DIR = PROJECT_ROOT / "novels-nc"

# API Configuration
API_BASE_URL = "http://localhost:3000/api"  # เปลี่ยนเป็น production URL ตอน deploy
API_KEY = "your-api-key-here"  # เปลี่ยนเป็น API key จริง

def load_parsed_novels():
    """โหลดนิยายที่ parse แล้ว"""
    if not PARSED_NOVELS_FILE.exists():
        print("❌ ไม่พบไฟล์ parsed-novels.json")
        print("   กรุณารัน parse-novel-metadata.py ก่อน")
        sys.exit(1)

    with open(PARSED_NOVELS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_platform_urls():
    """โหลด platform URLs เพื่อ map slug กับ folder path"""
    if not PLATFORM_URLS_FILE.exists():
        return {}

    with open(PLATFORM_URLS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return {k: v for k, v in data.items() if not k.startswith('_')}

def find_novel_dir(novel_slug):
    """หา directory ของนิยายจาก slug"""
    # โหลด platform URLs เพื่อ map slug กับ folder path
    platform_urls = load_platform_urls()

    # หา folder path จาก slug
    for folder_path, data in platform_urls.items():
        if data.get('slug') == novel_slug:
            # folder_path เช่น "novels/1-ท่านประธานหัวใจไลฟ์สด"
            full_path = PROJECT_ROOT / folder_path
            if full_path.exists():
                return full_path

    # ถ้าไม่เจอใน platform URLs ลองหาแบบเดิม
    for folder in NOVELS_DIR.iterdir():
        if folder.is_dir() and folder.name != 'templates':
            if novel_slug in folder.name.lower():
                return folder

    for folder in NOVELS_NC_DIR.iterdir():
        if folder.is_dir() and folder.name not in ['templates', 'nc-automation', 'nc-server-setup', '1-ตัวอย่างนิยายNC']:
            if novel_slug in folder.name.lower():
                return folder

    return None

def parse_chapter_file(chapter_file):
    """อ่านไฟล์ตอนและแปลงเป็น chapter object"""
    with open(chapter_file, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    # Extract chapter number จากชื่อไฟล์ เช่น "ตอนที่01-ชื่อ.txt" → 1
    filename = chapter_file.name
    chapter_match = re.search(r'ตอนที่(\d+)', filename)

    if not chapter_match:
        return None

    chapter_number = int(chapter_match.group(1))

    # Extract ชื่อตอน
    title_match = re.search(r'ตอนที่\d+-(.+)\.txt', filename)
    chapter_title = title_match.group(1) if title_match else f"ตอนที่ {chapter_number}"

    return {
        'number': chapter_number,
        'title': chapter_title,
        'content': content,
        'isFree': chapter_number <= 10  # 10 ตอนแรกฟรี
    }

def upload_novel(novel_data, dry_run=False):
    """อัพโหลดนิยายขึ้น API"""
    url = f"{API_BASE_URL}/novels"

    if dry_run:
        print(f"   [DRY RUN] POST {url}")
        print(f"   [DRY RUN] Payload: {novel_data['slug']}")
        return True, {"id": "dry-run-id"}

    try:
        response = requests.post(
            url,
            json=novel_data,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            timeout=30
        )

        if response.status_code in [200, 201]:
            return True, response.json()
        else:
            return False, {"error": response.text}

    except Exception as e:
        return False, {"error": str(e)}

def upload_chapter(novel_slug, chapter_data, dry_run=False):
    """อัพโหลดตอนขึ้น API"""
    url = f"{API_BASE_URL}/chapters"

    payload = {
        "novelSlug": novel_slug,
        **chapter_data
    }

    if dry_run:
        print(f"      [DRY RUN] POST {url} - Chapter {chapter_data['number']}")
        return True, {}

    try:
        response = requests.post(
            url,
            json=payload,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            timeout=30
        )

        if response.status_code in [200, 201]:
            return True, response.json()
        else:
            return False, {"error": response.text}

    except Exception as e:
        return False, {"error": str(e)}

def import_novel_with_chapters(novel, dry_run=False, skip_existing=False):
    """Import นิยาย 1 เรื่องพร้อมตอน"""
    import re

    novel_slug = novel['slug']
    novel_title = novel['title']

    print(f"\n  📖 {novel_title} ({novel_slug})")

    # 1. อัพโหลด novel metadata
    print(f"     ⬆️  Uploading novel metadata...")
    success, result = upload_novel(novel, dry_run=dry_run)

    if not success:
        print(f"     ❌ Error: {result.get('error', 'Unknown error')}")
        return False

    print(f"     ✅ Novel uploaded")

    # 2. หา directory ของนิยาย
    novel_dir = find_novel_dir(novel_slug)

    if not novel_dir:
        print(f"     ⚠️  ไม่พบโฟลเดอร์นิยาย ข้ามการอัพโหลดตอน")
        return True  # ยังถือว่าสำเร็จ (มี metadata)

    # 3. อัพโหลดตอนทั้งหมด
    chapter_files = sorted(novel_dir.glob("ตอนที่*.txt"))

    if not chapter_files:
        print(f"     ⚠️  ไม่พบไฟล์ตอน")
        return True

    total_chapters = len(chapter_files)
    uploaded_count = 0
    error_count = 0

    print(f"     📚 พบ {total_chapters} ตอน กำลังอัพโหลด...")

    for chapter_file in chapter_files:
        chapter_data = parse_chapter_file(chapter_file)

        if not chapter_data:
            continue

        success, result = upload_chapter(novel_slug, chapter_data, dry_run=dry_run)

        if success:
            uploaded_count += 1
            if chapter_data['number'] % 10 == 0 or chapter_data['number'] <= 3:
                status = "ฟรี" if chapter_data['isFree'] else "Premium"
                print(f"        ✓ ตอนที่ {chapter_data['number']:02d}: {chapter_data['title']} ({status})")
        else:
            error_count += 1
            if error_count <= 3:  # แสดง error แค่ 3 อันแรก
                print(f"        ✗ ตอนที่ {chapter_data['number']:02d}: Error")

    print(f"     ✅ อัพโหลดตอน: {uploaded_count}/{total_chapters}")

    if error_count > 0:
        print(f"     ⚠️  Error: {error_count} ตอน")

    return True

def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(description='Bulk import novels to website')
    parser.add_argument('--dry-run', action='store_true', help='ทดสอบโดยไม่อัพโหลดจริง')
    parser.add_argument('--skip-existing', action='store_true', help='ข้ามนิยายที่มีอยู่แล้ว')
    parser.add_argument('--limit', type=int, help='จำกัดจำนวนเรื่องที่จะ import')

    args = parser.parse_args()

    print("🚀 Bulk Import Novels to Website\n")

    if args.dry_run:
        print("⚠️  DRY RUN MODE - จะไม่อัพโหลดจริง\n")

    # โหลดนิยายที่ parse แล้ว
    novels = load_parsed_novels()

    if args.limit:
        novels = novels[:args.limit]

    print(f"📚 พบนิยาย {len(novels)} เรื่อง\n")
    print("="*70)

    success_count = 0
    error_count = 0

    for novel in novels:
        try:
            result = import_novel_with_chapters(
                novel,
                dry_run=args.dry_run,
                skip_existing=args.skip_existing
            )

            if result:
                success_count += 1
            else:
                error_count += 1

        except Exception as e:
            print(f"  ❌ Error: {e}")
            error_count += 1

    # สรุปผล
    print(f"\n{'='*70}")
    print(f"✅ เสร็จสิ้น:")
    print(f"   - Import สำเร็จ: {success_count} เรื่อง")
    print(f"   - Error/ข้าม: {error_count} เรื่อง")
    print(f"{'='*70}\n")

    if args.dry_run:
        print("💡 ทำจริงด้วยคำสั่ง:")
        print("   python scripts/bulk-import-novels.py")
        print("\n")

if __name__ == "__main__":
    main()
