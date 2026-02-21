#!/usr/bin/env python3
"""
Parse Novel Metadata Script
อ่าน template files จากโฟลเดอร์นิยาย แล้วแปลงเป็น JSON สำหรับเว็บ
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
NOVELS_DIR = PROJECT_ROOT / "novels"
NOVELS_NC_DIR = PROJECT_ROOT / "novels-nc"
PLATFORM_URLS_FILE = PROJECT_ROOT / "novel-platform-urls.json"

def load_platform_urls():
    """โหลด platform URLs"""
    if not PLATFORM_URLS_FILE.exists():
        return {}

    with open(PLATFORM_URLS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return {k: v for k, v in data.items() if not k.startswith('_')}

def extract_title_info(novel_dir):
    """อ่านไฟล์ชื่อเรื่อง (01-ชื่อเรื่อง*.txt)"""
    # รองรับหลายรูปแบบ: 01-ชื่อเรื่อง.txt, 01-ชื่อเรื่อง-template.txt, 01-ชื่อเรื่อง-nc.txt
    title_files = (
        list(novel_dir.glob("01-ชื่อเรื่อง.txt")) +
        list(novel_dir.glob("01-ชื่อเรื่อง-*.txt"))
    )

    if not title_files:
        return None

    with open(title_files[0], 'r', encoding='utf-8') as f:
        content = f.read()

    result = {
        'title': '',
        'titleEn': '',
        'subtitle': '',
        'logline': ''
    }

    # Parse content - ยืดหยุ่นกับรูปแบบต่างๆ
    lines = content.strip().split('\n')
    for line in lines:
        # ลบช่องว่างและตัวอักษรพิเศษออก แล้วเช็คว่ามี : ไหม
        line = line.strip()
        if not line or ':' not in line:
            continue

        # ลบช่องว่างซ้ำและตัวอักษรตกแต่ง
        line = re.sub(r'\s+', ' ', line)

        # แยก key:value
        parts = line.split(':', 1)
        if len(parts) != 2:
            continue

        key = parts[0].strip()
        value = parts[1].strip()

        # ลบวงเล็บออกจาก key เช่น "ชื่อเรื่อง (ไทย)" → "ชื่อเรื่อง"
        key_clean = re.sub(r'\s*\([^)]*\)', '', key).strip()

        if key_clean in ['ชื่อนิยาย', 'ชื่อเรื่อง', 'ชื่อย่อ'] and not result['title']:
            result['title'] = value
        elif key_clean in ['ชื่ออังกฤษ', 'Title', 'English Title'] and not result['titleEn']:
            result['titleEn'] = value
        elif key_clean in ['ซับไตเติล', 'Subtitle'] and not result['subtitle']:
            result['subtitle'] = value
        elif key in ['Logline', 'คำโปรย'] and not result['logline']:
            result['logline'] = value

    return result if result['title'] else None

def extract_synopsis(novel_dir):
    """อ่านเรื่องย่อ (04-เรื่องย่อ*.txt)"""
    synopsis_files = (
        list(novel_dir.glob("04-เรื่องย่อ.txt")) +
        list(novel_dir.glob("04-เรื่องย่อ-*.txt"))
    )

    if not synopsis_files:
        return ""

    with open(synopsis_files[0], 'r', encoding='utf-8') as f:
        content = f.read().strip()

    # ลบหัวข้อและ decoration lines
    content = re.sub(r'^═+\s*$', '', content, flags=re.MULTILINE)  # ลบ ═══
    content = re.sub(r'^─+\s*$', '', content, flags=re.MULTILINE)  # ลบ ───
    content = re.sub(r'^┌.*┐\s*$', '', content, flags=re.MULTILINE)  # ลบกรอบบน
    content = re.sub(r'^└.*┘\s*$', '', content, flags=re.MULTILINE)  # ลบกรอบล่าง
    content = re.sub(r'^│.*│\s*$', '', content, flags=re.MULTILINE)  # ลบกรอบข้าง
    content = re.sub(r'^เรื่องย่อ:?\s*\n?', '', content, flags=re.MULTILINE)
    content = re.sub(r'".*?"', '', content)  # ลบชื่อเรื่องในเครื่องหมายคำพูด

    # ลบบรรทัดที่มีแต่ช่องว่างหรือสั้นเกินไป
    lines = [line.strip() for line in content.split('\n') if line.strip() and len(line.strip()) > 5]
    content = '\n\n'.join(lines)  # ใช้ double newline คั่นพารากราฟ

    return content.strip()

def extract_characters(novel_dir):
    """อ่านข้อมูลตัวละคร (03-ตัวละคร*.txt)"""
    char_files = (
        list(novel_dir.glob("03-ตัวละคร.txt")) +
        list(novel_dir.glob("03-ตัวละคร-*.txt"))
    )

    if not char_files:
        return []

    with open(char_files[0], 'r', encoding='utf-8') as f:
        content = f.read()

    characters = []

    # ลบ decoration lines ออกก่อน
    content = re.sub(r'^[═─━┃┏┓┗┛]+\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^│.*│\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^┃.*┃\s*$', '', content, flags=re.MULTILINE)

    # แยกตัวละครตาม section headers เช่น "พระเอก:", "นางเอก:"
    sections = re.split(r'(?:พระเอก|นางเอก|ตัวประกอบ|ตัวละครรอง)\s*:\s*([^\n]+)', content)

    current_char = {}
    for section in sections:
        lines = section.strip().split('\n')

        for line in lines:
            line = line.strip()
            if not line or len(line) < 3:
                continue

            # หา key: value pattern
            if ':' in line:
                parts = line.split(':', 1)
                key = parts[0].strip()
                value = parts[1].strip() if len(parts) > 1 else ''

                # ลบช่องว่างซ้ำและตัวอักษรตกแต่ง
                key = re.sub(r'\s+', ' ', key)

                # แปลง key
                if any(k in key for k in ['ชื่อเล่น', 'ชื่อ', 'Name']):
                    if 'name' not in current_char or not current_char.get('name'):
                        current_char['name'] = value
                elif any(k in key for k in ['อายุ', 'Age']):
                    try:
                        age_str = re.search(r'\d+', value)
                        current_char['age'] = int(age_str.group()) if age_str else 25
                    except:
                        current_char['age'] = 25
                elif any(k in key for k in ['อาชีพ', 'Occupation']):
                    current_char['role'] = value
                elif any(k in key for k in ['นิสัย', 'Personality', 'ลักษณะ']):
                    current_char['description'] = value

        # ถ้ามี name ให้เพิ่มตัวละคร
        if current_char.get('name'):
            if 'role' not in current_char:
                current_char['role'] = ''
            if 'age' not in current_char:
                current_char['age'] = 25
            if 'description' not in current_char:
                current_char['description'] = ''
            if 'quote' not in current_char:
                current_char['quote'] = ''

            characters.append(current_char)
            current_char = {}

    return characters[:4]  # เอาแค่ 4 ตัวละครแรก

def extract_hooks(novel_dir):
    """อ่านคำโปรย/จุดเด่น (05-คำโปรย*.txt)"""
    hook_files = (
        list(novel_dir.glob("05-คำโปรย.txt")) +
        list(novel_dir.glob("05-คำโปรย-*.txt"))
    )

    if not hook_files:
        return []

    with open(hook_files[0], 'r', encoding='utf-8') as f:
        content = f.read()

    hooks = []

    # ลบ decoration lines
    content = re.sub(r'^═+\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^─+\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^┌.*┐\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^└.*┘\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^│.*│\s*$', '', content, flags=re.MULTILINE)

    # ลบหัวข้อ
    content = re.sub(r'^(คำโปรย|จุดเด่น):?\s*\n?', '', content, flags=re.MULTILINE)
    content = re.sub(r'".*?"', '', content)  # ลบชื่อเรื่องในเครื่องหมายคำพูด

    # แยกตาม bullet points หรือเลขข้อ
    lines = content.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line or len(line) < 10:  # ข้ามบรรทัดสั้นเกินไป
            continue

        # ลบ bullet points/เลขข้อ
        line = re.sub(r'^[\-\*\d\.]+\s*', '', line)

        if line and len(line) >= 10:  # เอาแค่ที่มีความยาวพอ
            hooks.append(line)

    return hooks[:5]  # เอาแค่ 5 ข้อแรก

def generate_slug(title):
    """สร้าง slug จากชื่อไทย (ใช้ romanization เบื้องต้น)"""
    # ตารางแปลงเบื้องต้น
    thai_to_roman = {
        'ก': 'k', 'ข': 'kh', 'ค': 'kh', 'ง': 'ng',
        'จ': 'j', 'ฉ': 'ch', 'ช': 'ch', 'ซ': 's', 'ฌ': 'ch', 'ญ': 'y',
        'ฎ': 'd', 'ฏ': 't', 'ฐ': 'th', 'ฑ': 'th', 'ฒ': 'th', 'ณ': 'n',
        'ด': 'd', 'ต': 't', 'ถ': 'th', 'ท': 'th', 'ธ': 'th', 'น': 'n',
        'บ': 'b', 'ป': 'p', 'ผ': 'ph', 'ฝ': 'f', 'พ': 'ph', 'ฟ': 'f', 'ภ': 'ph', 'ม': 'm',
        'ย': 'y', 'ร': 'r', 'ล': 'l', 'ว': 'w',
        'ศ': 's', 'ษ': 's', 'ส': 's', 'ห': 'h', 'ฬ': 'l', 'อ': 'o', 'ฮ': 'h',
        'ะ': 'a', 'ั': 'a', 'า': 'a', 'ำ': 'am',
        'ิ': 'i', 'ี': 'i', 'ึ': 'ue', 'ื': 'ue', 'ุ': 'u', 'ู': 'u',
        'เ': 'e', 'แ': 'ae', 'โ': 'o', 'ใ': 'ai', 'ไ': 'ai',
        '็': '', '่': '', '้': '', '๊': '', '๋': '', '์': '', '์': '',
        ' ': '-', '-': '-',
    }

    slug = title.lower()
    result = []

    for char in slug:
        if char in thai_to_roman:
            result.append(thai_to_roman[char])
        elif char.isalnum() or char == '-':
            result.append(char)

    slug = ''.join(result)
    slug = re.sub(r'-+', '-', slug)  # ลบ - ซ้ำ
    slug = slug.strip('-')  # ลบ - ข้างหน้า/หลัง

    return slug if slug else 'untitled'

def get_genre_from_folder(folder_name):
    """กำหนด genre จากชื่อโฟลเดอร์หรือเนื้อหา"""
    folder_lower = folder_name.lower()

    genres = ["Romance"]

    if 'ceo' in folder_lower or 'ประธาน' in folder_name:
        genres.append("CEO")
    if 'มาเฟีย' in folder_name:
        genres.append("Mafia")
    if 'nc' in folder_lower or folder_name.startswith('novels-nc'):
        genres.append("Adult")

    return genres

def count_chapters(novel_dir):
    """นับจำนวนตอน"""
    chapter_files = list(novel_dir.glob("ตอนที่*.txt"))
    return len(chapter_files)

def parse_novel(novel_dir, platform_urls_data):
    """Parse ข้อมูลนิยาย 1 เรื่อง"""

    # สร้าง key สำหรับหา platform URLs
    relative_path = str(novel_dir.relative_to(PROJECT_ROOT))
    platform_data = platform_urls_data.get(relative_path, {})

    # อ่านข้อมูลจาก template files
    title_info = extract_title_info(novel_dir)

    if not title_info:
        return None  # ไม่มีไฟล์ชื่อเรื่อง ข้าม

    synopsis = extract_synopsis(novel_dir)
    characters = extract_characters(novel_dir)
    hooks = extract_hooks(novel_dir)
    total_chapters = count_chapters(novel_dir)

    # สร้าง slug
    slug = platform_data.get('slug') or generate_slug(title_info['title'])

    # กำหนด genre
    genres = get_genre_from_folder(novel_dir.name)

    # สร้าง tags
    tags = [title_info['title'], "นิยายรัก"] + genres

    # สร้าง novel object
    novel = {
        "slug": slug,
        "title": title_info['title'],
        "titleEn": title_info['titleEn'] or title_info['title'],
        "subtitle": title_info['subtitle'],
        "author": "ผู้เขียน",  # Default author
        "genre": genres,
        "rating": "18+" if 'novels-nc' in relative_path else "13+",
        "intensity": 7 if 'novels-nc' in relative_path else 5,
        "totalChapters": total_chapters if total_chapters > 0 else 50,
        "freeChapters": 10,
        "status": "กำลังเขียน" if total_chapters < 50 else "จบแล้ว",
        "coverImage": f"/images/novels/{slug}/cover.jpg",
        "logline": title_info['logline'] or synopsis[:200] + "...",
        "synopsis": synopsis or "เรื่องย่อจะเพิ่มเติมในภายหลัง",
        "characters": characters,
        "hooks": hooks if hooks else ["เรื่องราวที่น่าติดตาม"],
        "tags": tags,
        "publishedAt": datetime.now().strftime("%Y-%m-%d"),
        "updatedAt": datetime.now().strftime("%Y-%m-%d"),
        # Multi-platform support
        "platforms": list(platform_data.get('platforms', {}).keys()),
        "platformUrls": platform_data.get('platforms', {}),
        "primaryPlatform": platform_data.get('primaryPlatform', ''),
        # Legacy fields
        "platform": platform_data.get('primaryPlatform', '') or "Tunwalai",
        "platformUrl": ""
    }

    return novel

def main():
    """Main function"""
    print("🚀 Parse Novel Metadata\n")

    # โหลด platform URLs
    platform_urls = load_platform_urls()

    # รวมโฟลเดอร์นิยายทั้งหมด
    novel_folders = []

    # จาก /novels/
    if NOVELS_DIR.exists():
        for folder in sorted(NOVELS_DIR.iterdir()):
            if folder.is_dir() and folder.name != 'templates':
                novel_folders.append(('novels', folder))

    # จาก /novels-nc/
    if NOVELS_NC_DIR.exists():
        for folder in sorted(NOVELS_NC_DIR.iterdir()):
            if folder.is_dir() and folder.name not in ['templates', 'nc-automation', 'nc-server-setup', '1-ตัวอย่างนิยายNC']:
                novel_folders.append(('novels-nc', folder))

    if not novel_folders:
        print("❌ ไม่พบโฟลเดอร์นิยาย")
        sys.exit(1)

    print(f"📚 พบนิยาย {len(novel_folders)} เรื่อง\n")

    # Parse แต่ละเรื่อง
    parsed_novels = []
    success_count = 0
    error_count = 0

    for category, folder in novel_folders:
        try:
            novel_data = parse_novel(folder, platform_urls)

            if novel_data:
                parsed_novels.append(novel_data)
                print(f"  ✅ {novel_data['title']} ({novel_data['slug']})")
                success_count += 1
            else:
                print(f"  ⚠️  {folder.name}: ไม่มีข้อมูลชื่อเรื่อง (ข้าม)")
                error_count += 1

        except Exception as e:
            print(f"  ❌ {folder.name}: Error - {e}")
            error_count += 1

    # สรุปผล
    print(f"\n{'='*60}")
    print(f"✅ เสร็จสิ้น:")
    print(f"   - Parse สำเร็จ: {success_count} เรื่อง")
    print(f"   - Error/ข้าม: {error_count} เรื่อง")
    print(f"{'='*60}\n")

    # บันทึกผลลง JSON (optional)
    if parsed_novels:
        output_file = PROJECT_ROOT / "parsed-novels.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(parsed_novels, f, ensure_ascii=False, indent=2)
        print(f"💾 บันทึกผลลัพธ์ไว้ที่: {output_file}\n")

    return parsed_novels

if __name__ == "__main__":
    main()
