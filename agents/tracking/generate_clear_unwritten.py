"""
Generate batch to clear colors on unwritten chapters (set to white)
"""

import json
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config

def main():
    """Generate requests to clear colors on unwritten chapters"""

    print("\n" + "="*60)
    print("Generate Clear Unwritten Chapters Batch")
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

    # Generate clear requests for unwritten chapters
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
                continue

        chapters_written = novel['chapters_written']
        chapters_target = novel['chapters_target']

        # Only process novels with unwritten chapters
        if chapters_written >= chapters_target:
            # All chapters written, no need to clear
            continue

        print(f"\n{idx:2d}. {novel['title']}")
        print(f"    Sheet ID: {sheet_id}")
        print(f"    Written: {chapters_written}/{chapters_target}")
        print(f"    Unwritten: {chapters_target - chapters_written}")

        # Generate requests to clear unwritten chapters
        requests = generate_clear_requests(
            sheet_id=sheet_id,
            chapters_written=chapters_written,
            chapters_target=chapters_target
        )

        all_requests.extend(requests)
        print(f"    Requests: {len(requests)}")

    print(f"\n{'='*60}")
    print(f"Total requests generated: {len(all_requests)}")
    print(f"{'='*60}")

    # Save as single batch
    batch_file = "/tmp/clear_unwritten_batch.json"

    with open(batch_file, 'w', encoding='utf-8') as f:
        json.dump(all_requests, f, ensure_ascii=False, indent=2)

    size_kb = os.path.getsize(batch_file) / 1024
    print(f"\n✓ Saved: {batch_file} ({size_kb:.1f} KB)")
    print(f"✓ Ready to apply {len(all_requests)} clear requests")


def generate_clear_requests(sheet_id, chapters_written, chapters_target):
    """Generate requests to set unwritten chapters to white"""

    requests = []

    # Calculate unwritten range
    unwritten_start = chapters_written
    unwritten_count = chapters_target - chapters_written

    if unwritten_count <= 0:
        return requests

    # For each platform row (rows 5-8 = indices 5-8)
    for row_idx in range(5, 9):
        # Clear unwritten chapters (set to white)
        # Columns: D + chapters_written onwards
        request = {
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": row_idx,
                    "endRowIndex": row_idx + 1,
                    "startColumnIndex": 3 + unwritten_start,  # After written chapters
                    "endColumnIndex": 3 + chapters_target  # All remaining chapters
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": {
                            "red": 1.0,
                            "green": 1.0,
                            "blue": 1.0
                        }
                    }
                },
                "fields": "userEnteredFormat.backgroundColor"
            }
        }

        requests.append(request)

    return requests


if __name__ == "__main__":
    main()
