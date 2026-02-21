"""
Populate all story sheets with data and apply written chapter coloring
"""

import json
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from formatting_helpers import hex_to_rgb


def main():
    """Generate commands for Claude Code to execute"""
    print("\n" + "="*60)
    print("Populating Story Sheets")
    print("="*60)

    # Load instructions
    instructions_file = os.path.join(
        os.path.dirname(__file__),
        'data',
        'story_sheets_instructions.json'
    )

    with open(instructions_file, 'r', encoding='utf-8') as f:
        instructions = json.load(f)

    # Generate operations list
    operations = []

    for idx, inst in enumerate(instructions, start=1):
        title = inst['title']
        sheet_title = inst['sheet_title']
        chapters_written = inst['chapters_written']
        chapters_target = inst['chapters_target']
        novel_data = inst['novel_data']

        print(f"\n{idx}. {title}")
        print(f"   Sheet: {sheet_title}")
        print(f"   Chapters: {chapters_written}/{chapters_target} written")

        # Build data for this sheet
        data = build_sheet_data(novel_data)

        # Calculate formatting specs
        num_cols = len(data[4])  # Header row has all columns
        formatting = build_format_specs(novel_data, num_cols)

        operations.append({
            "novel_id": idx,
            "title": title,
            "sheet_title": sheet_title,
            "data": data,
            "formatting": formatting,
            "chapters_written": chapters_written,
            "chapters_target": chapters_target
        })

    # Save operations
    output_file = os.path.join(os.path.dirname(__file__), 'data', 'populate_operations.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(operations, f, ensure_ascii=False, indent=2)

    print(f"\n✓ Operations saved to: {output_file}")
    print(f"\n✓ Ready to populate {len(operations)} sheets")
    print("\nNext: Claude Code will:")
    print("  1. Write data to each sheet")
    print("  2. Apply formatting with written chapter colors")
    print("  3. Verify all sheets are correct")


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
    meta_text = f"แนว: {genre} | ตอนทั้งหมด: {chapters_target} | เขียนแล้ว: {chapters_written} | 💰Paywall: ตอน {paywall} | สถานะ: {status}"
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


def build_format_specs(novel_data, num_cols):
    """Build formatting specifications (to be converted to batch_update requests later)"""
    chapters_written = novel_data['chapters_written']
    chapters_target = novel_data['chapters_target']
    paywall = novel_data['paywall']

    specs = {
        "title_row": {"row": 0, "cols": num_cols, "bold": True, "fontSize": 16, "align": "CENTER", "bg": {"red": 0.95, "green": 0.95, "blue": 0.95}},
        "metadata_row": {"row": 1, "cols": num_cols, "align": "CENTER", "bg": {"red": 0.98, "green": 0.98, "blue": 0.98}},
        "header_row": {"row": 4, "cols": num_cols, "bold": True, "align": "CENTER", "bg": {"red": 0.8, "green": 0.8, "blue": 0.8}},
        "platforms": [],
        "freeze": {"rows": 5, "cols": 3},
        "column_widths": {
            "first_three": 120,
            "chapters": 30
        }
    }

    # Platform rows formatting
    for idx, platform in enumerate(config.PLATFORMS):
        row_index = 5 + idx
        color_rgb = hex_to_rgb(platform['color_hex'])

        platform_spec = {
            "row": row_index,
            "platform_name": platform['name'],
            "platform_color": color_rgb,
            "chapters_written": chapters_written,
            "chapters_target": chapters_target,
            "paywall": paywall
        }

        specs["platforms"].append(platform_spec)

    return specs


if __name__ == "__main__":
    main()
