# n8n Novel Writing System

ระบบเขียนนิยายอัตโนมัติด้วย n8n และ Multi-AI

## Overview

ระบบนี้ออกแบบมาสำหรับเขียนนิยายปริมาณมากด้วย automation:
- 10-15 เรื่องพร้อมกัน
- หลาย AI models (Gemini, GPT, Claude)
- Multi-layer QC system
- Scheduled batch writing

## Quick Start

### 1. Setup Environment

```bash
# Copy environment file
cp .env.example .env

# Edit .env with your API keys
nano .env
```

### 2. Start Docker

```bash
# Start n8n and PostgreSQL
docker-compose up -d

# Check status
docker-compose ps
```

### 3. Access n8n

เปิด browser: http://localhost:5678

Login ด้วย credentials ใน .env

### 4. Import Workflows

1. ไปที่ n8n UI
2. Import workflows จาก `n8n-data/workflows/`
3. Configure credentials สำหรับ AI APIs

## โครงสร้างโฟลเดอร์

```
n8n-novels/
├── docker-compose.yml         # Docker configuration
├── .env.example               # Environment template
├── README.md                  # ไฟล์นี้
├── n8n-data/
│   └── workflows/             # n8n workflow JSONs
├── database/
│   └── init.sql              # Database schema
├── stories/                   # นิยายแต่ละเรื่อง
│   └── [project-id]/
│       ├── config.json
│       ├── characters.json
│       ├── outline.txt
│       ├── chapters/
│       └── metadata.json
├── templates/                 # Templates
├── prompts/                   # AI prompts
│   ├── character-generation/
│   ├── plot-outlining/
│   ├── chapter-writing/
│   └── quality-control/
├── outputs/                   # Export outputs
│   ├── daily/
│   ├── weekly/
│   └── exports/
├── logs/                      # Logs
└── scripts/                   # Helper scripts
    ├── setup_project.py
    ├── monitor_dashboard.py
    ├── backup_all.py
    └── export_batch.py
```

## Scripts

### สร้างโปรเจคใหม่
```bash
python scripts/setup_project.py "ชื่อเรื่อง" --genre romantic-comedy --chapters 20
```

Available genres:
- romantic-comedy
- fantasy
- horror
- mystery
- bl-gl

### Monitor Dashboard
```bash
# แสดง dashboard
python scripts/monitor_dashboard.py

# Watch mode (refresh ทุก 60 วินาที)
python scripts/monitor_dashboard.py --watch
```

### Backup
```bash
# Create backup
python scripts/backup_all.py create

# List backups
python scripts/backup_all.py list

# Cleanup old backups
python scripts/backup_all.py cleanup --keep-days 30
```

### Export
```bash
# Export all projects
python scripts/export_batch.py all --format txt epub

# Export single project
python scripts/export_batch.py single project-id --format txt
```

## Workflows

| # | Workflow | หน้าที่ |
|---|----------|---------|
| 1 | character-generator | สร้างตัวละคร |
| 2 | plot-outliner | วางโครงเรื่อง |
| 3 | chapter-writer-gemini | เขียนบทด้วย Gemini |
| 4 | chapter-writer-gpt | เขียนบทด้วย GPT |
| 5 | chapter-writer-claude | เขียนบทด้วย Claude |
| 6 | qc-basic | ตรวจ QC พื้นฐาน |
| 7 | qc-ai-scorer | ให้คะแนนด้วย AI |
| 8 | qc-deep-check | ตรวจละเอียด |
| 9 | batch-writer | เขียนหลายเรื่องพร้อมกัน |
| 10 | daily-scheduler | ตั้งเวลาเขียนรายวัน |
| 11 | weekly-publisher | รวมและ export รายสัปดาห์ |
| 12 | analytics-reporter | รายงานสถิติ |

## QC System

### Layer 1: Basic Checks
- ความยาว (3000-6000 คำ)
- ไม่มี placeholder
- Format ถูกต้อง

### Layer 2: AI Scoring (Gemini)
- Quick scan
- คะแนน 0-100

### Layer 3: Deep Check (Claude Haiku)
- Grammar
- Character consistency
- Plot coherence

### Layer 4: Expert Review (GPT-4o)
- เฉพาะกรณีคะแนนต่ำ

### Layer 5: Human Review
- Flag ให้ตรวจเอง

## AI Models Usage

| Genre | Primary | Backup |
|-------|---------|--------|
| Romantic Comedy | Gemini | GPT-4o-mini |
| Fantasy | GPT-4o | Claude Haiku |
| Horror | Claude Haiku | GPT-4o |
| Mystery | GPT-4o | Claude Haiku |
| BL/GL | Claude Haiku | Gemini |

## Maintenance

### ตรวจ Logs
```bash
docker logs n8n-novels
docker logs n8n-postgres
```

### Restart Services
```bash
docker-compose restart
```

### Database Access
```bash
docker exec -it n8n-postgres psql -U n8n -d n8n_novels
```

## Troubleshooting

### n8n ไม่ start
```bash
docker-compose down
docker-compose up -d
docker logs n8n-novels
```

### Database connection error
```bash
docker-compose restart postgres
# รอ 10 วินาที
docker-compose restart n8n
```

### API rate limit
- ลด parallelism ใน batch workflow
- เพิ่ม delay ระหว่าง requests
- Switch to backup AI model

## KPIs

- Chapters/day: 10-15
- Average quality: ≥ 75/100
- Auto-approval rate: ≥ 80%
- API cost/day: $10-25
