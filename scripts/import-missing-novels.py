#!/usr/bin/env python3
"""
Import Missing Novels with Chapters
Import 3 novels ที่มีตอนในโฟลเดอร์ต้นฉบับแต่ยังไม่ได้ import เข้าเว็บ
"""

import json
import re
from pathlib import Path
from datetime import datetime, timedelta

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
NOVELS_NC_DIR = PROJECT_ROOT / "novels-nc"
WEBSITE_CHAPTERS_DIR = PROJECT_ROOT / "novel-promo-site" / "src" / "content" / "chapters"

# Novels to import
NOVELS_TO_IMPORT = {
    "2. สวาทลับคุณหนูมาเฟีย": {
        "slug": "sawat-lub-khunnoo-mafia",
        "chapters_subdir": "chapters"
    },
    "3. สัญญารักลับห้องประธาน": {
        "slug": "sanya-rak-lub-hong-prathan",
        "chapters_subdir": "ตอน"
    },
    "4. คุณหนูร้อนรักกับนายมาเฟีย-ภาค2": {
        "slug": "khunnoo-ron-rak-mafia-s2",
        "chapters_subdir": "chapters"
    }
}

def extract_chapter_number(filename):
    """Extract chapter number from filename"""
    # Match patterns like: บทที่-29.1, ตอนที่01, etc.
    patterns = [
        r'บทที่[- ]?(\d+\.?\d*)',
        r'ตอนที่[- ]?(\d+\.?\d*)',
        r'chapter[- ]?(\d+\.?\d*)',
    ]

    for pattern in patterns:
        match = re.search(pattern, filename, re.IGNORECASE)
        if match:
            num_str = match.group(1)
            # Return as float if has decimal, otherwise int
            if '.' in num_str:
                return float(num_str)
            else:
                return int(num_str)

    return None

def extract_title(filename):
    """Extract chapter title from filename"""
    # Remove extension
    name = filename.replace('.txt', '')

    # Try to extract title after chapter number
    patterns = [
        r'บทที่[- ]?\d+\.?\d*[- ]?(.+)',
        r'ตอนที่[- ]?\d+\.?\d*[- ]?(.+)',
    ]

    for pattern in patterns:
        match = re.search(pattern, name, re.IGNORECASE)
        if match:
            title = match.group(1).strip()
            # Clean up the title
            title = re.sub(r'^[-\s]+', '', title)
            title = re.sub(r'[-\s]+$', '', title)
            return title

    # Fallback: use filename without extension
    return name

def generate_slug(chapter_num):
    """Generate slug for chapter"""
    if isinstance(chapter_num, float):
        # For decimal numbers like 29.1, use format "29-1"
        major, minor = str(chapter_num).split('.')
        return f"{major}-{minor}"
    else:
        return str(chapter_num)

def parse_chapter(file_path, novel_slug, chapter_index):
    """Parse a chapter text file into JSON structure"""
    filename = file_path.name

    # Extract chapter number
    chapter_num = extract_chapter_number(filename)
    if chapter_num is None:
        print(f"  ⚠️  ไม่สามารถหาเลขตอนจาก: {filename}")
        return None

    # Extract title
    title = extract_title(filename)
    if not title:
        title = f"ตอนที่ {chapter_num}"

    # Read content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
    except Exception as e:
        print(f"  ❌ ไม่สามารถอ่านไฟล์: {filename} - {e}")
        return None

    # Determine if free (first 10 chapters)
    is_free = chapter_index < 10

    # Generate slug
    slug = generate_slug(chapter_num)

    # Published date (base date + chapter index)
    base_date = datetime(2025, 2, 1)
    published_date = base_date + timedelta(days=chapter_index)

    return {
        "slug": slug,
        "novelSlug": novel_slug,
        "number": int(chapter_num) if isinstance(chapter_num, int) else chapter_num,
        "title": title,
        "content": content,
        "isFree": is_free,
        "publishedAt": published_date.strftime('%Y-%m-%d')
    }

def import_novel(novel_folder_name, config):
    """Import all chapters of a novel"""
    novel_slug = config['slug']
    chapters_subdir = config['chapters_subdir']

    print(f"\n📖 {novel_folder_name}")
    print(f"   Slug: {novel_slug}")

    # Source directory
    source_dir = NOVELS_NC_DIR / novel_folder_name / chapters_subdir

    if not source_dir.exists():
        print(f"   ❌ ไม่พบโฟลเดอร์: {source_dir}")
        return 0

    # Get all chapter files
    chapter_files = sorted(
        [f for f in source_dir.glob('*.txt') if f.is_file()],
        key=lambda f: extract_chapter_number(f.name) or 0
    )

    if not chapter_files:
        print(f"   ❌ ไม่พบไฟล์ตอน")
        return 0

    print(f"   พบ {len(chapter_files)} ตอน")

    # Create output directory
    output_dir = WEBSITE_CHAPTERS_DIR / novel_slug
    output_dir.mkdir(parents=True, exist_ok=True)

    # Import each chapter
    imported_count = 0
    for idx, chapter_file in enumerate(chapter_files):
        chapter_data = parse_chapter(chapter_file, novel_slug, idx)

        if not chapter_data:
            continue

        # Output file
        output_file = output_dir / f"{chapter_data['slug']}.json"

        # Write JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(chapter_data, f, ensure_ascii=False, indent=2)

        imported_count += 1

        # Show progress every 10 chapters
        if (idx + 1) % 10 == 0:
            print(f"   ... {idx + 1}/{len(chapter_files)} ตอน")

    print(f"   ✅ Import สำเร็จ: {imported_count} ตอน")
    return imported_count

def main():
    """Main function"""
    print("🚀 Import Missing Novels with Chapters\n")
    print(f"📂 Source: {NOVELS_NC_DIR}")
    print(f"📂 Target: {WEBSITE_CHAPTERS_DIR}\n")

    total_imported = 0

    for novel_folder, config in NOVELS_TO_IMPORT.items():
        try:
            count = import_novel(novel_folder, config)
            total_imported += count
        except Exception as e:
            print(f"   ❌ Error: {e}")
            import traceback
            traceback.print_exc()

    # Summary
    print(f"\n{'='*60}")
    print(f"✅ เสร็จสิ้น:")
    print(f"   - Import ทั้งหมด: {total_imported} ตอน")
    print(f"   - จาก: {len(NOVELS_TO_IMPORT)} เรื่อง")
    print(f"{'='*60}\n")

    if total_imported > 0:
        print("💡 ขั้นตอนถัดไป:")
        print("   1. Restart dev server: npm run dev")
        print("   2. เปิดเว็บตรวจสอบ: http://localhost:3001")
        print()

if __name__ == "__main__":
    main()
