# ===========================================
# NC Automation Settings
# ===========================================

# Mac Studio Ollama Server
OLLAMA_HOST = "192.168.31.125"
OLLAMA_PORT = 11434
OLLAMA_URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}"

# Model Settings
NC_MODEL = "dolphin-mixtral:8x7b"  # Model สำหรับเขียน NC
FAST_MODEL = "dolphin-mistral:7b"  # Model เร็ว (draft)

# Generation Settings
DEFAULT_TEMPERATURE = 0.85
DEFAULT_TOP_P = 0.92
DEFAULT_MAX_TOKENS = 4096

# Output Settings
OUTPUT_DIR = "output"
DEFAULT_LANGUAGE = "thai"

# ===========================================
# Novel Folder Naming (ชื่อโฟลเดอร์นิยาย)
# ===========================================

# Format: {number}. {novel_name}
# Example: 2. สวาทลับคุณหนูมาเฟีย
NOVEL_FOLDER_FORMAT = "{number}. {name}"

def format_novel_folder(number: int, name: str) -> str:
    """สร้างชื่อโฟลเดอร์นิยายพร้อมเลขลำดับ"""
    return f"{number}. {name}"

def get_next_novel_number(existing_folders: list) -> int:
    """หาเลขลำดับถัดไปจากโฟลเดอร์ที่มีอยู่"""
    max_num = 0
    for folder in existing_folders:
        if ". " in folder:
            try:
                num = int(folder.split(". ")[0])
                max_num = max(max_num, num)
            except ValueError:
                pass
    return max_num + 1

# Intensity Levels
INTENSITY_LEVELS = {
    "soft": 5,      # NC15-18
    "medium": 7,    # NC20
    "hard": 9,      # NC25
    "extreme": 10   # NC30+
}

# ===========================================
# NC Distribution Rules (กฎการกระจายฉาก NC)
# ===========================================

# Rule 1: เปอร์เซ็นต์ฉาก NC ต่อจำนวนตอนทั้งหมด
NC_CHAPTER_PERCENTAGE_MIN = 35  # ขั้นต่ำ 35%
NC_CHAPTER_PERCENTAGE_MAX = 45  # สูงสุด 45%

# Rule 2: Rating tags สำหรับใส่ในชื่อตอน (ตั้งแต่ NC20 ขึ้นไป)
NC_RATING_TAGS = ["NC20", "NC25+", "NC30+"]

# Chapter title format: ตอนที่ {n} {title} [{rating}]
# Example: ตอนที่ 3 ธีจัดในรถ [NC25+]

def calculate_nc_chapters(total_chapters: int) -> dict:
    """คำนวณจำนวนตอน NC ที่ต้องมีตามกฎ"""
    min_nc = int(total_chapters * NC_CHAPTER_PERCENTAGE_MIN / 100)
    max_nc = int(total_chapters * NC_CHAPTER_PERCENTAGE_MAX / 100)

    # ปัดขึ้นให้ขั้นต่ำ
    if (total_chapters * NC_CHAPTER_PERCENTAGE_MIN / 100) > min_nc:
        min_nc += 1

    return {
        "total_chapters": total_chapters,
        "min_nc_chapters": min_nc,
        "max_nc_chapters": max_nc,
        "percentage_range": f"{NC_CHAPTER_PERCENTAGE_MIN}%-{NC_CHAPTER_PERCENTAGE_MAX}%"
    }

def format_nc_chapter_title(chapter_num: int, title: str, rating: str) -> str:
    """สร้างชื่อตอนพร้อม NC rating tag"""
    if rating not in NC_RATING_TAGS:
        raise ValueError(f"Invalid rating: {rating}. Must be one of {NC_RATING_TAGS}")
    return f"ตอนที่ {chapter_num} {title} [{rating}]"

def validate_nc_distribution(total_chapters: int, nc_chapters: int) -> dict:
    """ตรวจสอบว่าจำนวนตอน NC อยู่ในเกณฑ์หรือไม่"""
    rules = calculate_nc_chapters(total_chapters)
    percentage = (nc_chapters / total_chapters) * 100

    status = "OK"
    message = f"NC {nc_chapters}/{total_chapters} ตอน ({percentage:.1f}%)"

    if nc_chapters < rules["min_nc_chapters"]:
        status = "BELOW_MIN"
        needed = rules["min_nc_chapters"] - nc_chapters
        message = f"NC น้อยเกินไป! ต้องเพิ่มอีก {needed} ตอน"
    elif nc_chapters > rules["max_nc_chapters"]:
        status = "ABOVE_MAX"
        excess = nc_chapters - rules["max_nc_chapters"]
        message = f"NC มากเกินไป! ต้องลด {excess} ตอน"

    return {
        "status": status,
        "message": message,
        "current": nc_chapters,
        "min_required": rules["min_nc_chapters"],
        "max_allowed": rules["max_nc_chapters"],
        "percentage": round(percentage, 1)
    }
