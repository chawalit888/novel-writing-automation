# Cover Design Team

## Overview

ทีมออกแบบปกนิยายอัตโนมัติ ทำงานร่วมกับระบบ Agent ของ Novel Empire

```
                    ┌─────────────────────┐
                    │      CEO Agent      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Cover Design Mgr   │
                    │    (mgr-cover-001)  │
                    └──────────┬──────────┘
                               │
          ┌───────────┬───────┴───────┬───────────┐
          │           │               │           │
          ▼           ▼               ▼           ▼
    ┌──────────┐ ┌──────────┐  ┌──────────┐ ┌──────────┐
    │  Image   │ │  Prompt  │  │  Layout  │ │  Cover   │
    │  Scout   │ │ Engineer │  │ Designer │ │    QC    │
    └──────────┘ └──────────┘  └──────────┘ └──────────┘
```

---

## Team Members

| Agent | ID | Role | Description |
|-------|-----|------|-------------|
| **Cover Design Manager** | mgr-cover-001 | Manager | ผู้จัดการทีม รับ brief และประสานงาน |
| **Image Scout** | cover-scout-001 | Subagent | หารูป Stock Photo ที่เหมาะสม |
| **Prompt Engineer** | cover-prompt-001 | Subagent | เขียน Prompt สำหรับ AI Enhance |
| **Layout Designer** | cover-layout-001 | Subagent | ออกแบบ Layout และ Typography |
| **Cover QC** | cover-qc-001 | Subagent | ตรวจสอบคุณภาพก่อนส่งมอบ |

---

## Workflow

```
1. รับ Brief จาก CEO/User
         │
         ▼
2. Manager วิเคราะห์ข้อมูลนิยาย
         │
         ▼
3. Image Scout หารูป Stock Photo
         │
         ▼
4. Prompt Engineer เขียน AI Prompt
         │
         ▼
5. User ใช้ AI Tool (Leonardo/Canva) สร้างปก
         │
         ▼
6. Layout Designer กำหนด Typography
         │
         ▼
7. Cover QC ตรวจสอบคุณภาพ
         │
         ▼
8. ส่งมอบปกสำเร็จ
```

---

## Directory Structure

```
cover-design-team/
├── README.md              # This file
├── templates/
│   ├── cover-brief-template.md    # Template สำหรับ brief
│   ├── color-schemes.json         # Color schemes by genre
│   └── font-guide.md              # Font recommendations
├── resources/
│   └── stock-photo-sources.md     # แหล่งหารูป
├── skills/
│   └── (skills for agents)
└── examples/
    └── (example covers)
```

---

## Quick Start

### 1. สร้าง Cover Brief

```bash
# Copy template และกรอกข้อมูล
cp templates/cover-brief-template.md {{novel_path}}/covers/brief.md
```

### 2. Run Cover Design Manager

```bash
python agents/agent_runner.py cover-design-manager
```

### 3. ส่ง Task

```bash
python agents/orchestrator.py --send-task '{
  "type": "create_cover",
  "novel_path": "novels-nc/2. สวาทลับคุณหนูมาเฟีย",
  "platform": "thanwalai",
  "priority": "normal"
}'
```

---

## Default Cover Size

**ขนาดมาตรฐาน: 900x900 px (1:1 square)**

## Platform Requirements

| Platform | Dimensions | AI Art | Max Size |
|----------|------------|--------|----------|
| **Default** | 900x900 | - | 5MB |
| **ธันวลัย** | 900x900 | ❌ ห้าม generate, ✅ enhance ได้ | 2MB |
| **ReadAWrite** | 900x900 | ✅ ได้ | 5MB |
| **Joylada** | 900x900 | ✅ ได้ | 3MB |

---

## Supported AI Tools

| Tool | Mode | Use For |
|------|------|---------|
| **Leonardo AI** | Canvas | รวมรูป, แต่ง composition |
| **Leonardo AI** | Image to Image | Enhance รูปเดียว |
| **Canva** | Filters + Edit | ปรับสี, ใส่ text (ไม่ใช่ AI) |
| **Midjourney** | Blend | รวมรูป |

---

## Color Schemes

ดูรายละเอียดใน `templates/color-schemes.json`

| Genre | Primary | Secondary | Accent |
|-------|---------|-----------|--------|
| Mafia Romance | #1a1a1a | #8B0000 | #D4AF37 |
| Sweet Romance | #fff5f5 | #ffb6c1 | #ff69b4 |
| Fantasy | #1a1a3e | #4a0080 | #FFD700 |
| Horror | #0d0d0d | #1a1a1a | #8B0000 |
| BL Soft | #1e3a5f | #4a90d9 | #87ceeb |

---

## Best Practices

### สำหรับ ธันวลัย (ห้าม AI Art)

1. **ใช้ Stock Photo เป็นหลัก** จาก Unsplash, Pexels
2. **AI Enhance เท่านั้น** ปรับสี, แสง, รวมภาพ
3. **เก็บหลักฐาน License** ไว้เสมอ
4. **หลีกเลี่ยงรูปที่ดู AI** (นิ้วผิด, texture แปลก)

### Typography Tips

1. **ชื่อเรื่องต้องอ่านง่าย** แม้จาก thumbnail
2. **ใช้ contrast สูง** กับ background
3. **อย่าใช้เกิน 2-3 fonts**
4. **Test บน mobile**

---

## Config Files

- Manager: `agents/config/cover-design-manager.yaml`
- Image Scout: `agents/config/subagents/image-scout.yaml`
- Prompt Engineer: `agents/config/subagents/prompt-engineer.yaml`
- Layout Designer: `agents/config/subagents/layout-designer.yaml`
- Cover QC: `agents/config/subagents/cover-qc.yaml`

---

## Troubleshooting

### AI เปลี่ยนรูปมากเกินไป
- ลด Init Strength เป็น 0.2-0.3
- ใช้ Canvas mode แทน Text-to-Image
- เน้น "keep original" ใน prompt

### ปกไม่ผ่าน ธันวลัย
- ตรวจสอบว่าใช้ Stock Photo จริง
- ลด AI enhancement
- เก็บหลักฐาน license ไว้ชี้แจง

### Text อ่านยาก
- เพิ่ม gradient overlay
- เพิ่ม text shadow
- เปลี่ยนสี text ให้ contrast มากขึ้น

---

## License

Part of Novel Writing Automation Project
