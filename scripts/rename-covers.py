#!/usr/bin/env python3
"""
Rename Cover Images Script
เปลี่ยนชื่อรูปปกทั้งหมดเป็น cover.jpg อัตโนมัติ
"""

import os
import sys
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
IMAGES_DIR = PROJECT_ROOT / "novel-promo-site" / "public" / "images" / "novels"

def rename_covers(dry_run=False):
    """เปลี่ยนชื่อรูปปกทั้งหมดเป็น cover.jpg"""

    if not IMAGES_DIR.exists():
        print(f"❌ ไม่พบโฟลเดอร์: {IMAGES_DIR}")
        sys.exit(1)

    print(f"📂 สแกนโฟลเดอร์: {IMAGES_DIR}\n")

    renamed_count = 0
    skipped_count = 0
    error_count = 0

    # วนลูปทุกโฟลเดอร์ย่อย
    for novel_folder in sorted(IMAGES_DIR.iterdir()):
        if not novel_folder.is_dir():
            continue

        # หารูปภาพในโฟลเดอร์ (jpg, png, jpeg, webp)
        image_files = list(novel_folder.glob('*.jpg')) + \
                     list(novel_folder.glob('*.png')) + \
                     list(novel_folder.glob('*.jpeg')) + \
                     list(novel_folder.glob('*.webp'))

        if not image_files:
            print(f"  ⚠️  {novel_folder.name}/ - ไม่มีรูปภาพ")
            skipped_count += 1
            continue

        # ถ้ามีหลายรูป เตือน
        if len(image_files) > 1:
            print(f"  ⚠️  {novel_folder.name}/ - มี {len(image_files)} รูป (จะใช้รูปแรก)")

        # เอารูปแรก
        original_file = image_files[0]
        original_ext = original_file.suffix.lower()

        # ถ้าชื่อเป็น cover.* อยู่แล้ว
        if original_file.stem == 'cover':
            print(f"  ✅ {novel_folder.name}/ - มี cover{original_ext} อยู่แล้ว")
            skipped_count += 1
            continue

        # เปลี่ยนชื่อเป็น cover.jpg (หรือ cover.png ถ้าเป็น PNG)
        # ใช้ extension เดิม
        new_filename = f"cover{original_ext}"
        new_file = novel_folder / new_filename

        if dry_run:
            print(f"  🔍 {novel_folder.name}/")
            print(f"     {original_file.name} → {new_filename}")
            renamed_count += 1
        else:
            try:
                # Rename
                original_file.rename(new_file)
                print(f"  ✅ {novel_folder.name}/")
                print(f"     {original_file.name} → {new_filename}")
                renamed_count += 1

                # ลบรูปอื่นๆ ที่เหลือ (ถ้ามี)
                if len(image_files) > 1:
                    for extra_file in image_files[1:]:
                        extra_file.unlink()
                        print(f"     🗑️  ลบ: {extra_file.name}")

            except Exception as e:
                print(f"  ❌ {novel_folder.name}/ - เกิดข้อผิดพลาด: {e}")
                error_count += 1

    # สรุปผล
    print(f"\n{'='*60}")
    if dry_run:
        print(f"🔍 ผลการทดสอบ:")
    else:
        print(f"✅ เสร็จสิ้น:")
    print(f"   - เปลี่ยนชื่อ: {renamed_count} ไฟล์")
    print(f"   - ข้าม: {skipped_count} โฟลเดอร์")
    if error_count > 0:
        print(f"   - ข้อผิดพลาด: {error_count} ไฟล์")
    print(f"{'='*60}\n")

    if dry_run:
        print("💡 รันจริงโดยไม่ต้องใส่ --dry-run:")
        print("   python scripts/rename-covers.py\n")

def main():
    """Main function"""
    # เช็ค arguments
    dry_run = '--dry-run' in sys.argv or '-n' in sys.argv

    if dry_run:
        print("🔍 โหมดทดสอบ (Dry Run) - จะไม่เปลี่ยนชื่อจริง\n")
    else:
        print("🚀 เปลี่ยนชื่อรูปปกเป็น cover.jpg\n")

    rename_covers(dry_run)

if __name__ == "__main__":
    main()
