"""
Novel Factory - Create Story Gantt Chart Sheets
Creates individual sheets for each story with Gantt charts
"""

import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from formatting_helpers import hex_to_rgb, create_cell_format


def create_story_gantt_sheet(spreadsheet_id: str, novel_data: dict, sheet_number: int):
    """
    Create Gantt chart sheet for one story

    Args:
        spreadsheet_id: Google Sheets ID
        novel_data: Novel metadata
        sheet_number: Sheet number for unique ID
    """
    from mcp import get_mcp_client

    title = novel_data['title']
    genre = novel_data['genre']
    chapters_written = novel_data['chapters_written']
    chapters_target = novel_data['chapters_target']
    paywall = novel_data['paywall']
    status = novel_data['status']
    tags = ' '.join(novel_data.get('tags', []))

    print(f"\n{'='*60}")
    print(f"Creating sheet for: {title}")
    print(f"Chapters: {chapters_written}/{chapters_target}")
    print(f"{'='*60}")

    # Create sheet
    sheet_title = f"📖 {title[:25]}"  # Limit length

    try:
        result = get_mcp_client().call_tool(
            "mcp__google-sheets__create_sheet",
            {
                "spreadsheet_id": spreadsheet_id,
                "title": sheet_title
            }
        )
        sheet_id = result['properties']['sheetId']
        print(f"✓ Created sheet: {sheet_title} (ID: {sheet_id})")
    except Exception as e:
        print(f"✗ Error creating sheet: {e}")
        return

    # Build data rows
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

    # Calculate range
    num_cols = len(data[4])  # Header row length
    col_letter = chr(64 + num_cols)  # A=65, so 64+n gives the letter
    if num_cols > 26:
        # For columns beyond Z (AA, AB, etc.)
        first_letter = chr(64 + (num_cols - 1) // 26)
        second_letter = chr(65 + (num_cols - 1) % 26)
        col_letter = first_letter + second_letter

    range_str = f"A1:{col_letter}{len(data)}"

    # Write data
    try:
        get_mcp_client().call_tool(
            "mcp__google-sheets__update_cells",
            {
                "spreadsheet_id": spreadsheet_id,
                "sheet": sheet_title,
                "range": range_str,
                "data": data
            }
        )
        print(f"✓ Wrote data to {range_str}")
    except Exception as e:
        print(f"✗ Error writing data: {e}")
        return

    # Apply formatting via batch_update
    requests = []

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
        published = novel_data['platforms'].get(platform['name'], 0)
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

        # Not written chapters: white (no color - default)
        # Leave these cells white to show they haven't been written yet

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

    # Apply all formatting
    try:
        get_mcp_client().call_tool(
            "mcp__google-sheets__batch_update",
            {
                "spreadsheet_id": spreadsheet_id,
                "requests": requests
            }
        )
        print(f"✓ Applied formatting ({len(requests)} requests)")
    except Exception as e:
        print(f"✗ Error applying formatting: {e}")

    print(f"✓ Completed: {title}")


def main():
    """Create all story Gantt sheets"""
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

    # Create sheets for all novels
    for idx, novel in enumerate(novels, start=1):
        create_story_gantt_sheet(
            spreadsheet_id=config.SPREADSHEET_ID,
            novel_data=novel,
            sheet_number=idx
        )

    print("\n" + "="*60)
    print("✓ All story sheets created!")
    print("="*60)


if __name__ == "__main__":
    main()
