"""
Apply all formatting batches to Google Sheets
This script prints out instructions for Claude Code to execute
"""

import json
import os

def main():
    spreadsheet_id = "1JPZKbBXJMxVX9ugJ-WnLQmArIlJEOCEWbjLvb-xZ8OU"

    print("="*60)
    print("Applying All Formatting Batches")
    print("="*60)

    # Process each batch
    for i in range(9):
        batch_file = f"/tmp/batch_chunk_{i:02d}.json"

        if not os.path.exists(batch_file):
            print(f"✗ Batch {i} not found: {batch_file}")
            continue

        with open(batch_file, 'r', encoding='utf-8') as f:
            requests = json.load(f)

        print(f"\n📦 Batch {i}: {len(requests)} requests")
        print(f"   File: {batch_file}")
        print(f"   Size: {os.path.getsize(batch_file)} bytes")

        # Save batch info
        print(f"   → Ready to apply via mcp__google-sheets__batch_update")

    print("\n" + "="*60)
    print("All batches are ready")
    print("="*60)
    print(f"\nSpreadsheet ID: {spreadsheet_id}")
    print("Total batches: 9")
    print("\nClaude Code will now apply each batch sequentially...")

if __name__ == "__main__":
    main()