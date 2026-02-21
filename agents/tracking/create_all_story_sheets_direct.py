"""
Novel Factory - Create All Story Gantt Chart Sheets
This version is designed to output instructions for Claude Code to execute
"""

import json
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from formatting_helpers import hex_to_rgb

def build_sheet_data(novel_data):
    """Build data array for a story sheet"""
    title = novel_data['title']
    genre = novel_data['genre']
    chapters_written = novel_data['chapters_written']
    chapters_target = novel_data['chapters_target']
    paywall = novel_data['paywall']
    status = novel_data['status']
    tags = ' '.join(novel_data.get('tags', []))

    data = []

    # Row 1: Title with tags
    title_text = f"{title} {tags}"
    data.append([title_text])

    # Row 2: Metadata
    meta_text = f"แนว: {genre} | ตอนทั้งหมด: {chapters_target} | 💰Paywall: ตอน {paywall} | สถานะ: {status}"
    data.append([meta_text])

    # Row 3: Legend
    data.append(["Legend: ▓ เขียนแล้ว (สีทึบ) | ░ ยังไม่เขียน (สีขาว) | 💰 Paywall"])

    # Row 4: Empty
    data.append([""])

    # Row 5: Header row
    header = ["แพลตฟอร์ม", "ลงถึงตอน", "%"]
    # Add chapter columns (1, 2, 3, ...)
    for i in range(1, chapters_target + 1):
        header.append(str(i))
    data.append(header)

    # Row 6-9: Platform rows
    for platform in config.PLATFORMS:
        platform_name = platform['name']
        published = novel_data['platforms'].get(platform_name, 0)
        progress = round(published / chapters_target, 2) if chapters_target > 0 else 0

        row = [platform_name, str(published), f"{int(progress * 100)}%"]

        # Add empty cells for chapters
        for i in range(1, chapters_target + 1):
            row.append("")

        data.append(row)

    # Row 10: Empty
    data.append([""])

    # Row 11+: Publishing rules
    data.append(["กฎการลง:"])
    data.append(["• วันที่ 1: ลง 5 ตอนแรก"])
    data.append(["• วันที่ 2: ลง 5 ตอนถัดไป"])
    data.append(["• วันที่ 3+: ลงวันละ 1 ตอน"])
    data.append([f"• Paywall: เริ่มตอนที่ {paywall}"])

    return data


