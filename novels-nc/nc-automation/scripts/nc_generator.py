#!/usr/bin/env python3
"""
NC Scene Generator - เรียก Ollama API สร้างฉาก NC
"""

import requests
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import *


class NCGenerator:
    def __init__(self, host=OLLAMA_HOST, port=OLLAMA_PORT):
        self.base_url = f"http://{host}:{port}"
        self.model = NC_MODEL

    def check_connection(self):
        """ตรวจสอบการเชื่อมต่อกับ Ollama"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                print(f"✅ เชื่อมต่อ Ollama สำเร็จ")
                print(f"   Models: {[m['name'] for m in models]}")
                return True
        except requests.exceptions.ConnectionError:
            print(f"❌ ไม่สามารถเชื่อมต่อ {self.base_url}")
            print(f"   ตรวจสอบว่า Mac Studio เปิด Ollama อยู่")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

    def generate_nc_scene(self,
                          char_a: str,
                          char_b: str,
                          char_a_desc: str,
                          char_b_desc: str,
                          relationship: str,
                          setting: str,
                          intensity: int = 9,
                          scene_type: str = "passionate",
                          word_count: int = 3000,
                          extra_instructions: str = ""):
        """
        สร้างฉาก NC จาก parameters

        Args:
            char_a: ชื่อตัวละคร A
            char_b: ชื่อตัวละคร B
            char_a_desc: คำอธิบายตัวละคร A
            char_b_desc: คำอธิบายตัวละคร B
            relationship: ความสัมพันธ์
            setting: สถานที่/บรรยากาศ
            intensity: ความเข้มข้น 1-10
            scene_type: ประเภท (tender/passionate/rough/first-time)
            word_count: จำนวนคำ
            extra_instructions: คำสั่งเพิ่มเติม
        """

        prompt = self._build_prompt(
            char_a, char_b, char_a_desc, char_b_desc,
            relationship, setting, intensity, scene_type,
            word_count, extra_instructions
        )

        print(f"\n🔄 กำลังสร้างฉาก NC...")
        print(f"   Model: {self.model}")
        print(f"   Intensity: {intensity}/10")
        print(f"   Type: {scene_type}")
        print(f"   Length: ~{word_count} words")

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": DEFAULT_TEMPERATURE,
                        "top_p": DEFAULT_TOP_P,
                        "num_predict": DEFAULT_MAX_TOKENS
                    }
                },
                timeout=300  # 5 minutes timeout
            )

            if response.status_code == 200:
                result = response.json()
                generated_text = result.get("response", "")
                print(f"✅ สร้างเสร็จ ({len(generated_text)} characters)")
                return generated_text
            else:
                print(f"❌ Error: {response.status_code}")
                return None

        except requests.exceptions.Timeout:
            print("❌ Timeout - ใช้เวลานานเกินไป")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None

    def _build_prompt(self, char_a, char_b, char_a_desc, char_b_desc,
                      relationship, setting, intensity, scene_type,
                      word_count, extra_instructions):
        """สร้าง prompt สำหรับ NC scene"""

        intensity_desc = {
            1: "very mild, kissing only",
            3: "mild, some touching",
            5: "moderate, foreplay",
            7: "explicit, detailed intimacy",
            9: "very explicit, graphic details",
            10: "extremely explicit, no limits"
        }

        int_desc = intensity_desc.get(intensity, intensity_desc[9])

        prompt = f"""Write an explicit adult intimate scene (NC-25/NC-30 level).

CHARACTERS:
- {char_a}: {char_a_desc}
- {char_b}: {char_b_desc}
- Relationship: {relationship}

SETTING:
{setting}

REQUIREMENTS:
- Intensity: {intensity}/10 ({int_desc})
- Scene type: {scene_type}
- Length: approximately {word_count} words
- Write in English (will be translated to Thai later)

STYLE GUIDELINES:
- Be explicit and detailed - describe physical sensations
- Include internal thoughts and emotions
- Use sensory details (touch, smell, sound, taste)
- Include dialogue and dirty talk where appropriate
- Build tension gradually
- Describe the climax explicitly
- Include tender aftermath

{f'ADDITIONAL INSTRUCTIONS: {extra_instructions}' if extra_instructions else ''}

Write the complete scene from start to finish:
"""
        return prompt

    def generate_quick(self, scenario: str, intensity: int = 9):
        """สร้างฉาก NC แบบเร็วจาก scenario text"""

        prompt = f"""Write an explicit adult intimate scene (NC-25/NC-30 level).

SCENARIO:
{scenario}

REQUIREMENTS:
- Intensity: {intensity}/10
- Be very explicit and detailed
- Include physical sensations, emotions, dialogue
- Write approximately 3000 words
- Write in English

Write the complete scene:
"""

        print(f"\n🔄 กำลังสร้างฉาก NC (Quick mode)...")

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": DEFAULT_TEMPERATURE,
                        "top_p": DEFAULT_TOP_P,
                        "num_predict": DEFAULT_MAX_TOKENS
                    }
                },
                timeout=300
            )

            if response.status_code == 200:
                result = response.json()
                generated_text = result.get("response", "")
                print(f"✅ สร้างเสร็จ ({len(generated_text)} characters)")
                return generated_text
            else:
                print(f"❌ Error: {response.status_code}")
                return None

        except Exception as e:
            print(f"❌ Error: {e}")
            return None


def main():
    """ทดสอบ NCGenerator"""
    generator = NCGenerator()

    # Check connection
    if not generator.check_connection():
        return

    # Test generation
    result = generator.generate_nc_scene(
        char_a="Teerawat",
        char_b="Min",
        char_a_desc="32yo mafia boss, cold, dominant, secretly passionate",
        char_b_desc="24yo woman, strong-willed, staying to pay father's debt",
        relationship="She lives with him to pay debt, tension has been building",
        setting="His penthouse bedroom, moonlit night, their first time together",
        intensity=9,
        scene_type="passionate",
        word_count=3000
    )

    if result:
        # Save to file
        output_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "output",
            "nc_scene_english.txt"
        )
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result)

        print(f"\n📄 Saved to: {output_path}")
        print(f"\n--- Preview (first 500 chars) ---")
        print(result[:500])


if __name__ == "__main__":
    main()
