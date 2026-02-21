# Novel Queue System

ระบบจัดการคิวเขียนนิยาย - แก้ปัญหางานหยุดเมื่อติด Rate Limit

## ปัญหาที่แก้ไข

1. **งานหยุดเมื่อติด Rate Limit** → ระบบจะ auto-retry เมื่อ limit หมด
2. **งานหายเมื่อ fail** → ระบบเก็บ state และ retry ได้
3. **ไม่รู้ progress** → ดู progress ของแต่ละเรื่องได้
4. **ต้องสั่งทีละตอน** → สร้าง batch jobs ทั้งเรื่องได้

---

## Quick Start

### 1. เพิ่มเรื่องใหม่เข้าคิว

```bash
cd agents/queue
python novel_queue.py add "mafia-rebirth-wife" -c 36 -o "../../novels/mafia-rebirth-wife/outline.md"
```

### 2. ดูสถานะคิว

```bash
python novel_queue.py status
```

### 3. เริ่ม Auto-Resume Worker

```bash
python novel_queue.py start
```

### 4. ดู Progress

```bash
python novel_queue.py progress "mafia-rebirth-wife"
```

---

## คำสั่งทั้งหมด

| คำสั่ง | คำอธิบาย |
|--------|---------|
| `status` | ดูสถานะคิวทั้งหมด |
| `add <story-id> -c <chapters>` | เพิ่มเรื่องใหม่ |
| `progress <story-id>` | ดู progress ของเรื่อง |
| `resume` | Resume งานที่ค้าง |
| `list` | ดูรายการงานที่รอ |
| `start` | เริ่ม auto-resume worker |

---

## ตัวอย่างการใช้งาน

### เพิ่มนิยายเรื่องใหม่

```bash
# เพิ่มเรื่อง 36 ตอน
python novel_queue.py add "my-novel" -c 36

# เพิ่มเรื่องพร้อม outline
python novel_queue.py add "my-novel" -c 36 -o "/path/to/outline.md"

# เริ่มจากตอนที่ 10 (เขียนตอน 1-9 ไปแล้ว)
python novel_queue.py add "my-novel" -c 36 -s 10
```

### Resume งานที่ค้าง

```bash
# Resume ทุกงานที่ติด rate limit หรือ fail
python novel_queue.py resume
```

### เริ่ม Worker

```bash
# Default (n8n localhost, check ทุก 30 วินาที)
python novel_queue.py start

# Custom settings
python novel_queue.py start --n8n-url "http://192.168.1.100:5678" --interval 60
```

---

## โครงสร้างระบบ

```
agents/queue/
├── job_queue.py      # Core queue system + Rate Limiter
├── auto_resume.py    # Auto-resume worker
├── novel_queue.py    # CLI tool
├── data/
│   ├── jobs.json     # เก็บ state ของงานทั้งหมด
│   └── auto_resume.log
└── README.md
```

---

## สถานะของงาน

| สถานะ | คำอธิบาย |
|-------|---------|
| `pending` | รอดำเนินการ |
| `in_progress` | กำลังทำ |
| `completed` | เสร็จแล้ว |
| `failed` | ล้มเหลว (retry ครบแล้ว) |
| `rate_limited` | รอ rate limit หมด |
| `paused` | หยุดชั่วคราว |

---

## Rate Limit Settings

```python
# Default settings (ปรับได้ใน job_queue.py)
requests_per_minute = 40  # Claude API limit
tokens_per_minute = 100000
```

---

## Retry Logic

1. **Rate Limit**: รอ 60 วินาที แล้ว retry อัตโนมัติ
2. **API Error**: retry สูงสุด 3 ครั้ง (exponential backoff)
3. **Content ไม่ครบ**: retry โดยอัตโนมัติ
4. **Fail ครบ 3 ครั้ง**: หยุด แจ้งเตือน (ใช้ `resume` เพื่อ retry ใหม่)

---

## Integration กับ n8n

Worker จะเรียก n8n webhooks:

| Job Type | Webhook |
|----------|---------|
| write_chapter | `/webhook/chapter-writer` |
| create_character | `/webhook/character-generator` |
| create_plot | `/webhook/plot-outliner` |
| qc_check | `/webhook/qc-scorer` |

ต้องแน่ใจว่า n8n workflows มี webhooks เหล่านี้ active

---

## Tips

### รัน Worker เป็น Background

```bash
# Linux/Mac
nohup python novel_queue.py start > worker.log 2>&1 &

# หรือใช้ screen/tmux
screen -S novel-worker
python novel_queue.py start
# Ctrl+A, D เพื่อ detach
```

### ดู Log

```bash
tail -f data/auto_resume.log
```

### Reset งานที่ fail ทั้งหมด

```bash
python novel_queue.py resume
```
