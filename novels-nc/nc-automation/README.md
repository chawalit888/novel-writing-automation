# NC Scene Generator - ระบบอัตโนมัติสร้างฉาก NC

## Overview

ระบบอัตโนมัติสำหรับสร้างฉาก NC25+/NC30+ โดยใช้:
- **Mac Studio** (Ollama) - สร้างเนื้อหา NC ภาษาอังกฤษ
- **Claude** - แปลงเป็นภาษาไทยสำนวนนิยาย

---

## โครงสร้างไฟล์

```
nc-automation/
├── nc_generate.py          # 🚀 Main entry point
├── config/
│   └── settings.py         # ตั้งค่า IP, Model, etc.
├── scripts/
│   ├── nc_generator.py     # เรียก Ollama API
│   ├── nc_workflow.py      # Workflow หลัก
│   └── nc_preset.py        # ใช้ preset สำเร็จรูป
├── templates/
│   └── scene_presets.json  # Preset ฉากต่างๆ
└── output/                 # ผลลัพธ์ที่สร้าง
```

---

## วิธีติดตั้ง

### 1. ตรวจสอบ Mac Studio

```bash
# ที่ Mac Studio ต้องรัน Ollama
ollama serve

# ตรวจสอบ IP
ipconfig getifaddr en0
# ต้องได้: 192.168.31.125 (หรือ IP ที่ตั้งไว้)
```

### 2. ตั้งค่า IP (ถ้า IP เปลี่ยน)

แก้ไขไฟล์ `config/settings.py`:

```python
OLLAMA_HOST = "192.168.31.125"  # ← ใส่ IP Mac Studio
```

---

## วิธีใช้งาน

### Mode 1: Interactive (แนะนำ)

```bash
cd nc-automation
python nc_generate.py
```

ระบบจะถามข้อมูลทีละอย่าง:
- ชื่อตัวละคร
- คำอธิบาย
- ความสัมพันธ์
- สถานที่
- ความเข้มข้น

### Mode 2: Preset (เร็วสุด)

```bash
# ดูรายการ preset
python nc_generate.py --list

# รันจาก preset
python nc_generate.py --preset mafia_first_night
python nc_generate.py --preset bl_sweet
python nc_generate.py --preset palace_forbidden
```

### Mode 3: Quick (พิมพ์เอง)

```bash
python nc_generate.py --quick "Mafia boss and debt girl, first night together, passionate" --intensity 9
```

---

## Presets ที่มี

| Preset | คำอธิบาย | Intensity |
|--------|---------|-----------|
| `mafia_first_night` | เจ้าพ่อ x สาวใช้หนี้ | 9/10 |
| `bl_sweet` | BL หวาน | 7/10 |
| `palace_forbidden` | รักต้องห้ามในวัง | 8/10 |
| `ceo_secretary` | CEO x เลขา | 8/10 |
| `enemies_to_lovers` | ศัตรูกลายเป็นคนรัก | 9/10 |
| `reunion` | รักเก่าพบกันใหม่ | 8/10 |

---

## Workflow อัตโนมัติ

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  1. รัน nc_generate.py                                      │
│           │                                                 │
│           ▼                                                 │
│  2. Script เรียก Ollama API ───────► Mac Studio            │
│           │                          (192.168.31.125)      │
│           │                                │                │
│           │◄──────── NC Scene (English) ───┘                │
│           │                                                 │
│           ▼                                                 │
│  3. บันทึกที่ output/latest_nc_scene.txt                    │
│           │                                                 │
│           ▼                                                 │
│  4. Copy ไปให้ Claude แปลเป็นไทย                            │
│           │                                                 │
│           ▼                                                 │
│  5. ได้ฉาก NC ภาษาไทยสวยๆ                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## หลังรัน Script

เมื่อ script สร้างเสร็จ จะได้ไฟล์:
- `output/latest_nc_scene.txt`

**ขั้นตอนถัดไป:**

1. เปิดไฟล์ `output/latest_nc_scene.txt`
2. Copy เนื้อหาทั้งหมด
3. ส่งให้ Claude พร้อมข้อความ:

```
ช่วยแปลฉาก NC นี้เป็นภาษาไทยสำนวนนิยาย
ให้ได้อารมณ์ มีสำนวนวรรณกรรม Show Don't Tell
ความเข้มข้นเท่าเดิม

[วาง NC Scene ที่นี่]
```

4. Claude จะแปลงเป็นภาษาไทยให้

---

## Intensity Levels

| Level | คำอธิบาย | Rating |
|-------|---------|--------|
| 1-3 | จูบ กอด | NC15 |
| 4-5 | Foreplay | NC18 |
| 6-7 | Explicit เบา | NC20 |
| 8-9 | Explicit ชัด | NC25 |
| 10 | ไม่มีขีดจำกัด | NC30+ |

---

## Troubleshooting

### ❌ Connection Error

```
ไม่สามารถเชื่อมต่อ http://192.168.31.125:11434
```

**แก้ไข:**
1. ตรวจสอบว่า Mac Studio เปิดอยู่
2. ที่ Mac Studio รัน: `ollama serve`
3. ตรวจสอบ IP: `ipconfig getifaddr en0`
4. แก้ IP ใน `config/settings.py`

### ❌ Model Not Found

```
Model dolphin-mixtral:8x7b not found
```

**แก้ไข:**
ที่ Mac Studio รัน:
```bash
ollama pull dolphin-mixtral:8x7b
```

### ❌ Timeout

**แก้ไข:**
- Model ใหญ่ใช้เวลานาน (2-5 นาที)
- ลองใช้ model เล็กกว่า: แก้ `NC_MODEL` ใน settings.py เป็น `dolphin-mistral:7b`

---

## เพิ่ม Preset ใหม่

แก้ไขไฟล์ `templates/scene_presets.json`:

```json
{
    "my_new_preset": {
        "name": "My New Scene",
        "char_a": "Name A",
        "char_a_desc": "Description",
        "char_b": "Name B",
        "char_b_desc": "Description",
        "relationship": "Their relationship",
        "setting": "Where and when",
        "intensity": 9,
        "scene_type": "passionate",
        "word_count": 3000
    }
}
```

---

## License

For personal novel writing use only.
