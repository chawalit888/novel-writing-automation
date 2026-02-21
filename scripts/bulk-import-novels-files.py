#!/usr/bin/env python3
"""
Bulk Import Novels Script (File-based)
เขียนไฟล์นิยายลง content/novels/ โดยตรง (ไม่ผ่าน API)
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
PARSED_NOVELS_FILE = PROJECT_ROOT / "parsed-novels.json"
PLATFORM_URLS_FILE = PROJECT_ROOT / "novel-platform-urls.json"
NOVELS_DIR = PROJECT_ROOT / "novels"
NOVELS_NC_DIR = PROJECT_ROOT / "novels-nc"
WEB_NOVELS_DIR = PROJECT_ROOT / "novel-promo-site" / "src" / "content" / "novels"
WEB_CHAPTERS_DIR = PROJECT_ROOT / "novel-promo-site" / "src" / "content" / "chapters"

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
    platform_urls = load_platform_urls()

    # หา folder path จาก slug
    for folder_path, data in platform_urls.items():
        if data.get('slug') == novel_slug:
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

    # Extract chapter number จากชื่อไฟล์
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

def write_novel_json(novel_data, dry_run=False):
    """เขียนไฟล์ JSON ของนิยาย"""
    novel_slug = novel_data['slug']
    output_file = WEB_NOVELS_DIR / f"{novel_slug}.json"

    if dry_run:
        print(f"   [DRY RUN] จะเขียนไฟล์: {output_file.name}")
        return True

    try:
        # สร้างโฟลเดอร์ถ้ายังไม่มี
        WEB_NOVELS_DIR.mkdir(parents=True, exist_ok=True)

        # เขียนไฟล์
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(novel_data, f, ensure_ascii=False, indent=2)

        return True

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def write_chapter_json(novel_slug, chapter_data, dry_run=False):
    """เขียนไฟล์ JSON ของตอน"""
    # สร้างโฟลเดอร์ของนิยาย
    novel_chapters_dir = WEB_CHAPTERS_DIR / novel_slug
    chapter_file = novel_chapters_dir / f"{chapter_data['number']}.json"

    if dry_run:
        return True

    try:
        # สร้างโฟลเดอร์ถ้ายังไม่มี
        novel_chapters_dir.mkdir(parents=True, exist_ok=True)

        # เขียนไฟล์
        with open(chapter_file, 'w', encoding='utf-8') as f:
            json.dump(chapter_data, f, ensure_ascii=False, indent=2)

        return True

    except Exception as e:
        print(f"      ❌ Error writing chapter {chapter_data['number']}: {e}")
        return False

def import_novel_with_chapters(novel, dry_run=False, skip_existing=False):
    """Import นิยาย 1 เรื่องพร้อมตอน"""
    novel_slug = novel['slug']
    novel_title = novel['title']

    print(f"\n  📖 {novel_title} ({novel_slug})")

    # ตรวจสอบว่ามีไฟล์อยู่แล้วไหม
    existing_file = WEB_NOVELS_DIR / f"{novel_slug}.json"
    if skip_existing and existing_file.exists():
        print(f"     ⏭️  ข้าม (มีไฟล์อยู่แล้ว)")
        return True

    # 1. เขียนไฟล์ novel metadata
    print(f"     📝 Writing novel JSON...")
    success = write_novel_json(novel, dry_run=dry_run)

    if not success:
        return False

    if not dry_run:
        print(f"     ✅ เขียนไฟล์ {novel_slug}.json")

    # 2. หา directory ของนิยาย
    novel_dir = find_novel_dir(novel_slug)

    if not novel_dir:
        print(f"     ⚠️  ไม่พบโฟลเดอร์นิยาย ข้ามการเขียนตอน")
        return True

    # 3. เขียนไฟล์ตอนทั้งหมด
    # หาในโฟลเดอร์หลักก่อน
    chapter_files = sorted(novel_dir.glob("ตอนที่*.txt"))

    # ถ้าไม่เจอ ลองหาในโฟลเดอร์ย่อย "ตอน/" หรือ "chapters/"
    if not chapter_files:
        chapter_subdir = novel_dir / "ตอน"
        if chapter_subdir.exists():
            chapter_files = sorted(chapter_subdir.glob("ตอนที่*.txt"))

    if not chapter_files:
        chapter_subdir = novel_dir / "chapters"
        if chapter_subdir.exists():
            chapter_files = sorted(chapter_subdir.glob("ตอนที่*.txt"))

    if not chapter_files:
        print(f"     ⚠️  ไม่พบไฟล์ตอน")
        return True

    total_chapters = len(chapter_files)
    written_count = 0
    error_count = 0

    print(f"     📚 พบ {total_chapters} ตอน กำลังเขียนไฟล์...")

    for chapter_file in chapter_files:
        chapter_data = parse_chapter_file(chapter_file)

        if not chapter_data:
            continue

        success = write_chapter_json(novel_slug, chapter_data, dry_run=dry_run)

        if success:
            written_count += 1
            # แสดงความคืบหน้าทุก 10 ตอน
            if chapter_data['number'] % 10 == 0 or chapter_data['number'] <= 3:
                status = "ฟรี" if chapter_data['isFree'] else "Premium"
                if not dry_run:
                    print(f"        ✓ ตอนที่ {chapter_data['number']:02d}: {chapter_data['title'][:30]}... ({status})")
                else:
                    print(f"      [DRY RUN] ตอนที่ {chapter_data['number']:02d}")
        else:
            error_count += 1

    if not dry_run:
        print(f"     ✅ เขียนตอน: {written_count}/{total_chapters}")
    else:
        print(f"   [DRY RUN] จะเขียน {written_count} ตอน")

    if error_count > 0:
        print(f"     ⚠️  Error: {error_count} ตอน")

    return True

def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(description='Bulk import novels (file-based)')
    parser.add_argument('--dry-run', action='store_true', help='ทดสอบโดยไม่เขียนไฟล์จริง')
    parser.add_argument('--skip-existing', action='store_true', help='ข้ามนิยายที่มีไฟล์อยู่แล้ว')
    parser.add_argument('--limit', type=int, help='จำกัดจำนวนเรื่องที่จะ import')

    args = parser.parse_args()

    print("🚀 Bulk Import Novels (File-based)\n")

    if args.dry_run:
        print("⚠️  DRY RUN MODE - จะไม่เขียนไฟล์จริง\n")

    # ตรวจสอบโฟลเดอร์เว็บ
    if not WEB_NOVELS_DIR.exists():
        print(f"❌ ไม่พบโฟลเดอร์: {WEB_NOVELS_DIR}")
        print("   กรุณาตรวจสอบว่าเว็บไซต์อยู่ที่ถูกต้อง")
        sys.exit(1)

    # โหลดนิยายที่ parse แล้ว
    novels = load_parsed_novels()

    if args.limit:
        novels = novels[:args.limit]

    print(f"📚 พบนิยาย {len(novels)} เรื่อง")
    print(f"📁 เขียนไฟล์ลง: {WEB_NOVELS_DIR.relative_to(PROJECT_ROOT)}\n")
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
        print("   python scripts/bulk-import-novels-files.py")
    else:
        print("💡 Refresh เว็บเพื่อดูนิยายใหม่:")
        print("   http://localhost:3000")

    print("\n")

if __name__ == "__main__":
    main()
