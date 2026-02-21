#!/usr/bin/env python3
"""
Update Cover Image Paths Script
อัพเดท path รูปปกในไฟล์ novel JSON ให้ใช้โฟลเดอร์ภาษาไทย
"""

import json
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
PLATFORM_URLS_FILE = PROJECT_ROOT / "novel-platform-urls.json"
NOVELS_DIR = PROJECT_ROOT / "novel-promo-site" / "src" / "content" / "novels"

def load_platform_urls():
    """โหลดไฟล์ novel-platform-urls.json"""
    with open(PLATFORM_URLS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return {k: v for k, v in data.items() if not k.startswith('_')}

def main():
    """Main function"""
    print("🚀 อัพเดท path รูปปกเป็นภาษาไทย\n")

    platform_urls = load_platform_urls()
    updated_count = 0
    skipped_count = 0

    for novel_dir, data in platform_urls.items():
        slug = data.get('slug')
        folder_name = data.get('folderName')

        if not slug or not folder_name:
            continue

        novel_file = NOVELS_DIR / f"{slug}.json"

        # ข้ามถ้าไม่มีไฟล์ (นิยายยังไม่ได้ซิงก์ขึ้นเว็บ)
        if not novel_file.exists():
            print(f"  ⚠️  {slug}.json ไม่พบ (ข้าม)")
            skipped_count += 1
            continue

        # อ่านไฟล์ JSON
        with open(novel_file, 'r', encoding='utf-8') as f:
            novel_data = json.load(f)

        # อัพเดท coverImage path
        old_path = novel_data.get('coverImage', '')
        new_path = f"/images/novels/{folder_name}/cover.jpg"

        if old_path == new_path:
            print(f"  ℹ️  {slug}: path ถูกต้องอยู่แล้ว")
            skipped_count += 1
            continue

        novel_data['coverImage'] = new_path

        # เขียนกลับลงไฟล์
        with open(novel_file, 'w', encoding='utf-8') as f:
            json.dump(novel_data, f, ensure_ascii=False, indent=2)

        print(f"  ✅ {slug}")
        print(f"     เดิม: {old_path}")
        print(f"     ใหม่: {new_path}")
        updated_count += 1

    # สรุปผล
    print(f"\n{'='*60}")
    print(f"✅ เสร็จสิ้น:")
    print(f"   - อัพเดต: {updated_count} ไฟล์")
    print(f"   - ข้าม: {skipped_count} ไฟล์")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
