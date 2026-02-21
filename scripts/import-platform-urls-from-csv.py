#!/usr/bin/env python3
"""
Import Platform URLs from CSV Script
อ่าน CSV ที่กรอก URL แล้วอัปเดตลงใน novel-platform-urls.json
"""

import json
import csv
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
CSV_FILE = PROJECT_ROOT / "novel-platform-urls.csv"
JSON_FILE = PROJECT_ROOT / "novel-platform-urls.json"

def main():
    """Main function"""
    print("🚀 Import Platform URLs from CSV\n")

    if not CSV_FILE.exists():
        print("❌ ไม่พบไฟล์ novel-platform-urls.csv")
        print("   กรุณากรอก URL ในไฟล์ CSV ก่อน")
        return

    # Load JSON
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    # Create slug -> folder_path mapping
    slug_to_folder = {}
    for folder_path, info in json_data.items():
        if not folder_path.startswith('_'):
            slug = info.get('slug')
            if slug:
                slug_to_folder[slug] = folder_path

    # Read CSV
    updated_count = 0
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            slug = row['Slug']
            folder_path = slug_to_folder.get(slug)

            if not folder_path:
                print(f"  ⚠️  ไม่พบ slug: {slug}")
                continue

            # Get URLs from CSV
            tunwalai = row['Tunwalai'].strip()
            readawrite = row['ReadAWrite'].strip()
            dekd = row['Dek-D'].strip()
            fictionlog = row['Fictionlog'].strip()

            # Check if any URL was added
            platforms = json_data[folder_path]['platforms']
            changed = False

            if tunwalai and platforms.get('tunwalai') != tunwalai:
                platforms['tunwalai'] = tunwalai
                changed = True

            if readawrite and platforms.get('readawrite') != readawrite:
                platforms['readawrite'] = readawrite
                changed = True

            if dekd and platforms.get('dekd') != dekd:
                platforms['dekd'] = dekd
                changed = True

            if fictionlog and platforms.get('fictionlog') != fictionlog:
                platforms['fictionlog'] = fictionlog
                changed = True

            if changed:
                # Update primaryPlatform if not set
                if not json_data[folder_path].get('primaryPlatform'):
                    if tunwalai:
                        json_data[folder_path]['primaryPlatform'] = 'tunwalai'
                    elif readawrite:
                        json_data[folder_path]['primaryPlatform'] = 'readawrite'
                    elif dekd:
                        json_data[folder_path]['primaryPlatform'] = 'dekd'
                    elif fictionlog:
                        json_data[folder_path]['primaryPlatform'] = 'fictionlog'

                updated_count += 1
                print(f"  ✅ {row['ชื่อเรื่อง']}")

    # Save JSON
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    # Summary
    print(f"\n{'='*60}")
    print(f"✅ เสร็จสิ้น:")
    print(f"   - อัปเดต: {updated_count} เรื่อง")
    print(f"   - ไฟล์: novel-platform-urls.json")
    print(f"{'='*60}\n")

    if updated_count > 0:
        print("💡 ขั้นตอนต่อไป:")
        print("   1. รัน: python scripts/update-platform-urls.py")
        print("   2. เพื่ออัปเดต URL ลงในไฟล์ JSON ของนิยายแต่ละเรื่อง")
        print()

if __name__ == "__main__":
    main()
