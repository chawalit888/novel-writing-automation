"""
Novel Factory - Data Extraction Script
Scan นิยายทั้งหมดใน novels/ และ novels-nc/ แล้วสร้าง novels_data.json
"""

import os
import re
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

import config

def scan_novels_directory() -> List[Dict]:
    """
    Scan both novels/ and novels-nc/ directories

    Returns:
        List[Dict]: List of novel metadata
    """
    novels = []

    # Skip these directories
    skip_dirs = ['templates', 'nc-automation', 'nc-server-setup', '.git', '__pycache__']

    # Scan regular novels
    if os.path.exists(config.NOVELS_DIR):
        for item in sorted(os.listdir(config.NOVELS_DIR)):
            if item in skip_dirs or item.startswith('.') or item.endswith('.txt'):
                continue
            item_path = os.path.join(config.NOVELS_DIR, item)
            if os.path.isdir(item_path):
                novel_data = extract_novel_metadata(item_path, novel_type="regular")
                if novel_data:
                    novels.append(novel_data)
                    print(f"✓ Extracted: {novel_data['title']} ({novel_data['chapters_written']} ตอน)")

    # Scan NC novels
    if os.path.exists(config.NOVELS_NC_DIR):
        for item in sorted(os.listdir(config.NOVELS_NC_DIR)):
            if item in skip_dirs or item.startswith('.') or item.endswith('.txt'):
                continue
            item_path = os.path.join(config.NOVELS_NC_DIR, item)
            if os.path.isdir(item_path):
                novel_data = extract_novel_metadata(item_path, novel_type="nc")
                if novel_data:
                    novels.append(novel_data)
                    print(f"✓ Extracted: {novel_data['title']} ({novel_data['chapters_written']} ตอน) [NC]")

    return novels


def extract_novel_metadata(novel_path: str, novel_type: str = "regular") -> Optional[Dict]:
    """
    Extract metadata from a novel directory

    Args:
        novel_path: Path to novel directory
        novel_type: "regular" or "nc"

    Returns:
        Dict: Novel metadata or None if invalid
    """
    try:
        # Count chapters
        chapter_count, chapter_list = count_chapters(novel_path)

        # Don't skip - include even if no chapters written yet

        # Extract title
        title = extract_title(novel_path)
        if not title:
            # Fallback to directory name
            title = os.path.basename(novel_path)
            # Remove number prefix (e.g., "1. ชื่อเรื่อง" → "ชื่อเรื่อง")
            title = re.sub(r'^\d+\.\s*', '', title)

        # Parse genre and other metadata
        genre, nc_rating, paywall, target_chapters, tags = parse_title_file(novel_path)

        # Guess genre if not found
        if not genre:
            genre = guess_genre(title)

        # Default values
        if not target_chapters:
            target_chapters = 50  # Default

        if not paywall:
            paywall = config.PUBLISHING_RULES["paywall_start_default"]

        # Determine status based on chapter count
        status = determine_status(chapter_count, target_chapters)

        # Build metadata
        novel_data = {
            "id": None,  # Will be assigned later
            "title": title,
            "genre": genre,
            "type": novel_type,
            "chapters_written": chapter_count,
            "chapters_target": target_chapters,
            "progress": round(chapter_count / target_chapters, 2) if target_chapters > 0 else 0,
            "paywall": paywall,
            "nc_rating": nc_rating if novel_type == "nc" else None,
            "tags": tags,
            "path": novel_path,
            "status": status,
            "chapter_list": chapter_list,
            "platforms": {
                "ธัญวลัย": 0,
                "readAwrite": 0,
                "Dek-D": 0,
                "Fictionlog": 0
            },
            "qc_score": None,
            "launch_date": None,
            "notes": ""
        }

        return novel_data

    except Exception as e:
        print(f"Error extracting metadata from {novel_path}: {e}")
        return None


def count_chapters(novel_path: str) -> tuple:
    """
    Count chapter files (ตอนที่XX-*.txt)

    Args:
        novel_path: Path to novel directory

    Returns:
        tuple: (chapter_count, chapter_list)
    """
    chapter_pattern = re.compile(config.CHAPTER_PATTERN)
    chapters = []

    for filename in os.listdir(novel_path):
        match = chapter_pattern.match(filename)
        if match:
            chapter_num = int(match.group(1))
            chapters.append({
                "number": chapter_num,
                "filename": filename
            })

    chapters.sort(key=lambda x: x["number"])
    return len(chapters), chapters


