#!/usr/bin/env python3
"""
Fix Image Folders Script
แก้ไขโฟลเดอร์รูปให้ใช้ slug แทนชื่อไทย และอัปเดต JSON
"""

import json
import shutil
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
PLATFORM_URLS_FILE = PROJECT_ROOT / "novel-platform-urls.json"
IMAGES_DIR = PROJECT_ROOT / "novel-promo-site" / "public" / "images" / "novels"
NOVELS_DIR = PROJECT_ROOT / "novel-promo-site" / "src" / "content" / "novels"

def load_platform_urls():
    """โหลด platform URLs"""
    with open(PLATFORM_URLS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return {k: v for k, v in data.items() if not k.startswith('_')}

def main():
    """Main function"""
    print("🚀 แก้ไขโฟลเดอร์รูปให้ใช้ slug\n")

    platform_urls = load_platform_urls()
    renamed_count = 0
    updated_json_count = 0

    for folder_path, data in platform_urls.items():
        slug = data.get('slug')
        folder_name = data.get('folderName')

        if not slug or not folder_name:
            continue

        # เช็คว่ามีโฟลเดอร์ชื่อไทยอยู่ไหม
        thai_folder = IMAGES_DIR / folder_name
        slug_folder = IMAGES_DIR / slug

        # ถ้ามีโฟลเดอร์ไทย และยังไม่มีโฟลเดอร์ slug
        if thai_folder.exists() and not slug_folder.exists():
            # Rename
            shutil.move(str(thai_folder), str(slug_folder))
            print(f"  ✅ Renamed: {folder_name} → {slug}")
            renamed_count += 1

        # อัปเดต JSON ของนิยาย
        novel_json = NOVELS_DIR / f"{slug}.json"

        if novel_json.exists():
            with open(novel_json, 'r', encoding='utf-8') as f:
                novel_data = json.load(f)

            # เช็คว่ามีรูปในโฟลเดอร์ไหม
            if slug_folder.exists():
                # หา cover.jpg หรือ cover.png
                cover_jpg = slug_folder / "cover.jpg"
                cover_png = slug_folder / "cover.png"

                if cover_jpg.exists():
                    ext = ".jpg"
                elif cover_png.exists():
                    ext = ".png"
                else:
                    continue

                # อัปเดต path
                new_path = f"/images/novels/{slug}/cover{ext}"
                old_path = novel_data.get('coverImage', '')

                if old_path != new_path:
                    novel_data['coverImage'] = new_path

                    # เขียนกลับ
                    with open(novel_json, 'w', encoding='utf-8') as f:
                        json.dump(novel_data, f, ensure_ascii=False, indent=2)

                    print(f"     📝 Updated JSON: {slug}")
                    updated_json_count += 1

    # สรุปผล
    print(f"\n{'='*60}")
    print(f"✅ เสร็จสิ้น:")
    print(f"   - Rename โฟลเดอร์: {renamed_count} โฟลเดอร์")
    print(f"   - อัปเดต JSON: {updated_json_count} ไฟล์")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
