"""
Novel Factory - Google Sheets Setup Script
สร้าง tracking spreadsheet พร้อม MASTER, WEEKLY, ANALYTICS sheets
"""

import json
import os
import sys
from typing import Dict, List

import config
import formatting_helpers as fmt

# MCP tools will be available via claude code environment
# We'll reference them as functions


def load_novels_data() -> Dict:
    """Load novels data from JSON file"""
    data_file = os.path.join(config.DATA_DIR, "novels_data.json")

    if not os.path.exists(data_file):
        print(f"Error: {data_file} not found!")
        print("Please run extract_novel_data.py first.")
        sys.exit(1)

    with open(data_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def create_spreadsheet(title: str = "Novel Factory - Tracking System") -> str:
    """
    Create new Google Spreadsheet

    Args:
        title: Spreadsheet title

    Returns:
        str: Spreadsheet ID
    """
    print(f"Creating spreadsheet: {title}")
    print("Please use MCP tool: mcp__google-sheets__create_spreadsheet")
    print(f'Title: "{title}"')
    print()
    print("After creating, please update SPREADSHEET_ID in config.py")
    return ""


def create_master_sheet_data(novels: List[Dict]) -> List[List]:
    """
    Create MASTER sheet data

    Args:
        novels: List of novel metadata dicts

    Returns:
        List[List]: 2D array for Google Sheets
    """
    # Header row
    data = [config.MASTER_COLUMNS]

    # Data rows
    for novel in novels:
        row = [
            novel["id"],
            novel["title"],
            novel["genre"],
            novel["chapters_written"],
            novel["chapters_target"],
            f"{novel['progress']:.0%}",
            novel["status"],
            novel.get("qc_score", ""),  # Empty if None
            novel["platforms"].get("ธัญวลัย", 0),
            novel["platforms"].get("readAwrite", 0),
            novel["platforms"].get("Dek-D", 0),
            novel["platforms"].get("Fictionlog", 0),
            novel["paywall"],
            novel.get("launch_date", ""),
            ", ".join(novel.get("tags", [])),
            novel.get("notes", "")
        ]
        data.append(row)

    return data


def create_weekly_sheet_template() -> List[List]:
    """
    Create WEEKLY sheet template

    Returns:
        List[List]: 2D array for Google Sheets
    """
    data = []

    # Title row
    data.append(["📅 งานสัปดาห์นี้ — วันที่ __/__/2026"])
    data.append([""])

    # Section 1: เปิดใหม่
    data.append(["⭐ เปิดเรื่องใหม่ (จัน / พุธ / ศุกร์)"])
    data.append(["วัน", "เรื่อง", "แพลตฟอร์ม", "ลงตอน", "กฎ", "เวลา", "✅"])
    data.append(["จันทร์", "", "", "", "Day1=5ตอน, Day2=5, แล้ววันละ1", "", ""])
    data.append(["พุธ", "", "", "", "Day1=5ตอน, Day2=5, แล้ววันละ1", "", ""])
    data.append(["ศุกร์", "", "", "", "Day1=5ตอน, Day2=5, แล้ววันละ1", "", ""])
    data.append([""])

    # Section 2: ลงประจำ
    data.append(["📤 ลงประจำ วันละ 1 ตอน"])
    data.append(["เรื่อง", "แพลตฟอร์ม", "จ", "อ", "พ", "พฤ", "ศ", "ส", "อา"])

    # Empty rows for data
    for _ in range(20):
        data.append(["", "", "", "", "", "", "", "", ""])

    return data


def create_analytics_sheet_template() -> List[List]:
    """
    Create ANALYTICS sheet template

    Returns:
        List[List]: 2D array for Google Sheets
    """
    data = []

    # Header
    data.append(config.ANALYTICS_COLUMNS)

    # Empty rows for data
    for _ in range(50):
        data.append([""] * len(config.ANALYTICS_COLUMNS))

    return data


def print_instructions():
    """Print setup instructions"""
    print("="*70)
    print("Novel Factory - Google Sheets Setup Instructions")
    print("="*70)
    print()
    print("Step 1: Create Spreadsheet")
    print("-" * 70)
    print("Use Claude Code MCP tool:")
    print('  mcp__google-sheets__create_spreadsheet')
    print('  title: "Novel Factory - Tracking System"')
    print()
    print("Step 2: Get Spreadsheet ID from result")
    print()
    print("Step 3: Update config.py with the Spreadsheet ID:")
    print('  SPREADSHEET_ID = "YOUR_SPREADSHEET_ID_HERE"')
    print()
    print("Step 4: Create sheets using the data generated below")
    print("="*70)
    print()


def generate_setup_data():
    """
    Generate setup data for manual Google Sheets creation

    This function generates the data needed to populate the sheets.
    Since we can't directly call MCP tools from Python, we'll output
    the instructions and data for manual setup via Claude Code.
    """
    # Load novels data
    novels_data = load_novels_data()
    novels = novels_data["novels"]

    print_instructions()

    # Generate MASTER sheet data
    master_data = create_master_sheet_data(novels)
    print("\n### MASTER Sheet Data ###")
    print(f"Total novels: {len(novels)}")
    print(f"Rows: {len(master_data)}")
    print(f"Columns: {len(config.MASTER_COLUMNS)}")
    print("\nFirst 5 rows preview:")
    for i, row in enumerate(master_data[:5]):
        print(f"Row {i+1}: {row[:5]}...")  # Show first 5 columns

    # Generate WEEKLY sheet template
    weekly_data = create_weekly_sheet_template()
    print("\n### WEEKLY Sheet Template ###")
    print(f"Rows: {len(weekly_data)}")

    # Generate ANALYTICS sheet template
    analytics_data = create_analytics_sheet_template()
    print("\n### ANALYTICS Sheet Template ###")
    print(f"Rows: {len(analytics_data)}")

    # Save data to JSON for easy loading
    output_data = {
        "master": master_data,
        "weekly": weekly_data,
        "analytics": analytics_data,
        "novels_count": len(novels)
    }

    output_file = os.path.join(config.DATA_DIR, "sheets_setup_data.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"\n✓ Setup data saved to: {output_file}")
    print("\nReady to create Google Sheets!")
    print("\nNext: Run this script with Claude Code to create the sheets.")


def main():
    """Main entry point"""
    generate_setup_data()


if __name__ == "__main__":
    main()
