"""
Novel Factory Tracking System - Configuration
ตั้งค่าระบบ tracking สำหรับนิยาย 23 เรื่อง
"""

import os

# ========================
# Google Sheets Configuration
# ========================
SPREADSHEET_ID = "1JPZKbBXJMxVX9ugJ-WnLQmArIlJEOCEWbjLvb-xZ8OU"  # Novel Factory - Tracking System

# Base directory
BASE_DIR = "/Users/chawalitnoi/Projects/Novel Writing Automation Project"

# Novel directories
NOVELS_DIR = os.path.join(BASE_DIR, "novels")
NOVELS_NC_DIR = os.path.join(BASE_DIR, "novels-nc")

# Output directory
DATA_DIR = os.path.join(BASE_DIR, "agents/tracking/data")

# ========================
# Platform Definitions
# ========================
PLATFORMS = [
    {
        "name": "ธัญวลัย",
        "color_hex": "#F59E0B",
        "color_rgb": {"red": 0.96, "green": 0.62, "blue": 0.04},
        "post_time": "20:00",
        "notes": "รายได้สูงสุด, ห้ามปก AI"
    },
    {
        "name": "readAwrite",
        "color_hex": "#3B82F6",
        "color_rgb": {"red": 0.23, "green": 0.51, "blue": 0.88},
        "post_time": "21:00",
        "notes": "ปก AI ได้, แบ่ง 70%"
    },
    {
        "name": "Dek-D",
        "color_hex": "#EF4444",
        "color_rgb": {"red": 0.94, "green": 0.27, "blue": 0.27},
        "post_time": "19:00",
        "notes": "ฐานผู้อ่านใหญ่"
    },
    {
        "name": "Fictionlog",
        "color_hex": "#22C55E",
        "color_rgb": {"red": 0.13, "green": 0.77, "blue": 0.37},
        "post_time": "20:30",
        "notes": "เสริม portfolio"
    }
]

# ========================
# Status Definitions
# ========================
STATUSES = {
    "กำลังผลิต": {
        "description": "AI กำลังเขียน",
        "color_rgb": {"red": 1.0, "green": 0.95, "blue": 0.0}  # Yellow
    },
    "ผลิตแล้ว": {
        "description": "เขียนเสร็จ รอลง",
        "color_rgb": {"red": 0.0, "green": 0.8, "blue": 0.0}  # Green
    },
    "รอลง": {
        "description": "อยู่ในคิว",
        "color_rgb": {"red": 0.6, "green": 0.4, "blue": 0.8}  # Purple
    },
    "กำลังลง": {
        "description": "กำลังโพสอยู่",
        "color_rgb": {"red": 0.2, "green": 0.6, "blue": 1.0}  # Blue
    },
    "ลงครบแล้ว": {
        "description": "โพสครบทุกตอน",
        "color_rgb": {"red": 0.5, "green": 0.5, "blue": 0.5}  # Gray
    },
    "หยุดลง": {
        "description": "ไม่ปัง หยุดลง",
        "color_rgb": {"red": 1.0, "green": 0.0, "blue": 0.0}  # Red
    }
}

# ========================
# Publishing Rules
# ========================
PUBLISHING_RULES = {
    # เปิดเรื่องใหม่ในวันไหนบ้าง (3 เรื่อง/สัปดาห์ = 12 เรื่อง/เดือน)
    "new_story_days": ["Monday", "Wednesday", "Friday"],

    # กฎการลงตอน
    "day1_episodes": 5,  # Day 1: ลง 5 ตอน
    "day2_episodes": 5,  # Day 2: ลง 5 ตอน
    "daily_episodes": 1,  # Day 3+: วันละ 1 ตอน

    # Paywall
    "paywall_start_default": 20,  # เริ่มตอนที่ 20-25
    "paywall_start_min": 20,
    "paywall_start_max": 25,

    # Performance criteria
    "kill_criteria_views": 5000,  # <5k views ที่ตอน 25 → หยุดลง
    "kill_criteria_chapter": 25,

    "hit_criteria_views": 20000,  # 20k+ views = HIT
    "hit_criteria_followers": 1000,  # 1k+ followers = HIT

    # Cross-platform publishing
    "platform_launch_delay_days": 7  # เปิดแพลตฟอร์มแรก → รอ 1 สัปดาห์ → เปิดแพลตฟอร์มที่ 2
}

