#!/usr/bin/env python3
"""
NC Scene Generator - Main Entry Point
=====================================

วิธีใช้:

1. Interactive Mode (แนะนำ):
   python nc_generate.py

2. Quick Mode:
   python nc_generate.py --quick "Mafia boss and debt girl first night"

3. Preset Mode:
   python nc_generate.py --preset mafia_first_night

4. List Presets:
   python nc_generate.py --list

"""

import sys
import os
import argparse

# Add scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts"))

from nc_workflow import NCWorkflow
from nc_preset import list_presets, run_preset


def main():
    parser = argparse.ArgumentParser(
        description="NC Scene Generator - สร้างฉาก NC อัตโนมัติ",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
ตัวอย่างการใช้งาน:
  python nc_generate.py                    # Interactive mode
  python nc_generate.py --list             # ดู presets
  python nc_generate.py --preset mafia_first_night
  python nc_generate.py --quick "เจ้าพ่อกับสาวใช้หนี้ คืนแรก" --intensity 9
        """
    )

    parser.add_argument("--list", "-l", action="store_true",
                        help="แสดงรายการ presets")
    parser.add_argument("--preset", "-p", type=str,
                        help="รันจาก preset")
    parser.add_argument("--quick", "-q", type=str,
                        help="รันแบบเร็วด้วย scenario")
    parser.add_argument("--intensity", "-i", type=int, default=9,
                        help="ความเข้มข้น 1-10 (default: 9)")
    parser.add_argument("--file", "-f", type=str,
                        help="รันจากไฟล์ NC Brief")

    args = parser.parse_args()

    print("\n" + "="*60)
    print("   🔞 NC Scene Generator")
    print("   Powered by Ollama + Mac Studio")
    print("="*60)

    if args.list:
        list_presets()
    elif args.preset:
        run_preset(args.preset, args.intensity)
    elif args.quick:
        workflow = NCWorkflow()
        workflow.run_quick(args.quick, args.intensity)
    elif args.file:
        workflow = NCWorkflow()
        workflow.run_from_file(args.file)
    else:
        # Default: Interactive mode
        workflow = NCWorkflow()
        workflow.run_interactive()


if __name__ == "__main__":
    main()
