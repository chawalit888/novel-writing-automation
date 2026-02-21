#!/usr/bin/env python3
"""
Update Cover Extensions Script
อัพเดท coverImage path ให้ตรงกับ extension จริง (.jpg หรือ .png)
"""

import json
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
PLATFORM_URLS_FILE = PROJECT_ROOT / "novel-platform-urls.json"
NOVELS_DIR = PROJECT_ROOT / "novel-promo-site" / "src" / "content" / "novels"
IMAGES_DIR = PROJECT_ROOT / "novel-promo-site" / "public" / "images" / "novels"

def load_platform_urls():
    """โหลดไฟล์ novel-platform-urls.json"""
    with open(PLATFORM_URLS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return {k: v for k, v in data.items() if not k.startswith('_')}

def main():
    """Main function"""
    print("🚀 อัพเดท coverImage extension ให้ตรงกับไฟล์จริง\n")

    platform_urls = load_platform_urls()
    updated_count = 0
    skipped_count = 0

    for novel_dir, data in platform_urls.items():
        slug = data.get('slug')
        folder_name = data.get('folderName')

        if not slug or not folder_name:
            continue

        novel_file = NOVELS_DIR / f"{slug}.json"

        # ข้ามถ้าไม่มีไฟล์ JSON
        if not novel_file.exists():
            skipped_count += 1
            continue

        # เช็คว่ามีรูปอะไรในโฟลเดอร์บ้าง
        image_folder = IMAGES_DIR / folder_name
        if not image_folder.exists():
            print(f"  ⚠️  {slug}: ไม่พบโฟลเดอร์รูป (ข้าม)")
            skipped_count += 1
            continue

        # หา cover.jpg หรือ cover.png
        cover_jpg = image_folder / "cover.jpg"
        cover_png = image_folder / "cover.png"

        if cover_jpg.exists():
            cover_ext = ".jpg"
        elif cover_png.exists():
            cover_ext = ".png"
        else:
            print(f"  ⚠️  {slug}: ไม่พบ cover.jpg หรือ cover.png (ข้าม)")
            skipped_count += 1
            continue

        # อ่านไฟล์ JSON
        with open(novel_file, 'r', encoding='utf-8') as f:
            novel_data = json.load(f)

        # อัพเดท coverImage
        new_path = f"/images/novels/{folder_name}/cover{cover_ext}"
        old_path = novel_data.get('coverImage', '')

        if old_path == new_path:
            print(f"  ℹ️  {slug}: path ถูกต้องอยู่แล้ว")
            skipped_count += 1
            continue

        novel_data['coverImage'] = new_path

        # เขียนกลับ
        with open(novel_file, 'w', encoding='utf-8') as f:
            json.dump(novel_data, f, ensure_ascii=False, indent=2)

        print(f"  ✅ {slug}")
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
