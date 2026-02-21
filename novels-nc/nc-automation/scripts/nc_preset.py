#!/usr/bin/env python3
"""
NC Preset Generator - สร้างฉาก NC จาก preset ที่เตรียมไว้
"""

import os
import sys
import json
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.nc_generator import NCGenerator


def load_presets():
    """โหลด presets จากไฟล์"""
    preset_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "templates",
        "scene_presets.json"
    )

    with open(preset_path, "r", encoding="utf-8") as f:
        return json.load(f)


def list_presets():
    """แสดงรายการ presets"""
    presets = load_presets()

    print("\n" + "="*60)
    print("   Available NC Scene Presets")
    print("="*60 + "\n")

    for key, preset in presets.items():
        print(f"  📖 {key}")
        print(f"     {preset['name']}")
        print(f"     {preset['char_a']} x {preset['char_b']}")
        print(f"     Intensity: {preset['intensity']}/10 ({preset['scene_type']})")
        print()


def run_preset(preset_name: str, intensity_override: int = None):
    """รัน preset ที่เลือก"""

    presets = load_presets()

    if preset_name not in presets:
        print(f"❌ ไม่พบ preset: {preset_name}")
        print(f"   ใช้ --list เพื่อดูรายการ")
        return

    preset = presets[preset_name]
    generator = NCGenerator()

    if not generator.check_connection():
        return

    print(f"\n🎬 Running preset: {preset['name']}")

    result = generator.generate_nc_scene(
        char_a=preset['char_a'],
        char_b=preset['char_b'],
        char_a_desc=preset['char_a_desc'],
        char_b_desc=preset['char_b_desc'],
        relationship=preset['relationship'],
        setting=preset['setting'],
        intensity=intensity_override or preset['intensity'],
        scene_type=preset['scene_type'],
        word_count=preset['word_count']
    )

    if result:
        output_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "output"
        )
        os.makedirs(output_dir, exist_ok=True)

        # Save with preset name
        filepath = os.path.join(output_dir, f"{preset_name}_nc_scene.txt")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(result)

        # Also save as latest
        latest_path = os.path.join(output_dir, "latest_nc_scene.txt")
        with open(latest_path, "w", encoding="utf-8") as f:
            f.write(result)

        print(f"\n✅ บันทึกแล้ว: {filepath}")
        print(f"✅ Copy ล่าสุด: {latest_path}")

        print("\n" + "-"*40)
        print("📋 ขั้นตอนถัดไป: Copy ไปให้ Claude แปลเป็นไทย")
        print("-"*40)


def main():
    parser = argparse.ArgumentParser(description="NC Preset Generator")
    parser.add_argument("--list", "-l", action="store_true",
                        help="แสดงรายการ presets")
    parser.add_argument("--preset", "-p", type=str,
                        help="ชื่อ preset ที่ต้องการรัน")
    parser.add_argument("--intensity", "-i", type=int,
                        help="Override ความเข้มข้น")

    args = parser.parse_args()

    if args.list:
        list_presets()
    elif args.preset:
        run_preset(args.preset, args.intensity)
    else:
        # Interactive selection
        presets = load_presets()
        list_presets()

        print("พิมพ์ชื่อ preset ที่ต้องการ: ", end="")
        choice = input().strip()

        if choice in presets:
            run_preset(choice)
        else:
            print(f"❌ ไม่พบ preset: {choice}")


if __name__ == "__main__":
    main()
