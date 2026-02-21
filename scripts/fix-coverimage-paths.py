#!/usr/bin/env python3
"""
Fix Cover Image Paths Script
อัปเดต coverImage paths ใน JSON ให้ใช้ slug แทนชื่อไทย
"""

import json
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
NOVELS_DIR = PROJECT_ROOT / "novel-promo-site" / "src" / "content" / "novels"

def main():
    """Main function"""
    print("🚀 แก้ไข coverImage paths ให้ใช้ slug\n")

    updated_count = 0

    # วนลูปทุกไฟล์ JSON
    for json_file in NOVELS_DIR.glob("*.json"):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # เช็คว่า coverImage มีชื่อไทยไหม
        cover_path = data.get('coverImage', '')
        slug = data.get('slug', '')

        # ถ้า coverImage ไม่ใช่ slug-based path
        if cover_path and slug:
            # Expected path should be: /images/novels/{slug}/cover.{ext}
            expected_prefix = f"/images/novels/{slug}/"

            if not cover_path.startswith(expected_prefix):
                # Extract extension from current path
                ext = Path(cover_path).suffix  # .jpg or .png

                # Update to slug-based path
                new_path = f"/images/novels/{slug}/cover{ext}"

                print(f"  📝 {json_file.name}")
                print(f"     เดิม: {cover_path}")
                print(f"     ใหม่: {new_path}")

                data['coverImage'] = new_path

                # เขียนกลับ
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)

                updated_count += 1

    # สรุปผล
    print(f"\n{'='*60}")
    print(f"✅ เสร็จสิ้น:")
    print(f"   - อัปเดต: {updated_count} ไฟล์")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
