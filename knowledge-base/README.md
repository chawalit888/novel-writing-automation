# Knowledge Base - ฐานข้อมูลสำหรับเขียนนิยาย

## Overview
เก็บผลการ research ทั้งหมดที่ใช้ในการเขียนนิยาย
เพื่อให้นำกลับมาใช้ซ้ำได้โดยไม่ต้อง research ใหม่

---

## โครงสร้าง

```
knowledge-base/
├── README.md                    # ไฟล์นี้
│
├── historical/                  # ข้อมูลประวัติศาสตร์
│   ├── rattanakosin-early/      # สมัยรัตนโกสินทร์ตอนต้น
│   ├── rama5-era/               # สมัยรัชกาลที่ 5
│   ├── thai-noble-families/     # ตระกูลขุนนาง/เจ้านาย
│   └── [ยุค-หัวข้อ].md
│
├── medical/                     # ข้อมูลทางการแพทย์
│   ├── injuries/                # การบาดเจ็บ
│   ├── conditions/              # โรค/อาการ
│   ├── psychology/              # จิตวิทยา
│   └── [หัวข้อ].md
│
├── crime-legal/                 # กฎหมาย/อาชญากรรม
│   ├── thai-criminal-law/       # กฎหมายอาญาไทย
│   ├── investigation/           # กระบวนการสืบสวน
│   ├── court-procedures/        # กระบวนการศาล
│   └── [หัวข้อ].md
│
├── genre-guides/                # คู่มือแนวนิยาย
│   ├── dark-romance-guide.md
│   ├── historical-romance-guide.md
│   ├── mystery-thriller-guide.md
│   └── [แนว]-guide.md
│
└── profession-industry/         # ข้อมูลอาชีพ/วงการ
    ├── ceo-business/            # ธุรกิจ/CEO
    ├── mafia-underground/       # มาเฟีย/ใต้ดิน
    ├── debt-collection/         # การทวงหนี้
    ├── entertainment/           # วงการบันเทิง
    └── [อาชีพ].md
```

---

## วิธีใช้

### เมื่อเริ่มนิยายใหม่
1. ตรวจว่ามี knowledge ที่ต้องใช้อยู่แล้วหรือไม่
2. ถ้ามี → อ่านและใช้เป็น reference
3. ถ้ายังไม่มี → ทำ research แล้วบันทึกไว้

### เมื่อ Research เสร็จ
1. สร้างไฟล์ .md ในหมวดที่เกี่ยวข้อง
2. ใส่แหล่งอ้างอิงเสมอ
3. ระบุวันที่ research
4. ระบุนิยายที่ใช้ (ถ้ามี)

### รูปแบบไฟล์
```markdown
# [หัวข้อ]
## วันที่ Research: [วันที่]
## ใช้สำหรับ: [ชื่อนิยาย] (หรือ "ทั่วไป")

---

## ข้อมูลหลัก
[เนื้อหา]

## แหล่งอ้างอิง
- [URL/ชื่อหนังสือ]

## หมายเหตุ
[สิ่งที่ต้องระวัง/ข้อจำกัด]
```

---

## Skills ที่ใช้ Knowledge Base

| Skill | หมวดที่ใช้ |
|-------|----------|
| historical-research | `historical/` |
| fact-checker | `medical/`, `crime-legal/`, `profession-industry/` |
| genre-adapter | `genre-guides/` |
| mystery-crime-plotter | `crime-legal/` |
| world-building | `historical/`, ทุกหมวด |
| novel-writer | ทุกหมวด (reference ขณะเขียน) |
