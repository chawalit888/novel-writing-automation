"""
Apply all formatting batches to story sheets
"""

import json
import os

# This script outputs batch commands for Claude Code to execute via MCP

def main():
    print("\n" + "="*60)
    print("Applying Formatting Batches")
    print("="*60)

    # List batch files
    batch_files = []
    for i in range(9):  # 0-8
        filepath = f"/tmp/batch_chunk_{i:02d}.json"
        if os.path.exists(filepath):
            batch_files.append(filepath)
            size_kb = os.path.getsize(filepath) / 1024
            print(f"✓ Found: batch_chunk_{i:02d}.json ({size_kb:.1f} KB)")

    print(f"\nTotal batches: {len(batch_files)}")

    # Read and validate each batch
    all_requests = []
    for filepath in batch_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            batch_data = json.load(f)
            # batch_data is a list of requests
            if isinstance(batch_data, list):
                requests = batch_data
            else:
                requests = batch_data.get('requests', [])
            all_requests.extend(requests)
            print(f"  {os.path.basename(filepath)}: {len(requests)} requests")

    print(f"\nTotal requests: {len(all_requests)}")
    print("\n" + "="*60)
    print("Ready to apply via MCP tools")
    print("="*60)
    print("\nClaude Code will now execute:")
    print("  mcp__google-sheets__batch_update(")
    print("    spreadsheet_id='1JPZKbBXJMxVX9ugJ-WnLQmArIlJEOCEWbjLvb-xZ8OU',")
    print(f"    requests=<{len(all_requests)} formatting requests>")
    print("  )")

    # Save combined requests for Claude Code to use
    output_file = "/tmp/all_formatting_requests.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({"requests": all_requests}, f)

    print(f"\n✓ Combined requests saved to: {output_file}")
    print(f"  File size: {os.path.getsize(output_file) / 1024:.1f} KB")

if __name__ == "__main__":
    main()