def extract_title(novel_path: str) -> Optional[str]:
    """
    Extract title from directory name or 01-ชื่อเรื่อง-*.txt file

    Args:
        novel_path: Path to novel directory

    Returns:
        str: Title
    """
    # First, try to extract from directory name
    dir_name = os.path.basename(novel_path)
    # Remove number prefix (e.g., "1. ชื่อเรื่อง" → "ชื่อเรื่อง")
    title_from_dir = re.sub(r'^\d+[\.\s]*', '', dir_name).strip()

    # Try to read from title file
    for filename in os.listdir(novel_path):
        if filename.startswith(config.METADATA_FILES["title"]) and filename.endswith('.txt'):
            filepath = os.path.join(novel_path, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                    # Try to extract from "ชื่อเรื่อง (ไทย) : XXX" pattern
                    title_match = re.search(r'ชื่อเรื่อง\s*\(ไทย\)\s*[:：]\s*(.+)', content)
                    if title_match:
                        title = title_match.group(1).strip()
                        if title and len(title) > 0:
                            return title

                    # Fallback: try to find any line with actual Thai content
                    lines = content.split('\n')
                    for line in lines:
                        line = line.strip()
                        # Skip decoration lines and headers
                        if line and not all(c in '═─│┌┐└┘├┤┬┴┼ ' for c in line):
                            if 'ชื่อเรื่อง' not in line and 'แนวเรื่อง' not in line:
                                # Check if has Thai characters
                                if any('\u0E00' <= c <= '\u0E7F' for c in line):
                                    if len(line) > 3 and not line.startswith('#'):
                                        return line
            except Exception as e:
                print(f"Error reading title file {filepath}: {e}")

    # Fallback to directory name
    return title_from_dir if title_from_dir else "ไม่ระบุชื่อ"


def parse_title_file(novel_path: str) -> tuple:
    """
    Parse structured data from 01-ชื่อเรื่อง-*.txt file

    Args:
        novel_path: Path to novel directory

    Returns:
        tuple: (genre, nc_rating, paywall, target_chapters, tags)
    """
    genre = None
    nc_rating = None
    paywall = None
    target_chapters = None
    tags = []

    for filename in os.listdir(novel_path):
        if filename.startswith(config.METADATA_FILES["title"]) and filename.endswith('.txt'):
            filepath = os.path.join(novel_path, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                    # Extract genre
                    genre_match = re.search(r'แนว[:\s]*([^\n]+)', content)
                    if genre_match:
                        genre = genre_match.group(1).strip()

                    # Extract NC rating
                    for rating in config.NC_RATINGS:
                        if rating in content:
                            nc_rating = rating
                            tags.append(rating)
                            break

                    # Extract paywall
                    paywall_match = re.search(r'Paywall[:\s]*ตอน[ที่\s]*(\d+)', content, re.IGNORECASE)
                    if paywall_match:
                        paywall = int(paywall_match.group(1))

                    # Extract target chapters
                    target_match = re.search(r'(?:ตอนทั้งหมด|จำนวนตอน|Target)[:\s]*(\d+)', content, re.IGNORECASE)
                    if target_match:
                        target_chapters = int(target_match.group(1))

                    # Check for HIT tag
                    if '🔥' in content or 'HIT' in content:
                        tags.append('🔥')

            except Exception as e:
                print(f"Error parsing title file {filepath}: {e}")

    return genre, nc_rating, paywall, target_chapters, tags


def guess_genre(title: str) -> str:
    """
    Guess genre from title using keywords

    Args:
        title: Novel title

    Returns:
        str: Guessed genre
    """
    for genre, keywords in config.GENRE_KEYWORDS.items():
        for keyword in keywords:
            if keyword in title:
                return genre

    return "Romance"  # Default genre


def determine_status(chapters_written: int, chapters_target: int) -> str:
    """
    Determine status based on progress

    Args:
        chapters_written: Number of chapters written
        chapters_target: Target number of chapters

    Returns:
        str: Status
    """
    progress = chapters_written / chapters_target if chapters_target > 0 else 0

    if progress >= 1.0:
        return "ผลิตแล้ว"  # Written, ready to publish
    elif progress >= 0.8:
        return "กำลังผลิต"  # Almost done, still writing
    elif progress >= 0.5:
        return "กำลังผลิต"  # Halfway
    else:
        return "กำลังผลิต"  # Just started

    # Default
    return "กำลังผลิต"


def generate_novels_data() -> Dict:
    """
    Main function: scan all novels and generate JSON

    Returns:
        Dict: Complete novels data
    """
    print("="*60)
    print("Novel Factory - Data Extraction")
    print("="*60)
    print(f"Scanning: {config.NOVELS_DIR}")
    print(f"Scanning: {config.NOVELS_NC_DIR}")
    print()

    novels = scan_novels_directory()

    # Assign IDs
    for idx, novel in enumerate(novels, start=1):
        novel["id"] = idx

    # Summary
    total_chapters = sum(n["chapters_written"] for n in novels)
    regular_novels = [n for n in novels if n["type"] == "regular"]
    nc_novels = [n for n in novels if n["type"] == "nc"]

    print()
    print("="*60)
    print("Summary")
    print("="*60)
    print(f"Total novels: {len(novels)}")
    print(f"  Regular: {len(regular_novels)}")
    print(f"  NC: {len(nc_novels)}")
    print(f"Total chapters written: {total_chapters}")
    print(f"  Regular: {sum(n['chapters_written'] for n in regular_novels)}")
    print(f"  NC: {sum(n['chapters_written'] for n in nc_novels)}")
    print()

    # Build output data
    output_data = {
        "generated_at": datetime.now().isoformat(),
        "total_novels": len(novels),
        "total_chapters": total_chapters,
        "summary": {
            "regular": len(regular_novels),
            "nc": len(nc_novels),
            "chapters_regular": sum(n["chapters_written"] for n in regular_novels),
            "chapters_nc": sum(n["chapters_written"] for n in nc_novels)
        },
        "novels": novels
    }

    return output_data


def save_novels_data(output_data: Dict, output_file: str = None):
    """
    Save novels data to JSON file

    Args:
        output_data: Data to save
        output_file: Output file path (default: data/novels_data.json)
    """
    if not output_file:
        output_file = os.path.join(config.DATA_DIR, "novels_data.json")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"✓ Saved to: {output_file}")


def main():
    """Main entry point"""
    # Generate data
    output_data = generate_novels_data()

    # Save to JSON
    save_novels_data(output_data)

    print()
    print("✓ Data extraction complete!")
    print()


if __name__ == "__main__":
    main()