def build_format_requests(sheet_id, novel_data, num_cols):
    """Build formatting requests for batch_update"""
    requests = []

    chapters_written = novel_data['chapters_written']
    chapters_target = novel_data['chapters_target']
    paywall = novel_data['paywall']

    # 1. Title row (row 0): Large, bold, center
    requests.append({
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": 0,
                "endRowIndex": 1,
                "startColumnIndex": 0,
                "endColumnIndex": num_cols
            },
            "cell": {
                "userEnteredFormat": {
                    "textFormat": {"bold": True, "fontSize": 16},
                    "horizontalAlignment": "CENTER",
                    "verticalAlignment": "MIDDLE",
                    "backgroundColor": {"red": 0.95, "green": 0.95, "blue": 0.95}
                }
            },
            "fields": "userEnteredFormat(textFormat,horizontalAlignment,verticalAlignment,backgroundColor)"
        }
    })

    # 2. Metadata row (row 1): Center
    requests.append({
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": 1,
                "endRowIndex": 2,
                "startColumnIndex": 0,
                "endColumnIndex": num_cols
            },
            "cell": {
                "userEnteredFormat": {
                    "horizontalAlignment": "CENTER",
                    "backgroundColor": {"red": 0.98, "green": 0.98, "blue": 0.98}
                }
            },
            "fields": "userEnteredFormat(horizontalAlignment,backgroundColor)"
        }
    })

    # 3. Header row (row 4): Bold, centered, colored
    requests.append({
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": 4,
                "endRowIndex": 5,
                "startColumnIndex": 0,
                "endColumnIndex": num_cols
            },
            "cell": {
                "userEnteredFormat": {
                    "textFormat": {"bold": True},
                    "horizontalAlignment": "CENTER",
                    "backgroundColor": {"red": 0.8, "green": 0.8, "blue": 0.8}
                }
            },
            "fields": "userEnteredFormat(textFormat,horizontalAlignment,backgroundColor)"
        }
    })

    # 4. Platform rows (rows 5-8): Color Gantt bars
    for idx, platform in enumerate(config.PLATFORMS):
        row_index = 5 + idx
        color_rgb = hex_to_rgb(platform['color_hex'])

        # Platform name cell (column A): bold, platform color
        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": row_index,
                    "endRowIndex": row_index + 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 1
                },
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True},
                        "backgroundColor": color_rgb
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        })

        # Written chapters: medium shade (60% blend with white)
        if chapters_written > 0:
            written_rgb = {
                "red": color_rgb["red"] * 0.6 + 0.4,
                "green": color_rgb["green"] * 0.6 + 0.4,
                "blue": color_rgb["blue"] * 0.6 + 0.4
            }
            requests.append({
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": row_index,
                        "endRowIndex": row_index + 1,
                        "startColumnIndex": 3,  # Column D (chapter 1)
                        "endColumnIndex": 3 + chapters_written
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": written_rgb
                        }
                    },
                    "fields": "userEnteredFormat(backgroundColor)"
                }
            })

        # Mark paywall column (pink background)
        if paywall <= chapters_target:
            requests.append({
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": row_index,
                        "endRowIndex": row_index + 1,
                        "startColumnIndex": 2 + paywall,  # paywall column
                        "endColumnIndex": 3 + paywall
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": {"red": 1.0, "green": 0.75, "blue": 0.8}
                        }
                    },
                    "fields": "userEnteredFormat(backgroundColor)"
                }
            })

    # 5. Freeze first 3 columns and first 5 rows
    requests.append({
        "updateSheetProperties": {
            "properties": {
                "sheetId": sheet_id,
                "gridProperties": {
                    "frozenRowCount": 5,
                    "frozenColumnCount": 3
                }
            },
            "fields": "gridProperties.frozenRowCount,gridProperties.frozenColumnCount"
        }
    })

    # 6. Set column widths
    # Columns A-C: wider
    requests.append({
        "updateDimensionProperties": {
            "range": {
                "sheetId": sheet_id,
                "dimension": "COLUMNS",
                "startIndex": 0,
                "endIndex": 3
            },
            "properties": {"pixelSize": 120},
            "fields": "pixelSize"
        }
    })

    # Chapter columns: narrower (30px)
    requests.append({
        "updateDimensionProperties": {
            "range": {
                "sheetId": sheet_id,
                "dimension": "COLUMNS",
                "startIndex": 3,
                "endIndex": 3 + chapters_target
            },
            "properties": {"pixelSize": 30},
            "fields": "pixelSize"
        }
    })

    return requests


def main():
    """Generate instructions for creating all story sheets"""
    print("\n" + "="*60)
    print("Novel Factory - Story Gantt Sheet Creation")
    print("="*60)

    # Load novels data
    data_file = os.path.join(
        os.path.dirname(__file__),
        'data',
        'novels_data.json'
    )

    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    novels = data['novels']
    print(f"\nFound {len(novels)} novels")
    print(f"Spreadsheet ID: {config.SPREADSHEET_ID}")

    # Output JSON instructions for Claude Code to execute
    instructions = []

    for idx, novel in enumerate(novels, start=1):
        sheet_title = f"📖 {novel['title'][:25]}"

        instruction = {
            "novel_id": idx,
            "title": novel['title'],
            "sheet_title": sheet_title,
            "chapters_written": novel['chapters_written'],
            "chapters_target": novel['chapters_target'],
            "data": build_sheet_data(novel),
            "novel_data": novel  # For formatting
        }

        instructions.append(instruction)
        print(f"{idx}. {novel['title']} ({novel['chapters_written']}/{novel['chapters_target']})")

    # Save instructions to file
    output_file = os.path.join(os.path.dirname(__file__), 'data', 'story_sheets_instructions.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(instructions, f, ensure_ascii=False, indent=2)

    print(f"\n✓ Instructions saved to: {output_file}")
    print("\nNow Claude Code will execute these instructions using MCP tools...")


if __name__ == "__main__":
    main()
