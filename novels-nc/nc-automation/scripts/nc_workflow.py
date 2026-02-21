#!/usr/bin/env python3
"""
NC Workflow - ระบบอัตโนมัติสำหรับสร้างฉาก NC

Flow:
1. รับ input (ข้อมูลตัวละคร, ฉาก, ความเข้มข้น)
2. เรียก Ollama API (Mac Studio) สร้าง NC ภาษาอังกฤษ
3. บันทึกผลลัพธ์
4. แจ้งให้ copy ไปให้ Claude แปลเป็นไทย
"""

import os
import sys
import json
import argparse
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.nc_generator import NCGenerator
from config.settings import *


class NCWorkflow:
    def __init__(self):
        self.generator = NCGenerator()
        self.output_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "output"
        )
        os.makedirs(self.output_dir, exist_ok=True)

    def run_interactive(self):
        """รันแบบ interactive - ถามข้อมูลทีละอย่าง"""

        print("\n" + "="*60)
        print("   NC Scene Generator - Interactive Mode")
        print("="*60)

        # Check connection first
        if not self.generator.check_connection():
            print("\n⚠️  กรุณาตรวจสอบว่า Mac Studio เปิด Ollama อยู่")
            print(f"   ที่ Mac Studio รัน: ollama serve")
            return

        print("\n📝 กรอกข้อมูลฉาก NC:\n")

        # Character A
        char_a = input("ชื่อตัวละคร A (เช่น ธีรวัฒน์): ").strip() or "Teerawat"
        char_a_desc = input(f"คำอธิบาย {char_a} (เช่น เจ้าพ่อมาเฟีย อายุ 32): ").strip() or "32yo mafia boss, dominant"

        # Character B
        char_b = input("ชื่อตัวละคร B (เช่น มิน): ").strip() or "Min"
        char_b_desc = input(f"คำอธิบาย {char_b} (เช่น สาว 24 แข็งแกร่ง): ").strip() or "24yo woman, strong-willed"

        # Relationship
        relationship = input("ความสัมพันธ์ (เช่น อยู่ด้วยกันเพื่อใช้หนี้): ").strip() or "complicated, tension building"

        # Setting
        setting = input("สถานที่/บรรยากาศ (เช่น ห้องนอน penthouse กลางคืน): ").strip() or "bedroom, night, moonlight"

        # Intensity
        print("\nความเข้มข้น:")
        print("  5 = soft (NC15-18)")
        print("  7 = medium (NC20)")
        print("  9 = hard (NC25)")
        print("  10 = extreme (NC30+)")
        intensity_input = input("เลือกความเข้มข้น [9]: ").strip()
        intensity = int(intensity_input) if intensity_input.isdigit() else 9

        # Scene type
        print("\nประเภทฉาก:")
        print("  1 = tender (อ่อนโยน)")
        print("  2 = passionate (เร่าร้อน)")
        print("  3 = rough (รุนแรง)")
        print("  4 = first-time (ครั้งแรก)")
        scene_types = ["tender", "passionate", "rough", "first-time"]
        scene_input = input("เลือกประเภท [2]: ").strip()
        scene_idx = int(scene_input) - 1 if scene_input.isdigit() and 1 <= int(scene_input) <= 4 else 1
        scene_type = scene_types[scene_idx]

        # Word count
        word_input = input("จำนวนคำ (words) [3000]: ").strip()
        word_count = int(word_input) if word_input.isdigit() else 3000

        # Extra instructions
        extra = input("คำสั่งเพิ่มเติม (ถ้ามี): ").strip()

        # Confirm
        print("\n" + "-"*40)
        print("📋 สรุปข้อมูล:")
        print(f"   {char_a} ({char_a_desc})")
        print(f"   {char_b} ({char_b_desc})")
        print(f"   ความสัมพันธ์: {relationship}")
        print(f"   สถานที่: {setting}")
        print(f"   ความเข้มข้น: {intensity}/10 ({scene_type})")
        print(f"   ความยาว: ~{word_count} words")
        print("-"*40)

        confirm = input("\nยืนยันสร้างฉาก? (y/n) [y]: ").strip().lower()
        if confirm == 'n':
            print("ยกเลิก")
            return

        # Generate
        result = self.generator.generate_nc_scene(
            char_a=char_a,
            char_b=char_b,
            char_a_desc=char_a_desc,
            char_b_desc=char_b_desc,
            relationship=relationship,
            setting=setting,
            intensity=intensity,
            scene_type=scene_type,
            word_count=word_count,
            extra_instructions=extra
        )

        if result:
            # Save result
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"nc_scene_{timestamp}.txt"
            filepath = os.path.join(self.output_dir, filename)

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"# NC Scene Generated\n")
                f.write(f"# {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# Characters: {char_a} x {char_b}\n")
                f.write(f"# Intensity: {intensity}/10\n")
                f.write(f"# Type: {scene_type}\n")
                f.write(f"\n{'='*60}\n\n")
                f.write(result)

            print(f"\n✅ บันทึกแล้ว: {filepath}")

            # Also save a copy for easy access
            latest_path = os.path.join(self.output_dir, "latest_nc_scene.txt")
            with open(latest_path, "w", encoding="utf-8") as f:
                f.write(result)

            print(f"✅ Copy ล่าสุด: {latest_path}")

            # Instructions
            print("\n" + "="*60)
            print("📋 ขั้นตอนถัดไป:")
            print("="*60)
            print(f"\n1. เปิดไฟล์: {latest_path}")
            print("2. Copy เนื้อหาทั้งหมด")
            print("3. ส่งให้ Claude พร้อมข้อความ:")
            print("\n   ---")
            print("   ช่วยแปลฉาก NC นี้เป็นภาษาไทยสำนวนนิยาย")
            print("   ให้ได้อารมณ์ มีสำนวนวรรณกรรม Show Don't Tell")
            print("   ---")
            print("\n4. Claude จะแปลงเป็นภาษาไทยสวยๆ ให้")

            return filepath

    def run_quick(self, scenario: str, intensity: int = 9):
        """รันแบบเร็ว - ใส่ scenario เลย"""

        if not self.generator.check_connection():
            return None

        result = self.generator.generate_quick(scenario, intensity)

        if result:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"nc_scene_{timestamp}.txt"
            filepath = os.path.join(self.output_dir, filename)

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(result)

            latest_path = os.path.join(self.output_dir, "latest_nc_scene.txt")
            with open(latest_path, "w", encoding="utf-8") as f:
                f.write(result)

            print(f"\n✅ บันทึกแล้ว: {filepath}")
            return filepath

        return None

    def run_from_file(self, brief_file: str):
        """รันจากไฟล์ NC Brief"""

        if not os.path.exists(brief_file):
            print(f"❌ ไม่พบไฟล์: {brief_file}")
            return None

        with open(brief_file, "r", encoding="utf-8") as f:
            scenario = f.read()

        return self.run_quick(scenario)


def main():
    parser = argparse.ArgumentParser(description="NC Scene Generator")
    parser.add_argument("--interactive", "-i", action="store_true",
                        help="รันแบบ interactive")
    parser.add_argument("--quick", "-q", type=str,
                        help="รันแบบเร็วด้วย scenario")
    parser.add_argument("--file", "-f", type=str,
                        help="รันจากไฟล์ NC Brief")
    parser.add_argument("--intensity", type=int, default=9,
                        help="ความเข้มข้น 1-10 (default: 9)")

    args = parser.parse_args()

    workflow = NCWorkflow()

    if args.quick:
        workflow.run_quick(args.quick, args.intensity)
    elif args.file:
        workflow.run_from_file(args.file)
    else:
        # Default to interactive
        workflow.run_interactive()


if __name__ == "__main__":
    main()
