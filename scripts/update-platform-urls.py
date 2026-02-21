#!/usr/bin/env python3
"""
Update Platform URLs Script
อัปเดต platform URLs ของนิยายที่มีบนเว็บอยู่แล้ว
"""

import json
import os
import sys
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
PLATFORM_URLS_FILE = PROJECT_ROOT / "novel-platform-urls.json"
NOVELS_DIR = PROJECT_ROOT / "novel-promo-site" / "src" / "content" / "novels"

def load_platform_urls():
    """โหลดไฟล์ novel-platform-urls.json"""
    if not PLATFORM_URLS_FILE.exists():
        print(f"❌ ไม่พบไฟล์: {PLATFORM_URLS_FILE}")
        sys.exit(1)

    with open(PLATFORM_URLS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # กรอง entry ที่ขึ้นต้นด้วย _ (metadata)
    return {k: v for k, v in data.items() if not k.startswith('_')}

def update_novel_file(slug, platform_data, dry_run=False):
    """อัปเดตไฟล์ JSON ของนิยาย"""
    novel_file = NOVELS_DIR / f"{slug}.json"

    if not novel_file.exists():
        print(f"  ⚠️  ไม่พบไฟล์: {slug}.json (ข้าม)")
        return False

    # อ่านไฟล์เดิม
    with open(novel_file, 'r', encoding='utf-8') as f:
        novel_data = json.load(f)

    # เช็คว่ามี platform URLs หรือไม่
    platforms = platform_data.get('platforms', {})
    if not platforms or not any(platforms.values()):
        print(f"  ℹ️  {slug}: ไม่มี platform URLs (ข้าม)")
        return False

    # อัปเดตข้อมูล
    novel_data['platforms'] = [name.title() for name, url in platforms.items() if url]
    novel_data['platformUrls'] = {k: v for k, v in platforms.items() if v}
    novel_data['primaryPlatform'] = platform_data.get('primaryPlatform', '')

    if dry_run:
        print(f"  🔍 {slug}:")
        print(f"     - Platforms: {novel_data['platforms']}")
        print(f"     - Primary: {novel_data['primaryPlatform']}")
        print(f"     - URLs: {list(novel_data['platformUrls'].keys())}")
        return True

    # เขียนกลับลงไฟล์
    with open(novel_file, 'w', encoding='utf-8') as f:
        json.dump(novel_data, f, ensure_ascii=False, indent=2)

    print(f"  ✅ {slug}: อัปเดตแล้ว ({len(novel_data['platforms'])} แพลตฟอร์ม)")
    return True

def main():
    """Main function"""
    # เช็ค arguments
    dry_run = '--dry-run' in sys.argv or '-n' in sys.argv

    if dry_run:
        print("🔍 โหมดทดสอบ (Dry Run) - จะไม่เขียนไฟล์จริง\n")
    else:
        print("🚀 อัปเดต Platform URLs\n")

    # โหลด platform URLs
    platform_urls = load_platform_urls()

    if not platform_urls:
        print("❌ ไม่มีข้อมูล platform URLs ในไฟล์")
        sys.exit(1)

    print(f"📚 พบ {len(platform_urls)} รายการนิยาย\n")

    # อัปเดตแต่ละเรื่อง
    updated_count = 0
    skipped_count = 0

    for novel_dir, data in platform_urls.items():
        slug = data.get('slug')
        if not slug:
            print(f"⚠️  {novel_dir}: ไม่มี slug (ข้าม)")
            skipped_count += 1
            continue

        if update_novel_file(slug, data, dry_run):
            updated_count += 1
        else:
            skipped_count += 1

    # สรุปผล
    print(f"\n{'='*50}")
    if dry_run:
        print(f"🔍 ผลการทดสอบ:")
    else:
        print(f"✅ เสร็จสิ้น:")
    print(f"   - อัปเดต: {updated_count} เรื่อง")
    print(f"   - ข้าม: {skipped_count} เรื่อง")
    print(f"{'='*50}\n")

    if dry_run:
        print("💡 รันจริงโดยไม่ต้องใส่ --dry-run:")
        print("   python scripts/update-platform-urls.py\n")

if __name__ == "__main__":
    main()
