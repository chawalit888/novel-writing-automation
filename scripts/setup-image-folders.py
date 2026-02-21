#!/usr/bin/env python3
"""
Setup Image Folders Script
สร้างโฟลเดอร์รูปภาพสำหรับนิยายทุกเรื่องตาม novel-platform-urls.json
"""

import json
import os
import sys
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
PLATFORM_URLS_FILE = PROJECT_ROOT / "novel-platform-urls.json"
IMAGES_DIR = PROJECT_ROOT / "novel-promo-site" / "public" / "images" / "novels"

def load_platform_urls():
    """โหลดไฟล์ novel-platform-urls.json"""
    if not PLATFORM_URLS_FILE.exists():
        print(f"❌ ไม่พบไฟล์: {PLATFORM_URLS_FILE}")
        sys.exit(1)

    with open(PLATFORM_URLS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # กรอง entry ที่ขึ้นต้นด้วย _ (metadata)
    return {k: v for k, v in data.items() if not k.startswith('_')}

def setup_folders(dry_run=False):
    """สร้างโฟลเดอร์รูปภาพสำหรับนิยายทุกเรื่อง"""
    platform_urls = load_platform_urls()

    if not platform_urls:
        print("❌ ไม่มีข้อมูลนิยายในไฟล์")
        sys.exit(1)

    print(f"📚 พบนิยาย {len(platform_urls)} เรื่อง\n")

    # ตรวจสอบว่ามีโฟลเดอร์ images/novels หรือยัง
    if not IMAGES_DIR.exists():
        if dry_run:
            print(f"🔍 จะสร้างโฟลเดอร์: {IMAGES_DIR}")
        else:
            IMAGES_DIR.mkdir(parents=True, exist_ok=True)
            print(f"✅ สร้างโฟลเดอร์: {IMAGES_DIR}\n")

    created_count = 0
    existing_count = 0

    for novel_dir, data in platform_urls.items():
        # ใช้ folderName (ภาษาไทย) แทน slug
        folder_name = data.get('folderName') or data.get('slug')
        if not folder_name:
            print(f"⚠️  {novel_dir}: ไม่มี folderName หรือ slug (ข้าม)")
            continue

        folder_path = IMAGES_DIR / folder_name

        if folder_path.exists():
            print(f"  📁 {folder_name}/ (มีอยู่แล้ว)")
            existing_count += 1
        else:
            if dry_run:
                print(f"  🔍 {folder_name}/ (จะสร้างใหม่)")
                created_count += 1
            else:
                folder_path.mkdir(parents=True, exist_ok=True)
                print(f"  ✅ {folder_name}/ (สร้างแล้ว)")
                created_count += 1

    # สรุปผล
    print(f"\n{'='*60}")
    if dry_run:
        print(f"🔍 ผลการทดสอบ:")
    else:
        print(f"✅ เสร็จสิ้น:")
    print(f"   - โฟลเดอร์ที่มีอยู่แล้ว: {existing_count} โฟลเดอร์")
    print(f"   - โฟลเดอร์ที่สร้างใหม่: {created_count} โฟลเดอร์")
    print(f"   - รวมทั้งหมด: {existing_count + created_count} โฟลเดอร์")
    print(f"{'='*60}\n")

    if dry_run:
        print("💡 รันจริงโดยไม่ต้องใส่ --dry-run:")
        print("   python scripts/setup-image-folders.py\n")
    else:
        print("📌 คำแนะนำ:")
        print("   1. ลากไฟล์รูป cover.jpg ไปใส่ในโฟลเดอร์ของแต่ละเรื่อง")
        print("   2. ทุกรูปต้องชื่อ 'cover.jpg' เหมือนกันหมด")
        print("   3. แนะนำขนาดรูป: 800x1200 pixels (อัตราส่วน 2:3)\n")

def main():
    """Main function"""
    # เช็ค arguments
    dry_run = '--dry-run' in sys.argv or '-n' in sys.argv

    if dry_run:
        print("🔍 โหมดทดสอบ (Dry Run) - จะไม่สร้างโฟลเดอร์จริง\n")
    else:
        print("🚀 สร้างโฟลเดอร์รูปภาพ\n")

    setup_folders(dry_run)

if __name__ == "__main__":
    main()
