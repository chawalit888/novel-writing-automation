#!/usr/bin/env python3
"""
Add Platform Templates Script
เพิ่ม platform templates (tunwalai, readawrite, dekd, fictionlog) ให้ทุกเรื่อง
"""

import json
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
PLATFORM_URLS_FILE = PROJECT_ROOT / "novel-platform-urls.json"

def main():
    """Main function"""
    print("🚀 เพิ่ม Platform Templates ให้ทุกเรื่อง\n")

    # โหลดไฟล์
    with open(PLATFORM_URLS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # นับจำนวนที่อัปเดต
    updated_count = 0

    # วนลูปทุก entry
    for key, value in data.items():
        # ข้าม metadata fields
        if key.startswith('_'):
            continue

        # เช็คว่ามี platforms หรือยัง
        if 'platforms' not in value or not value['platforms']:
            # สร้าง platforms object ใหม่
            value['platforms'] = {
                "tunwalai": "",
                "readawrite": "",
                "dekd": "",
                "fictionlog": ""
            }
            updated_count += 1
            print(f"  ✅ {value.get('folderName', key)}")
        else:
            # มี platforms อยู่แล้ว แต่เช็คว่ามีครบ 4 แพลตฟอร์มไหม
            platforms = value['platforms']
            updated = False

            # เพิ่มแพลตฟอร์มที่ยังไม่มี
            for platform in ["tunwalai", "readawrite", "dekd", "fictionlog"]:
                if platform not in platforms:
                    platforms[platform] = ""
                    updated = True

            if updated:
                updated_count += 1
                print(f"  ✅ {value.get('folderName', key)} (เพิ่มแพลตฟอร์มที่ขาด)")

    # บันทึกกลับ
    with open(PLATFORM_URLS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # สรุปผล
    print(f"\n{'='*60}")
    print(f"✅ เสร็จสิ้น:")
    print(f"   - อัปเดต: {updated_count} เรื่อง")
    print(f"   - ไฟล์: {PLATFORM_URLS_FILE.name}")
    print(f"{'='*60}\n")

    print("💡 ตอนนี้คุณสามารถกรอก URL ของแต่ละแพลตฟอร์มได้แล้ว")
    print("   ถ้าเรื่องไหนยังไม่ได้ลงให้ทิ้งไว้เป็น \"\" (ว่างเปล่า)\n")

if __name__ == "__main__":
    main()
