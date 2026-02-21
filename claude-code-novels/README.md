# Claude Code Novel Writing System

ระบบเขียนนิยายคุณภาพสูงด้วย Claude Code

## Overview

ระบบนี้ออกแบบมาสำหรับเขียนนิยาย premium ที่ต้องการ:
- ความซับซ้อนของโครงเรื่องสูง
- Character consistency เข้มงวด
- World building ละเอียด
- คุณภาพการเขียนระดับสูง

## โครงสร้างโฟลเดอร์

```
claude-code-novels/
├── README.md                  # ไฟล์นี้
├── PROJECT_MASTER.md          # Master plan ทั้งหมด
├── projects/                  # โปรเจคนิยายแต่ละเรื่อง
│   └── [story-name]/
│       ├── PROJECT.md         # รายละเอียดเรื่อง
│       ├── characters/        # ข้อมูลตัวละคร
│       ├── world/             # World building
│       ├── outlines/          # โครงเรื่อง
│       ├── chapters/          # บทนิยาย
│       ├── metadata/          # ข้อมูลเสริม
│       └── exports/           # ไฟล์ส่งออก
├── skills/                    # Custom skills
│   ├── novel-writer/          # เขียนบท
│   ├── character-creator/     # สร้างตัวละคร
│   ├── plot-manager/          # จัดการโครงเรื่อง
│   └── consistency-checker/   # ตรวจ consistency
├── templates/                 # Templates แต่ละแนว
│   ├── romantic-comedy/
│   ├── fantasy/
│   ├── horror/
│   ├── mystery/
│   └── bl-gl/
├── tools/                     # Python tools
│   ├── consistency_checker.py
│   ├── export_manager.py
│   ├── stats_tracker.py
│   └── backup_manager.py
└── docs/                      # เอกสาร
```

## การใช้งาน

### 1. สร้างโปรเจคใหม่

```bash
# สั่ง Claude Code:
"สร้างโปรเจคนิยายแฟนตาซีใหม่ ชื่อ Dark Empire"
```

Claude จะ:
1. อ่าน skill: novel-writer
2. อ่าน template: fantasy
3. สร้างโครงสร้างโปรเจค
4. สร้าง PROJECT.md
5. แจ้งเสร็จ

### 2. สร้างตัวละคร

```bash
"สร้างตัวละครหลัก 3 คนสำหรับ Dark Empire"
```

### 3. วางโครงเรื่อง

```bash
"วางโครงเรื่อง Dark Empire 25 ตอน"
```

### 4. เขียนบท

```bash
"เขียนบทที่ 1 ของ Dark Empire"
```

### 5. ตรวจ Consistency

```bash
"ตรวจ consistency บท 1-5 ของ Dark Empire"
```

### 6. Export

```bash
"รวมบท 1-10 เป็นไฟล์เดียว"
```

## Skills

### novel-writer
- เขียนบทนิยายคุณภาพสูง
- มี prompts สำหรับ dialogue, action scene
- ตรวจสอบ consistency

### character-creator
- สร้างตัวละคร
- Templates สำหรับ protagonist/supporting
- Character arc planning

### plot-manager
- วางโครงเรื่อง
- Three-act structure
- Hero's journey template

### consistency-checker
- ตรวจ character consistency
- ตรวจ timeline
- ตรวจ world rules

## Tools

### consistency_checker.py
```bash
python tools/consistency_checker.py projects/dark-empire --start 1 --end 10
```

### export_manager.py
```bash
python tools/export_manager.py projects/dark-empire --format txt epub
```

### stats_tracker.py
```bash
python tools/stats_tracker.py projects/dark-empire
```

### backup_manager.py
```bash
python tools/backup_manager.py projects/dark-empire create
```

## แนวเรื่องที่เหมาะ

1. **Fantasy/Cultivation** - ระบบ magic ซับซ้อน
2. **Horror** - บรรยากาศละเอียด
3. **Mystery** - Timeline แม่นยำ
4. **BL/GL Premium** - Emotional depth
5. **Sci-Fi** - World building ซับซ้อน

## KPIs

- Quality score: ≥ 85/100
- Character consistency: ≥ 90/100
- Words/chapter: 4,000-6,000
- Chapters/week: 7-10

## Tips

1. **อ่านก่อนเขียน** - ให้ Claude อ่าน character sheets และ previous chapters เสมอ
2. **ตรวจบ่อยๆ** - รัน consistency checker ทุก 3-5 บท
3. **Backup** - backup ทุกวันหรือหลังเขียนเสร็จแต่ละบท
4. **Update metadata** - อัพเดท timeline หลังเขียนทุกบท
