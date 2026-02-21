"""
Get Sheet IDs for all story sheets
Uses MCP tools via subprocess to retrieve sheet metadata
"""

import json
import subprocess
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config

def main():
    """Get sheet IDs for all story sheets"""

    print("\n" + "="*60)
    print("Getting Sheet IDs from Google Sheets")
    print("="*60)

    spreadsheet_id = config.SPREADSHEET_ID

    # List all sheets
    print(f"\nSpreadsheet ID: {spreadsheet_id}")
    print("\nNote: This script needs to be called by Claude Code")
    print("Claude Code will use MCP tools to get sheet IDs")

    # Instructions for Claude Code
    print("\n" + "="*60)
    print("Instructions for Claude Code:")
    print("="*60)
    print("""
1. Use get_sheet_data with include_grid_data=false on each story sheet
2. Check the response for sheet ID information
3. Alternative: Use batch_update to query sheet properties
4. Create mapping: {sheet_title: sheet_id}
5. Save to /tmp/story_sheet_ids.json
    """)

    # Expected story sheets
    print("\n" + "="*60)
    print("Expected Story Sheets (24 total):")
    print("="*60)

    # Load novels data to get expected titles
    data_file = os.path.join(
        os.path.dirname(__file__),
        'data',
        'novels_data.json'
    )

    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    novels = data['novels']

    for idx, novel in enumerate(novels, start=1):
        sheet_title = f"📖 {novel['title'][:25]}"
        print(f"{idx:2d}. {sheet_title}")

    print(f"\nTotal: {len(novels)} story sheets")

if __name__ == "__main__":
    main()