# ========================
# Revenue Targets
# ========================
REVENUE_TARGETS = {
    "hit_stories_target": [10, 15],  # 10-15 เรื่อง HIT
    "revenue_per_story_min": 50000,  # 50k THB/เรื่อง/เดือน
    "revenue_per_story_max": 100000,  # 100k THB/เรื่อง/เดือน
    "monthly_target_min": 500000,  # 500k THB/เดือน
    "monthly_target_max": 1000000,  # 1M THB/เดือน
    "timeline_months": [3, 4]  # 3-4 เดือน
}

# ========================
# Genre Mapping
# ========================
GENRE_KEYWORDS = {
    "CEO": ["ประธาน", "CEO", "เจ้านาย", "นายจ้าง", "ออฟฟิศ"],
    "มาเฟีย": ["มาเฟีย", "อันธพาล", "เจ้าพ่อ", "แก๊งค์"],
    "ย้อนยุค": ["วัง", "พระนาง", "เจ้าชาย", "โบราณ", "ราชสำนัก", "สมัยก่อน"],
    "ทหาร": ["ทหาร", "นายทหาร", "พล", "ร้อย", "เอก"],
    "หมอ": ["หมอ", "แพทย์", "โรงพยาบาล", "คลินิก"],
    "Romance": ["รัก", "หวาน", "โรแมนติก"]
}

# NC Rating patterns
NC_RATINGS = ["NC17", "NC18", "NC20", "NC25", "NC25+", "NC30", "NC30+"]

# ========================
# Metadata File Patterns
# ========================
METADATA_FILES = {
    "title": "01-ชื่อเรื่อง",  # 01-ชื่อเรื่อง-*.txt
    "plot": "02-plot",  # 02-plot-*.txt
    "characters": "03-ตัวละคร",  # 03-ตัวละคร-*.txt
    "synopsis": "04-เรื่องย่อ",  # 04-เรื่องย่อ-*.txt
    "blurb": "05-คำโปรย",  # 05-คำโปรย-*.txt
}

# Chapter file pattern
CHAPTER_PATTERN = r"^ตอนที่(\d+)-.*\.txt$"

# ========================
# Google Sheets Structure
# ========================
SHEET_NAMES = {
    "master": "📊 MASTER",
    "monthly": "📆 MONTHLY",
    "weekly": "📅 WEEKLY",
    "analytics": "📈 ANALYTICS"
}

# MASTER Sheet columns
MASTER_COLUMNS = [
    "#",
    "ชื่อเรื่อง",
    "แนว",
    "ตอนที่เขียนแล้ว",
    "ตอน Target",
    "% Progress",
    "สถานะ",
    "QC Score",
    "ธัญวลัย",
    "readAwrite",
    "Dek-D",
    "Fictionlog",
    "Paywall",
    "วันที่เปิด",
    "Tags",
    "หมายเหตุ"
]

# ANALYTICS Sheet columns
ANALYTICS_COLUMNS = [
    "ชื่อเรื่อง",
    "แพลตฟอร์ม",
    "วันที่เช็ค",
    "วิว",
    "ผู้ติดตาม",
    "คอมเมนต์",
    "Coin/รายได้",
    "Engagement Rate",
    "Growth Rate",
    "สถานะ"
]

# ========================
# Helper Functions
# ========================

def get_platform_color(platform_name: str) -> dict:
    """
    Get RGB color for platform

    Args:
        platform_name: ชื่อแพลตฟอร์ม (ธัญวลัย, readAwrite, etc.)

    Returns:
        dict: {"red": float, "green": float, "blue": float}
    """
    for platform in PLATFORMS:
        if platform["name"] == platform_name:
            return platform["color_rgb"]
    return {"red": 0.5, "green": 0.5, "blue": 0.5}  # Default gray


def get_status_color(status: str) -> dict:
    """
    Get RGB color for status

    Args:
        status: สถานะ (กำลังผลิต, ผลิตแล้ว, etc.)

    Returns:
        dict: {"red": float, "green": float, "blue": float}
    """
    if status in STATUSES:
        return STATUSES[status]["color_rgb"]
    return {"red": 1.0, "green": 1.0, "blue": 1.0}  # Default white


def get_platform_post_time(platform_name: str) -> str:
    """
    Get posting time for platform

    Args:
        platform_name: ชื่อแพลตฟอร์ม

    Returns:
        str: เวลาโพส (e.g., "20:00")
    """
    for platform in PLATFORMS:
        if platform["name"] == platform_name:
            return platform["post_time"]
    return "20:00"  # Default


# Create data directory if not exists
os.makedirs(DATA_DIR, exist_ok=True)
