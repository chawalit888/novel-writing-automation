"""
Regenerate formatting requests with correct sheet IDs
Fixes the bug where sequential sheet IDs (0,1,2,3...) were used instead of actual IDs
"""

import json
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from formatting_helpers import hex_to_rgb

def main():
    """Regenerate all formatting requests with correct sheet IDs"""

    print("\n" + "="*60)
    print("Regenerating Formatting Requests with Correct Sheet IDs")
    print("="*60)

    # Load sheet IDs mapping
    sheet_ids_file = "/tmp/story_sheet_ids.json"
    with open(sheet_ids_file, 'r', encoding='utf-8') as f:
        sheet_ids = json.load(f)

    print(f"\n✓ Loaded {len(sheet_ids)} sheet IDs")

    # Load novels data
    data_file = os.path.join(
        os.path.dirname(__file__),
        'data',
        'novels_data.json'
    )

    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    novels = data['novels']
    print(f"✓ Loaded {len(novels)} novels data")

    # Generate formatting requests for each novel
    all_requests = []

    for idx, novel in enumerate(novels, start=1):
        # Try exact match first
        sheet_title = f"📖 {novel['title'][:25]}"

        if sheet_title in sheet_ids:
            sheet_id = sheet_ids[sheet_title]
        else:
            # Try partial match (sheet titles may be truncated)
            sheet_id = None
            for key in sheet_ids.keys():
                # Match by prefix (first 20 chars after 📖)
                novel_prefix = novel['title'][:20]
                if key.startswith(f"📖 {novel_prefix}"):
                    sheet_id = sheet_ids[key]
                    sheet_title = key
                    break

            if sheet_id is None:
                print(f"⚠️  Sheet not found: {sheet_title}")
                print(f"     Novel title: {novel['title']}")
                continue
        chapters_written = novel['chapters_written']
        chapters_target = novel['chapters_target']

        print(f"\n{idx:2d}. {novel['title']}")
        print(f"    Sheet ID: {sheet_id}")
        print(f"    Written: {chapters_written}/{chapters_target}")

        # Generate requests for this novel
        requests = generate_written_chapter_requests(
            sheet_id=sheet_id,
            chapters_written=chapters_written,
            chapters_target=chapters_target
        )

        all_requests.extend(requests)
        print(f"    Requests: {len(requests)}")

    print(f"\n{'='*60}")
    print(f"Total requests generated: {len(all_requests)}")
    print(f"{'='*60}")

    # Split into batches (200 requests per batch)
    batch_size = 200
    batches = []

    for i in range(0, len(all_requests), batch_size):
        batch = all_requests[i:i + batch_size]
        batches.append(batch)

    print(f"\nSplitting into {len(batches)} batches...")

    # Save batches
    for batch_idx, batch in enumerate(batches):
        batch_file = f"/tmp/corrected_batch_chunk_{batch_idx:02d}.json"

        with open(batch_file, 'w', encoding='utf-8') as f:
            json.dump(batch, f, ensure_ascii=False, indent=2)

        size_kb = os.path.getsize(batch_file) / 1024
        print(f"  ✓ Batch {batch_idx}: {len(batch)} requests ({size_kb:.1f} KB)")

    print(f"\n{'='*60}")
    print("✅ Formatting requests regenerated successfully!")
    print(f"{'='*60}")
    print(f"\nSaved {len(batches)} batch files to /tmp/")
    print("Ready to apply via mcp__google-sheets__batch_update")


def generate_written_chapter_requests(sheet_id, chapters_written, chapters_target):
    """Generate formatting requests for written chapters in one story sheet"""

    requests = []

    if chapters_written == 0:
        # No chapters written, no coloring needed
        return requests

    # For each platform row (rows 5-8 = indices 5-8)
    for row_idx, platform in enumerate(config.PLATFORMS, start=5):
        platform_rgb = hex_to_rgb(platform['color_hex'])

        # Calculate medium shade (60% base + 40% white)
        written_rgb = {
            "red": platform_rgb["red"] * 0.6 + 0.4,
            "green": platform_rgb["green"] * 0.6 + 0.4,
            "blue": platform_rgb["blue"] * 0.6 + 0.4
        }

        # Create request to color written chapters
        # Columns: D onwards (startColumnIndex=3)
        # Color chapters 1 to chapters_written
        request = {
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": row_idx,
                    "endRowIndex": row_idx + 1,
                    "startColumnIndex": 3,  # Column D (chapter 1)
                    "endColumnIndex": 3 + chapters_written
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": written_rgb
                    }
                },
                "fields": "userEnteredFormat.backgroundColor"
            }
        }

        requests.append(request)

    return requests


if __name__ == "__main__":
    main()
