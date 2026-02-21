#!/usr/bin/env python3
"""
Add Thai Folder Names Script
เพิ่ม folderName (ชื่อภาษาไทย) ลงใน novel-platform-urls.json
"""

import json
import re
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
PLATFORM_URLS_FILE = PROJECT_ROOT / "novel-platform-urls.json"

def extract_folder_name(directory_path):
    """
    แยกชื่อโฟลเดอร์ภาษาไทยจาก path
    เช่น "novels/1-ท่านประธานหัวใจไลฟ์สด" → "ท่านประธานหัวใจไลฟ์สด"
    หรือ "novels-nc/2. สวาทลับคุณหนูมาเฟีย" → "สวาทลับคุณหนูมาเฟีย"
    """
    # ดึงชื่อโฟลเดอร์สุดท้าย (หลัง /)
    folder = directory_path.split('/')[-1]

    # ตัดเลขข้างหน้าออก (รูปแบบ: "1-", "10-", "2. ", "14. ")
    # Pattern: เลข + (ขีด หรือ จุด+ช่องว่าง) ตามด้วยชื่อเรื่อง
    cleaned = re.sub(r'^\d+[-.\s]+', '', folder)

    return cleaned.strip()

def main():
    """Main function"""
    print("🚀 เพิ่มชื่อโฟลเดอร์ภาษาไทยลง novel-platform-urls.json\n")

    # โหลดไฟล์เดิม
    with open(PLATFORM_URLS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # อัพเดตแต่ละ entry
    updated_count = 0
    for key, value in data.items():
        # ข้าม metadata entries
        if key.startswith('_'):
            continue

        # เพิ่ม folderName
        folder_name = extract_folder_name(key)
        value['folderName'] = folder_name
        updated_count += 1
        print(f"  ✅ {key}")
        print(f"     → folderName: {folder_name}")

    # เขียนกลับลงไฟล์
    with open(PLATFORM_URLS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print(f"✅ เพิ่ม folderName สำเร็จ: {updated_count} เรื่อง")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
