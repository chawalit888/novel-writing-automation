# 📘 NOVEL WRITING AUTOMATION SYSTEM - DATA SHEET

**สำหรับ: Claude Code**  
**วันที่สร้าง: 31 มกราคม 2026**  
**เจ้าของโปรเจค: User**

---

## 🎯 PROJECT OVERVIEW

### ภาพรวมโปรเจค
สร้างระบบเขียนนิยายอัตโนมัติ 2 ระบบควบคู่กัน:
1. **Claude Code System** - เน้นคุณภาพสูง, นิยาย premium 3-5 เรื่อง
2. **n8n Multi-AI System** - เน้นปริมาณ, นิยายหลากหลาย 10-15 เรื่อง

### วัตถุประสงค์
- สร้างรายได้จากการเขียนนิยายออนไลน์
- ใช้ AI automation เพื่อเพิ่มประสิทธิภาพ
- มี quality control ที่เข้มงวด
- Scale ได้ตามความต้องการ

### AI Novel Factory Operations (เพิ่มเติม ก.พ. 2026)

เอกสาร operations ฉบับใหม่สำหรับกลยุทธ์ Factory (เป้า 500K-1M บาท/เดือน) อยู่ที่:

| เอกสาร | ที่อยู่ | เนื้อหา |
|--------|-------|---------|
| คู่มือปฏิบัติการ | `ai-factory/ai-factory-operations.md` | สูตรปล่อยเรื่อง, paywall, scale strategy |
| QC Pipeline | `ai-factory/qc-pipeline.md` | ระบบ QC 6 ขั้นตอนก่อนลงแพลตฟอร์ม |
| Story Pipeline | `ai-factory/story-pipeline.md` | ระบบ 4 สถานะติดตามเรื่อง |
| ปฏิทินปล่อยเรื่อง | `ai-factory/publishing-calendar-template.md` | template ปฏิทินรายสัปดาห์/เดือน |
| กลยุทธ์แพลตฟอร์ม | `ai-factory/platform-strategy.md` | Tunwalai หลัก + cross-posting |
| โมเดลรายได้ | `ai-factory/revenue-model.md` | projection + สูตรคำนวณ |
| Template รายงาน QC | `ai-factory/templates/qc-report.md` | template สำหรับรายงาน QC |
| Template สรุปสัปดาห์ | `ai-factory/templates/weekly-review.md` | template review ประจำสัปดาห์ |
| Template แผนดัน | `ai-factory/templates/scale-plan.md` | template วางแผนเรื่อง hit 120-200 ตอน |

---

## 📁 SYSTEM 1: CLAUDE CODE SYSTEM

### จุดประสงค์
เขียนนิยายคุณภาพสูง premium ที่ต้องการความซับซ้อนและ consistency สูง

### โครงสร้างไฟล์

```
/home/user/claude-code-novels/
│
├── README.md                          # ภาพรวมโปรเจค
├── PROJECT_MASTER.md                  # Master plan ทั้งหมด
│
├── projects/                          # โปรเจคนิยายแต่ละเรื่อง
│   ├── story-001-dark-fantasy/
│   │   ├── PROJECT.md                 # รายละเอียดเรื่อง
│   │   ├── characters/                # ข้อมูลตัวละคร
│   │   │   ├── protagonist.json
│   │   │   ├── antagonist.json
│   │   │   └── supporting.json
│   │   ├── world/                     # World building
│   │   │   ├── magic-system.md
│   │   │   ├── locations.md
│   │   │   └── rules.md
│   │   ├── outlines/                  # โครงเรื่อง
│   │   │   ├── master-outline.md      # โครงเรื่องทั้งหมด
│   │   │   ├── arc-1.md               # แต่ละ arc
│   │   │   └── arc-2.md
│   │   ├── chapters/                  # บทนิยาย
│   │   │   ├── chapter-001.txt
│   │   │   ├── chapter-002.txt
│   │   │   └── ...
│   │   ├── metadata/                  # ข้อมูลเสริม
│   │   │   ├── timeline.json          # Timeline เหตุการณ์
│   │   │   ├── relationships.json     # ความสัมพันธ์ตัวละคร
│   │   │   └── progress.json          # ความคืบหน้า
│   │   └── exports/                   # ไฟล์ส่งออก
│   │       ├── full-novel.txt
│   │       ├── epub/
│   │       └── pdf/
│   │
│   ├── story-002-psychological-horror/
│   │   └── [โครงสร้างเดียวกัน]
│   │
│   └── story-003-premium-bl/
│       └── [โครงสร้างเดียวกัน]
│
├── skills/                            # Custom skills สำหรับนิยาย
│   ├── novel-writer/
│   │   ├── SKILL.md                   # วิธีเขียนนิยายคุณภาพสูง
│   │   └── prompts/                   # Prompt templates
│   │       ├── chapter-writing.txt
│   │       ├── dialogue.txt
│   │       └── action-scene.txt
│   │
│   ├── character-creator/
│   │   ├── SKILL.md                   # วิธีสร้างตัวละคร
│   │   └── templates/
│   │       ├── protagonist.json
│   │       └── supporting.json
│   │
│   ├── plot-manager/
│   │   ├── SKILL.md                   # วิธีจัดการโครงเรื่อง
│   │   └── templates/
│   │       ├── three-act.md
│   │       └── heros-journey.md
│   │
│   └── consistency-checker/
│       ├── SKILL.md                   # ตรวจความสอดคล้อง
│       └── rules/
│           ├── character-rules.json
│           └── world-rules.json
│
├── templates/                         # Template สำหรับแนวต่างๆ
│   ├── romantic-comedy/
│   │   ├── structure.md
│   │   └── character-archetypes.json
│   ├── fantasy/
│   │   ├── structure.md
│   │   └── world-template.json
│   └── horror/
│       ├── structure.md
│       └── atmosphere-guide.md
│
├── tools/                             # Scripts ช่วยเหลือ
│   ├── consistency-checker.py         # ตรวจสอบความสอดคล้อง
│   ├── export-manager.py              # จัดการ export
│   ├── stats-tracker.py               # ติดตามสถิติ
│   └── backup-manager.py              # สำรองข้อมูล
│
└── docs/                              # เอกสารประกอบ
    ├── workflow-guide.md              # คู่มือการทำงาน
    ├── best-practices.md              # Best practices
    └── troubleshooting.md             # แก้ปัญหา
```

### Workflow การทำงาน

#### 1. Setup โปรเจคใหม่
```bash
# User สั่ง Claude Code:
"สร้างโปรเจคนิยายแฟนตาซีใหม่ ชื่อ Dark Empire 
โดยมีระบบ magic ที่ซับซ้อน และตัวละคร 5 คน"

# Claude Code จะทำ:
1. อ่าน skill: /skills/novel-writer/SKILL.md
2. อ่าน template: /templates/fantasy/
3. สร้างโฟลเดอร์ projects/dark-empire/
4. สร้าง PROJECT.md พร้อมรายละเอียด
5. สร้าง characters/ พร้อมตัวละคร 5 คน
6. สร้าง world/magic-system.md
7. สร้าง outlines/master-outline.md (20-30 ตอน)
8. แจ้งเสร็จพร้อมสรุป
```

#### 2. เขียนบทนิยาย
```bash
# User สั่ง:
"เขียนบทที่ 5 ของ Dark Empire 
ตามโครงเรื่องที่วางไว้ โดยเน้นการพัฒนาตัวละครหลัก
และแสดง magic system ให้ชัดเจน"

# Claude Code จะทำ:
1. อ่าน PROJECT.md
2. อ่าน characters/*.json ทั้งหมด
3. อ่าน world/magic-system.md
4. อ่าน outlines/master-outline.md
5. อ่าน chapters/chapter-004.txt (บทก่อนหน้า)
6. อ่าน metadata/timeline.json
7. เขียนบทใหม่ 4000-6000 คำ
8. ตรวจสอบ consistency ด้วย consistency-checker
9. บันทึก chapters/chapter-005.txt
10. อัพเดท metadata/timeline.json
11. อัพเดท metadata/progress.json
12. แจ้งเสร็จพร้อมสรุปสั้นๆ
```

#### 3. ตรวจสอบและแก้ไข
```bash
# User สั่ง:
"ตรวจสอบ consistency ของบท 1-5 
และแก้ไขข้อผิดพลาดที่พบ"

# Claude Code จะทำ:
1. รัน consistency-checker.py
2. ตรวจสอบ:
   - ตัวละครทำตัวสอดคล้องหรือไม่
   - Timeline ถูกต้องหรือไม่
   - Magic system ใช้ถูกต้องหรือไม่
   - Location ถูกต้องหรือไม่
3. สร้างรายงาน issues.md
4. แก้ไขปัญหาที่พบ
5. แจ้งรายการที่แก้แล้ว
```

#### 4. Export และ Publish
```bash
# User สั่ง:
"รวมบท 1-10 เป็นไฟล์เดียว และ export เป็น EPUB"

# Claude Code จะทำ:
1. รวมไฟล์ chapters/chapter-001 ถึง 010
2. จัด format ให้สวยงาม
3. สร้าง exports/full-novel-part1.txt
4. ใช้ tool สร้าง EPUB
5. บันทึกใน exports/epub/
6. แจ้งเสร็จพร้อมลิงก์ดาวน์โหลด
```

### แนวเรื่องที่เหมาะกับ Claude Code

1. **Dark Fantasy / Cultivation**
   - ระบบ magic/power ซับซ้อน
   - World building ลึก
   - ต้องการ consistency สูง

2. **Psychological Horror**
   - บรรยากาศละเอียด
   - Character depth สูง
   - Tension building แบบค่อยเป็นค่อยไป

3. **Premium BL/GL**
   - Emotional depth สูง
   - Relationship development ละเอียด
   - Sensitive content handling

4. **Mystery/Detective**
   - Timeline ซับซ้อน
   - Clue placement แม่นยำ
   - Plot twists วางแผนมาดี

5. **Sci-Fi**
   - Technology/science ต้องสมเหตุสมผล
   - World building ซับซ้อน
   - Concept ใหม่ๆ

### KPIs และเป้าหมาย

**คุณภาพ:**
- Overall quality score: ≥ 85/100
- Character consistency: ≥ 90/100
- Plot coherence: ≥ 90/100
- Reader satisfaction: ≥ 4.5/5 stars

**ปริมาณ:**
- Stories: 3-5 เรื่องพร้อมกัน
- Chapters/week: 7-10 บท
- Words/chapter: 4000-6000 คำ
- Completion time/story: 2-3 เดือน

**รายได้เป้าหมาย:**
- Price/chapter: 100-200 บาท
- Chapters/story: 20-30 บท
- Revenue/story: 8,000-15,000 บาท
- Total/month (3 stories): 25,000-45,000 บาท

### ต้นทุน

**API Costs:**
- Claude Sonnet 4: ~$3/1M input tokens
- Claude Opus 4.5: ~$15/1M input tokens
- ประมาณการ: 50,000-80,000 บาท/เดือน (1,500-2,500 USD)

**เหตุผลที่แพง:**
- เขียนละเอียด ใช้ context เยอะ
- ตรวจสอบ consistency หลายรอบ
- คุณภาพสูงสุด

**การลดต้นทุน:**
- ใช้ Sonnet สำหรับงานทั่วไป
- ใช้ Opus เฉพาะบทสำคัญ
- Cache context ที่ใช้บ่อยๆ

---

## 🤖 SYSTEM 2: n8n MULTI-AI SYSTEM

### จุดประสงค์
เขียนนิยายปริมาณมาก หลายแนว automation 100%

### โครงสร้างไฟล์

```
/home/user/n8n-novels/
│
├── docker-compose.yml                 # n8n + PostgreSQL setup
├── .env                               # Environment variables
├── README.md
│
├── n8n-data/                          # n8n workflows
│   ├── workflows/
│   │   ├── 01-character-generator.json
│   │   ├── 02-plot-outliner.json
│   │   ├── 03-chapter-writer-gemini.json
│   │   ├── 04-chapter-writer-gpt.json
│   │   ├── 05-chapter-writer-claude.json
│   │   ├── 06-qc-basic.json
│   │   ├── 07-qc-ai-scorer.json
│   │   ├── 08-qc-deep-check.json
│   │   ├── 09-batch-writer.json       # เขียนหลายเรื่องพร้อมกัน
│   │   ├── 10-daily-scheduler.json
│   │   ├── 11-weekly-publisher.json
│   │   └── 12-analytics-reporter.json
│   │
│   └── credentials/
│       ├── gemini-api.json
│       ├── openai-api.json
│       ├── claude-api.json
│       └── telegram-bot.json
│
├── database/                          # SQLite/PostgreSQL
│   └── novels.db
│
├── stories/                           # นิยายแต่ละเรื่อง
│   ├── romantic-001/
│   │   ├── config.json                # การตั้งค่าเรื่อง
│   │   ├── characters.json
│   │   ├── outline.txt
│   │   ├── chapters/
│   │   │   ├── ch-001.txt
│   │   │   └── ...
│   │   └── metadata.json
│   │
│   ├── romantic-002/
│   ├── fantasy-001/
│   ├── horror-001/
│   ├── bl-001/
│   └── ... (10-15 เรื่อง)
│
├── templates/                         # Templates สำหรับแนวต่างๆ
│   ├── romantic-comedy/
│   │   ├── config-template.json
│   │   ├── character-template.json
│   │   └── prompts.json
│   ├── fantasy/
│   ├── horror/
│   ├── mystery/
│   └── bl-gl/
│
├── prompts/                           # AI Prompts
│   ├── character-generation/
│   │   ├── romantic.txt
│   │   ├── fantasy.txt
│   │   └── horror.txt
│   ├── plot-outlining/
│   ├── chapter-writing/
│   │   ├── opening.txt
│   │   ├── middle.txt
│   │   └── climax.txt
│   └── quality-control/
│       ├── grammar-check.txt
│       ├── consistency-check.txt
│       └── scoring.txt
│
├── outputs/                           # ผลลัพธ์รวม
│   ├── daily/                         # บทที่เขียนแต่ละวัน
│   │   ├── 2026-01-31/
│   │   └── 2026-02-01/
│   ├── weekly/                        # รวมบททุกสัปดาห์
│   │   ├── week-01/
│   │   └── week-02/
│   └── exports/                       # ไฟล์ส่งออก
│       ├── epub/
│       ├── pdf/
│       └── txt/
│
├── logs/                              # Logs
│   ├── execution-logs/
│   ├── error-logs/
│   └── qc-reports/
│
├── scripts/                           # Helper scripts
│   ├── setup-project.py               # สร้างโปรเจคใหม่
│   ├── monitor-dashboard.py           # Dashboard แสดงสถานะ
│   ├── backup-all.py                  # Backup
│   └── export-batch.py                # Export หลายเรื่อง
│
└── docs/
    ├── setup-guide.md                 # คู่มือติดตั้ง
    ├── workflow-docs/                 # เอกสาร workflows
    ├── api-usage-guide.md
    └── troubleshooting.md
```

### Database Schema

```sql
-- Projects table
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    genre TEXT NOT NULL,
    status TEXT DEFAULT 'active',
    ai_model TEXT NOT NULL,
    target_chapters INTEGER,
    current_chapter INTEGER DEFAULT 0,
    schedule TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Characters table
CREATE TABLE characters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT NOT NULL,
    character_name TEXT NOT NULL,
    role TEXT,
    personality TEXT,
    background TEXT,
    data JSON,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

-- Chapters table
CREATE TABLE chapters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT NOT NULL,
    chapter_number INTEGER NOT NULL,
    title TEXT,
    word_count INTEGER,
    ai_model TEXT,
    status TEXT DEFAULT 'draft',
    filepath TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

-- Quality scores table
CREATE TABLE quality_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chapter_id INTEGER NOT NULL,
    overall_score INTEGER,
    grammar_score INTEGER,
    character_score INTEGER,
    plot_score INTEGER,
    emotion_score INTEGER,
    genre_score INTEGER,
    issues JSON,
    suggestions JSON,
    reviewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chapter_id) REFERENCES chapters(id)
);

-- Execution logs table
CREATE TABLE execution_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    workflow_name TEXT,
    project_id TEXT,
    status TEXT,
    duration_seconds INTEGER,
    api_cost_usd REAL,
    error_message TEXT,
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### n8n Workflows รายละเอียด

#### Workflow 1: Character Generator

**หน้าที่:** สร้างตัวละครสำหรับเรื่องใหม่

**Nodes:**
1. Manual Trigger - เริ่มต้นด้วยมือ
2. Get Project Info - ดึงข้อมูลโปรเจคจาก database
3. Load Character Template - โหลด template ตามแนวเรื่อง
4. Load Prompt - โหลด prompt สำหรับสร้างตัวละคร
5. Generate with Claude - เรียก Claude API สร้างตัวละคร
6. Parse JSON Response - แปลง response เป็น structured data
7. Save to Database - บันทึกลง characters table
8. Save to File - บันทึกเป็น JSON file
9. Send Notification - แจ้งเตือนผ่าน Telegram

#### Workflow 2: Plot Outliner

**หน้าที่:** วางโครงเรื่องทั้งหมด

**Nodes:**
1. Manual Trigger
2. Get Project Info
3. Get Characters - ดึงตัวละครที่สร้างแล้ว
4. Load Plot Template - โหลด template โครงเรื่อง
5. Generate with Claude - สร้างโครงเรื่อง 20-30 ตอน
6. Parse Outline - แยกเป็นตอนๆ
7. Save to File - บันทึก outline.txt
8. Update Database - อัพเดทสถานะโปรเจค
9. Send Notification

#### Workflow 3: Daily Batch Writer

**หน้าที่:** เขียนหลายเรื่องพร้อมกัน ทุกวัน

**Schedule:** 9:00 AM, 2:00 PM, 8:00 PM

**Nodes:**
1. Schedule Trigger - เริ่มอัตโนมัติตามเวลา
2. Get Active Projects - ดึงเรื่องที่กำลังเขียน (LIMIT 5)
3. Split into Batches - แบ่งเป็น batches รันพร้อมกัน
4. Load Project Data - โหลด characters, outline, previous chapters
5. Route by AI Model - เลือก AI ตามการตั้งค่า
6. Write with Gemini/GPT/Claude - เขียนบท
7. Basic QC Check - ตรวจพื้นฐาน (length, format)
8. AI Quality Scorer - ให้คะแนนคุณภาพ
9. Quality Decision - ตัดสินใจว่า pass หรือไม่
10. Save Chapter - บันทึกถ้า pass
11. Regenerate - เขียนใหม่ถ้าไม่ pass
12. Flag for Review - แจ้งเตือนถ้าต้องตรวจเอง
13. Update Database - อัพเดทความคืบหน้า
14. Send Notification - แจ้งผลสรุป

#### Workflow 4: QC System

**หน้าที่:** ตรวจสอบคุณภาพแบบ multi-layer

**Layer 1: Basic Checks**
- ความยาว (2000-8000 คำ)
- ตรวจซ้ำซ้อน
- ตรวจ placeholder
- ตรวจ format

**Layer 2: AI Scoring (Gemini Free)**
- Quick scan
- คะแนนคร่าวๆ 0-100

**Layer 3: Deep Check (Claude Haiku)**
- Grammar analysis
- Character consistency
- Plot coherence
- Emotional depth
- Genre appropriateness

**Layer 4: Expert Review (GPT-4o)**
- ใช้เฉพาะกรณีคะแนนต่ำ
- Deep analysis
- Detailed suggestions

**Layer 5: Human Review**
- Flag ถ้า AI ทุกตัวให้คะแนนต่ำ
- แจ้งเตือนให้ตรวจเอง

#### Workflow 5: Weekly Publisher

**หน้าที่:** รวบรวมและ export บทประจำสัปดาห์

**Schedule:** ทุกวันอาทิตย์ 8:00 PM

**Nodes:**
1. Schedule Trigger
2. Get This Week's Chapters - ดึงบททุกบทที่เขียนในสัปดาห์นี้
3. Group by Story - จัดกลุ่มตามเรื่อง
4. Format Chapters - จัด format สวยงาม
5. Export TXT - สร้างไฟล์ .txt
6. Export EPUB - สร้างไฟล์ .epub (ใช้ pandoc/calibre)
7. Export PDF - สร้างไฟล์ .pdf
8. Upload to Google Drive - อัพโหลดเก็บ
9. Send Summary - ส่งสรุปผ่าน Telegram
10. Update Analytics - อัพเดทสถิติ

### Configuration Files

#### config.json (สำหรับแต่ละเรื่อง)

```json
{
  "project_id": "romantic-001",
  "title": "รักนี้ที่คาเฟ่",
  "genre": "romantic-comedy",
  "ai_model": "gemini",
  "backup_ai_model": "gpt-4o-mini",
  
  "target_chapters": 20,
  "words_per_chapter": {
    "min": 3000,
    "target": 4000,
    "max": 6000
  },
  
  "schedule": {
    "frequency": "daily",
    "time": "09:00",
    "timezone": "Asia/Bangkok"
  },
  
  "quality_thresholds": {
    "auto_approve": 75,
    "manual_review": 70,
    "auto_regenerate": 60
  },
  
  "tags": ["โรแมนติก", "คอมเมดี้", "ชีวิตประจำวัน"],
  
  "price_per_chapter": 30,
  "target_platform": ["ookbee", "meb", "personal-site"],
  
  "metadata": {
    "created_at": "2026-01-31",
    "author": "AI Writer",
    "cover_image": "/assets/romantic-001-cover.jpg",
    "description": "เรื่องราวความรักที่เริ่มต้นในร้านกาแฟเล็กๆ..."
  }
}
```

#### docker-compose.yml

```yaml
version: '3.8'

services:
  n8n:
    image: n8nio/n8n:latest
    container_name: n8n
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=${N8N_USER}
      - N8N_BASIC_AUTH_PASSWORD=${N8N_PASSWORD}
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=${POSTGRES_DB}
      - DB_POSTGRESDB_USER=${POSTGRES_USER}
      - DB_POSTGRESDB_PASSWORD=${POSTGRES_PASSWORD}
      - N8N_ENCRYPTION_KEY=${N8N_ENCRYPTION_KEY}
    volumes:
      - ./n8n-data:/home/node/.n8n
      - ./stories:/stories
      - ./templates:/templates
      - ./prompts:/prompts
      - ./outputs:/outputs
    depends_on:
      - postgres

  postgres:
    image: postgres:15-alpine
    container_name: n8n-postgres
    restart: unless-stopped
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  postgres-data:
```

#### .env (Environment Variables)

```env
# n8n Configuration
N8N_USER=admin
N8N_PASSWORD=change_this_secure_password
N8N_ENCRYPTION_KEY=change_this_to_random_string

# Database
POSTGRES_DB=n8n
POSTGRES_USER=n8n
POSTGRES_PASSWORD=change_this_db_password

# AI API Keys
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Notification
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Budget Controls
DAILY_API_BUDGET_USD=10
MONTHLY_API_BUDGET_USD=300
ALERT_THRESHOLD_PERCENT=80
```

### แนวเรื่องและการตั้งค่า AI

```json
{
  "genres": {
    "romantic-comedy": {
      "ai_model": "gemini",
      "temperature": 0.7,
      "min_quality_score": 70,
      "focus": ["dialogue", "chemistry", "humor"],
      "prompts": {
        "character": "สร้างตัวละครสำหรับนิยายโรแมนติกคอมเมดี้ มีเสน่ห์ น่ารัก มีจุดเด่นชัดเจน",
        "chapter": "เขียนบทนิยายโรแมนติกคอมเมดี้ เน้นบทสนทนาสนุก มีเคมีระหว่างตัวละคร และมีตลกขบขัน"
      }
    },
    "fantasy": {
      "ai_model": "gpt-4o",
      "temperature": 0.6,
      "min_quality_score": 75,
      "focus": ["world-building", "consistency", "power-system"],
      "prompts": {
        "character": "สร้างตัวละครสำหรับนิยายแฟนตาซี มี background ชัดเจน มีพลังพิเศษ และมีการพัฒนาตัวละคร",
        "chapter": "เขียนบทนิยายแฟนตาซี ต้องสอดคล้องกับ world building และ power system ที่กำหนด"
      }
    },
    "horror": {
      "ai_model": "claude-haiku",
      "temperature": 0.5,
      "min_quality_score": 75,
      "focus": ["atmosphere", "tension", "pacing"],
      "prompts": {
        "character": "สร้างตัวละครสำหรับนิยายสยองขวัญ มี background น่ากลัว หรือมีความลับ",
        "chapter": "เขียนบทนิยายสยองขวัญ สร้างบรรยากาศน่ากลัว สร้าง tension ค่อยเป็นค่อยไป ไม่ใช้ jump scare มากเกินไป"
      }
    },
    "mystery": {
      "ai_model": "gpt-4o",
      "temperature": 0.4,
      "min_quality_score": 80,
      "focus": ["logic", "clues", "timeline"],
      "prompts": {
        "character": "สร้างตัวละครสำหรับนิยายสืบสวน แต่ละคนต้องมี motive, alibi, และความลับ",
        "chapter": "เขียนบทนิยายสืบสวน ต้องมีเบาะแสที่ subtle และ timeline ต้องสอดคล้อง"
      }
    },
    "bl-gl": {
      "ai_model": "claude-haiku",
      "temperature": 0.6,
      "min_quality_score": 70,
      "focus": ["relationship", "emotion", "chemistry"],
      "prompts": {
        "character": "สร้างตัวละครสำหรับนิยาย BL/GL มีบุคลิกชัดเจน มี chemistry ระหว่างกัน",
        "chapter": "เขียนบทนิยาย BL/GL เน้นการพัฒนาความสัมพันธ์ มีอารมณ์ความรู้สึก และ chemistry ที่ดี"
      }
    }
  }
}
```

### Schedule Templates

```json
{
  "schedules": {
    "high_volume": {
      "description": "เขียนเยอะมาก 15 เรื่อง/วัน",
      "batches": [
        {
          "time": "09:00",
          "stories": 5,
          "ai_distribution": {
            "gemini": 3,
            "gpt-4o-mini": 2
          }
        },
        {
          "time": "14:00",
          "stories": 5,
          "ai_distribution": {
            "gemini": 3,
            "gpt-4o-mini": 2
          }
        },
        {
          "time": "20:00",
          "stories": 5,
          "ai_distribution": {
            "claude-haiku": 3,
            "gpt-4o-mini": 2
          }
        }
      ],
      "estimated_cost_per_day": "$15-25",
      "total_chapters_per_day": 15,
      "total_words_per_day": "45,000-75,000"
    },
    "balanced": {
      "description": "สมดุล 10 เรื่อง/วัน",
      "batches": [
        {
          "time": "09:00",
          "stories": 5,
          "ai_distribution": {
            "gemini": 5
          }
        },
        {
          "time": "14:00",
          "stories": 5,
          "ai_distribution": {
            "gpt-4o": 2,
            "claude-haiku": 3
          }
        }
      ],
      "estimated_cost_per_day": "$10-15",
      "total_chapters_per_day": 10,
      "total_words_per_day": "30,000-50,000"
    },
    "budget": {
      "description": "ประหยัด 5 เรื่อง/วัน",
      "batches": [
        {
          "time": "09:00",
          "stories": 5,
          "ai_distribution": {
            "gemini": 5
          }
        }
      ],
      "estimated_cost_per_day": "$0-5",
      "total_chapters_per_day": 5,
      "total_words_per_day": "15,000-25,000"
    }
  }
}
```

### KPIs และเป้าหมาย

**ปริมาณ:**
- Active stories: 10-15 เรื่อง
- Chapters/day: 10-15 บท
- Words/day: 40,000-60,000 คำ
- Automation rate: ≥ 90%

**คุณภาพ:**
- Average quality score: ≥ 75/100
- Auto-approval rate: ≥ 80%
- Manual review needed: ≤ 20%
- Regeneration rate: ≤ 10%

**รายได้เป้าหมาย:**
- Price/chapter: 30-50 บาท
- Chapters/story: 20 บท
- Revenue/story: 600-1,000 บาท
- Total/month (10 stories completed): 6,000-10,000 บาท

**ต้นทุน:**
- Gemini: ฟรี (ใน quota) + $5-10 (เกิน quota)
- GPT-4o mini: $5-10/เดือน
- Claude Haiku: $5-10/เดือน
- VPS: $10/เดือน
- **รวม: $20-40/เดือน (600-1,200 บาท)**

---

## 🔄 INTEGRATION BETWEEN SYSTEMS

### การทำงานร่วมกัน

**Shared Resources:**
```
/home/user/shared/
├── templates/          # ใช้ร่วมกันทั้ง 2 ระบบ
├── prompts/            # ใช้ร่วมกันทั้ง 2 ระบบ
├── tools/              # Scripts ที่ใช้ร่วมกัน
└── backups/            # Backup ทั้ง 2 ระบบ
```

### Workflow Integration Scenarios

#### Scenario 1: เรื่องเดียวกัน 2 เวอร์ชัน (A/B Testing)

```
[เรื่อง: "Dark Fantasy Empire"]
         ↓
    ┌────┴────┐
    ↓         ↓
Version A   Version B
(Claude     (n8n
 Code)       Gemini)
    ↓         ↓
Premium     Budget
200฿/ตอน    30฿/ตอน
    ↓         ↓
    └────┬────┘
         ↓
A/B Testing Results
→ ดูว่าตลาดชอบแบบไหน
→ Optimize ต่อไป
```

**ขั้นตอน:**
1. สร้างโครงเรื่องและตัวละครใน Claude Code (คุณภาพสูง)
2. Export ข้อมูลไป n8n
3. n8n เขียนแบบ budget version
4. เปรียบเทียบยอดขาย
5. นำ insights ไป improve ทั้ง 2 ระบบ

#### Scenario 2: Pipeline ต่อเนื่อง

```
Step 1: n8n สร้างตัวละคร + โครงเรื่อง (เร็ว)
         ↓
Step 2: Export ไป Claude Code
         ↓
Step 3: Claude Code เขียนบทสำคัญ (1, 10, 20)
         ↓
Step 4: Import กลับ n8n
         ↓
Step 5: n8n เขียนบทกลางๆ (2-9, 11-19)
         ↓
Step 6: Claude Code final polish + climax
```

**ข้อดี:**
- ใช้จุดแข็งของทั้ง 2 ระบบ
- ประหยัดต้นทุน
- คุณภาพดีในส่วนสำคัญ

#### Scenario 3: Quality Upgrade Path

```
Phase 1: n8n เขียนเรื่อง 10 เรื่อง (volume testing)
         ↓
Phase 2: Analytics - ดูว่าเรื่องไหนได้รับความนิยม
         ↓
Phase 3: Top 2-3 stories → ย้ายไป Claude Code
         ↓
Phase 4: Claude Code rewrite เป็น premium version
         ↓
Phase 5: ขายราคาสูงขึ้น (×3-5 เท่า)
```

**ตัวอย่าง:**
- n8n version: 30฿/ตอน × 20 ตอน = 600฿
- Claude Code version: 150฿/ตอน × 25 ตอน = 3,750฿
- ROI: 525% improvement

### Shared Tools

#### 1. backup-all.sh

```bash
#!/bin/bash
# Backup ทั้ง 2 ระบบพร้อมกัน

DATE=$(date +%Y-%m-%d)
BACKUP_DIR="/home/user/shared/backups/$DATE"

echo "🔄 Starting backup process..."
mkdir -p "$BACKUP_DIR"

# Backup Claude Code
echo "📦 Backing up Claude Code projects..."
if [ -d "/home/user/claude-code-novels/projects" ]; then
    cp -r /home/user/claude-code-novels/projects "$BACKUP_DIR/claude-code-projects"
    echo "✅ Claude Code projects backed up"
else
    echo "⚠️  Claude Code projects directory not found"
fi

# Backup n8n stories
echo "📦 Backing up n8n stories..."
if [ -d "/home/user/n8n-novels/stories" ]; then
    cp -r /home/user/n8n-novels/stories "$BACKUP_DIR/n8n-stories"
    echo "✅ n8n stories backed up"
else
    echo "⚠️  n8n stories directory not found"
fi

# Backup n8n database
echo "📦 Backing up n8n database..."
if [ -f "/home/user/n8n-novels/database/novels.db" ]; then
    cp /home/user/n8n-novels/database/novels.db "$BACKUP_DIR/novels.db"
    echo "✅ n8n database backed up"
else
    echo "⚠️  n8n database not found"
fi

# Backup n8n workflows
echo "📦 Backing up n8n workflows..."
if [ -d "/home/user/n8n-novels/n8n-data/workflows" ]; then
    cp -r /home/user/n8n-novels/n8n-data/workflows "$BACKUP_DIR/n8n-workflows"
    echo "✅ n8n workflows backed up"
else
    echo "⚠️  n8n workflows directory not found"
fi

# Compress
echo "🗜️  Compressing backup..."
cd /home/user/shared/backups/
tar -czf "$DATE.tar.gz" "$DATE"
rm -rf "$DATE"

# Keep only last 30 days
echo "🧹 Cleaning old backups..."
find /home/user/shared/backups/ -name "*.tar.gz" -mtime +30 -delete

echo "✅ Backup complete: $DATE.tar.gz"
echo "📊 Backup size: $(du -sh "$DATE.tar.gz" | cut -f1)"
```

**การใช้งาน:**
```bash
# รัน manual
./backup-all.sh

# ตั้ง cron ทุกวันเที่ยงคืน
0 0 * * * /home/user/shared/tools/backup-all.sh
```

#### 2. unified-dashboard.py

```python
#!/usr/bin/env python3
"""
Unified Dashboard
แสดงสถานะทั้ง 2 ระบบในที่เดียว
"""

import os
import json
import sqlite3
from datetime import datetime
from pathlib import Path

def get_claude_code_stats():
    """Get statistics from Claude Code projects"""
    projects_dir = Path("/home/user/claude-code-novels/projects")
    
    stats = {
        "total_projects": 0,
        "total_chapters": 0,
        "total_words": 0,
        "projects": []
    }
    
    if not projects_dir.exists():
        return stats
    
    for project_path in projects_dir.iterdir():
        if not project_path.is_dir():
            continue
            
        stats["total_projects"] += 1
        project_stats = {
            "name": project_path.name,
            "chapters": 0,
            "words": 0
        }
        
        chapters_dir = project_path / "chapters"
        if chapters_dir.exists():
            for chapter_file in chapters_dir.glob("*.txt"):
                project_stats["chapters"] += 1
                try:
                    with open(chapter_file, 'r', encoding='utf-8') as f:
                        words = len(f.read().split())
                        project_stats["words"] += words
                except Exception as e:
                    print(f"Error reading {chapter_file}: {e}")
        
        stats["total_chapters"] += project_stats["chapters"]
        stats["total_words"] += project_stats["words"]
        stats["projects"].append(project_stats)
    
    return stats

def get_n8n_stats():
    """Get statistics from n8n database"""
    db_path = Path("/home/user/n8n-novels/database/novels.db")
    
    if not db_path.exists():
        return {
            "total_projects": 0,
            "total_chapters": 0,
            "total_words": 0,
            "avg_quality_today": 0,
            "chapters_today": 0
        }
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Total active projects
        cursor.execute("SELECT COUNT(*) FROM projects WHERE status='active'")
        total_projects = cursor.fetchone()[0]
        
        # Total chapters
        cursor.execute("SELECT COUNT(*) FROM chapters")
        total_chapters = cursor.fetchone()[0]
        
        # Total words
        cursor.execute("SELECT SUM(word_count) FROM chapters")
        total_words = cursor.fetchone()[0] or 0
        
        # Average quality score today
        cursor.execute("""
            SELECT AVG(overall_score) 
            FROM quality_scores 
            WHERE DATE(reviewed_at) = DATE('now')
        """)
        avg_quality = cursor.fetchone()[0] or 0
        
        # Chapters written today
        cursor.execute("""
            SELECT COUNT(*) 
            FROM chapters 
            WHERE DATE(created_at) = DATE('now')
        """)
        chapters_today = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_projects": total_projects,
            "total_chapters": total_chapters,
            "total_words": total_words,
            "avg_quality_today": round(avg_quality, 1),
            "chapters_today": chapters_today
        }
    except Exception as e:
        print(f"Error reading n8n database: {e}")
        return {
            "total_projects": 0,
            "total_chapters": 0,
            "total_words": 0,
            "avg_quality_today": 0,
            "chapters_today": 0
        }

def print_dashboard():
    """Print unified dashboard"""
    print("\n" + "="*70)
    print(" 📊 NOVEL WRITING EMPIRE - UNIFIED DASHBOARD".center(70))
    print("="*70)
    print(f" 📅 {datetime.now().strftime('%A, %B %d, %Y - %H:%M:%S')}".center(70))
    print("="*70)
    
    # Claude Code Stats
    print("\n🎯 CLAUDE CODE SYSTEM (Premium Quality)")
    print("-"*70)
    claude_stats = get_claude_code_stats()
    print(f" Active Projects:  {claude_stats['total_projects']}")
    print(f" Total Chapters:   {claude_stats['total_chapters']}")
    print(f" Total Words:      {claude_stats['total_words']:,}")
    if claude_stats['total_chapters'] > 0:
        avg_words = claude_stats['total_words'] // claude_stats['total_chapters']
        print(f" Avg Words/Ch:     {avg_words:,}")
    
    if claude_stats['projects']:
        print("\n Projects:")
        for p in claude_stats['projects']:
            print(f"   • {p['name']}: {p['chapters']} chapters, {p['words']:,} words")
    
    # n8n Stats
    print("\n🤖 N8N MULTI-AI SYSTEM (High Volume)")
    print("-"*70)
    n8n_stats = get_n8n_stats()
    print(f" Active Projects:  {n8n_stats['total_projects']}")
    print(f" Total Chapters:   {n8n_stats['total_chapters']}")
    print(f" Total Words:      {n8n_stats['total_words']:,}")
    print(f" Chapters Today:   {n8n_stats['chapters_today']}")
    print(f" Avg Quality:      {n8n_stats['avg_quality_today']}/100 (today)")
    
    # Combined Stats
    print("\n📈 COMBINED STATISTICS")
    print("-"*70)
    total_projects = claude_stats['total_projects'] + n8n_stats['total_projects']
    total_chapters = claude_stats['total_chapters'] + n8n_stats['total_chapters']
    total_words = claude_stats['total_words'] + n8n_stats['total_words']
    
    print(f" Total Projects:   {total_projects}")
    print(f" Total Chapters:   {total_chapters}")
    print(f" Total Words:      {total_words:,}")
    if total_chapters > 0:
        print(f" Avg Words/Ch:     {total_words//total_chapters:,}")
    
    # Revenue Projection
    print("\n💰 REVENUE PROJECTION (if all sold)")
    print("-"*70)
    claude_revenue = claude_stats['total_chapters'] * 150  # 150฿ avg
    n8n_revenue = n8n_stats['total_chapters'] * 40  # 40฿ avg
    total_revenue = claude_revenue + n8n_revenue
    
    print(f" Claude Code Est:  ฿{claude_revenue:,}")
    print(f" n8n Est:          ฿{n8n_revenue:,}")
    print(f" TOTAL POTENTIAL:  ฿{total_revenue:,}")
    
    # Progress Bar
    print("\n📊 PRODUCTIVITY")
    print("-"*70)
    target_chapters_month = 300  # 10 chapters/day × 30 days
    progress = (total_chapters / target_chapters_month) * 100
    bar_length = 40
    filled = int(bar_length * progress / 100)
    bar = "█" * filled + "░" * (bar_length - filled)
    print(f" Monthly Target:   [{bar}] {progress:.1f}%")
    print(f" {total_chapters}/{target_chapters_month} chapters")
    
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    try:
        print_dashboard()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
```

**การใช้งาน:**
```bash
# รัน manual
python3 unified-dashboard.py

# ตั้ง cron ทุกชั่วโมง
0 * * * * /home/user/shared/tools/unified-dashboard.py

# หรือใช้ watch แบบ real-time
watch -n 300 python3 /home/user/shared/tools/unified-dashboard.py
```

#### 3. sync-templates.sh

```bash
#!/bin/bash
# Sync templates ระหว่าง 2 ระบบ

SHARED_TEMPLATES="/home/user/shared/templates"
CLAUDE_TEMPLATES="/home/user/claude-code-novels/templates"
N8N_TEMPLATES="/home/user/n8n-novels/templates"

echo "🔄 Syncing templates..."

# Ensure shared directory exists
mkdir -p "$SHARED_TEMPLATES"

# Copy from Claude Code to shared
if [ -d "$CLAUDE_TEMPLATES" ]; then
    rsync -av --update "$CLAUDE_TEMPLATES/" "$SHARED_TEMPLATES/"
    echo "✅ Synced Claude Code → Shared"
fi

# Copy from shared to n8n
if [ -d "$SHARED_TEMPLATES" ]; then
    mkdir -p "$N8N_TEMPLATES"
    rsync -av --update "$SHARED_TEMPLATES/" "$N8N_TEMPLATES/"
    echo "✅ Synced Shared → n8n"
fi

echo "✅ Template sync complete"
```

---

## 🔧 MCP SERVERS & TOOLS

### MCP Servers ที่ใช้งาน

| MCP Server | Package | หน้าที่ |
|-----------|---------|--------|
| **Google Sheets** | `mcp-google-sheets@latest` | จัดการข้อมูลนิยาย, tracking, analytics |
| **Brave Search** | `@brave/brave-search-mcp-server` | ค้นหาข้อมูล research สำหรับนิยาย |

### การตั้งค่า
- ไฟล์: `.mcp.json` (project root)
- Brave Search API Key: ลงทะเบียนที่ https://brave.com/search/api/ (ฟรี 2,000 queries/เดือน)

### Brave Search MCP ใช้สำหรับ
- Research ประวัติศาสตร์/ยุคสมัย (นิยายย้อนยุค)
- ตรวจสอบข้อเท็จจริง (การแพทย์, กฎหมาย, อาชีพ)
- ศึกษาแนวนิยายใหม่ (genre conventions, tropes)
- หาข้อมูลสถานที่, วัฒนธรรม, ขนบธรรมเนียม

---

## 🧠 SKILLS SYSTEM (Claude Code)

### Skills ทั้งหมด (25 skills)

#### Core Writing Skills (9)
| Skill | ตำแหน่ง | หน้าที่ |
|-------|---------|--------|
| novel-writer | `claude-code-novels/skills/` | เขียนบทนิยาย 4,800-6,000 ตัวอักษร |
| character-creator | `claude-code-novels/skills/` | สร้างตัวละครลึก มีมิติ |
| plot-manager | `claude-code-novels/skills/` | วางโครงเรื่อง 3-act, Hero's Journey |
| world-building | `claude-code-novels/skills/` | สร้างโลก, ระบบ magic, ภูมิศาสตร์ |
| dialogue-master | `claude-code-novels/skills/` | เขียน dialogue มี voice เฉพาะ |
| tension-building | `claude-code-novels/skills/` | สร้าง tension หลายประเภท |
| hook-cliffhanger-specialist | `claude-code-novels/skills/` | สร้าง hook เปิดตอน, cliffhanger จบตอน |
| pacing-analyzer | `claude-code-novels/skills/` | วิเคราะห์จังหวะเรื่อง |
| ending-checker | `claude-code-novels/skills/` | ตรวจสอบตอนจบ |

#### Enhancement & Polish Skills (4)
| Skill | ตำแหน่ง | หน้าที่ |
|-------|---------|--------|
| emotional-scene | `claude-code-novels/skills/` | เขียนฉากอารมณ์ 6 ประเภท |
| consistency-checker | `claude-code-novels/skills/` | ตรวจความสอดคล้องตัวละคร/timeline/world |
| flashback-handler | `claude-code-novels/skills/` | เขียน flashback ไม่สับสน |
| thai-language-polish | `claude-code-novels/skills/` | ขัดเกลาภาษาไทย |

#### Research & Knowledge Skills (4) — ใหม่!
| Skill | ตำแหน่ง | หน้าที่ |
|-------|---------|--------|
| **historical-research** | `claude-code-novels/skills/` | Research ยุคสมัย, ตรวจ anachronism |
| **mystery-crime-plotter** | `claude-code-novels/skills/` | วาง plot คดี, เบาะแส, red herring |
| **genre-adapter** | `claude-code-novels/skills/` | ศึกษาแนวนิยายใหม่, สรุป guideline |
| **fact-checker** | `claude-code-novels/skills/` | ตรวจข้อเท็จจริง (แพทย์/กฎหมาย/อาชีพ) |

#### NC Content Skills (5)
| Skill | ตำแหน่ง | หน้าที่ |
|-------|---------|--------|
| nc-translation-specialist | `novels-nc/nc-automation/skills/` | แปล NC อังกฤษ→ไทย |
| character-chemistry-builder | `novels-nc/nc-automation/skills/` | สร้าง chemistry ระหว่างตัวละคร |
| nc-qc-validator | `novels-nc/nc-automation/skills/` | ตรวจคุณภาพฉาก NC |
| nc-scene-polish | `novels-nc/nc-automation/skills/` | ขัดเกลาฉาก NC |
| scene-integration-handler | `novels-nc/nc-automation/skills/` | ผสาน NC เข้ากับเนื้อเรื่อง |

#### Marketing Skills (2)
| Skill | ตำแหน่ง | หน้าที่ |
|-------|---------|--------|
| teaser-writer | `marketing-team/skills/` | เขียน teaser โซเชียล |
| line-broadcast-writer | `marketing-team/skills/` | เขียน LINE broadcast |

#### Visual (1)
| Skill | ตำแหน่ง | หน้าที่ |
|-------|---------|--------|
| cover-generator | `claude-code-novels/skills/` | สร้าง prompt ปกนิยาย AI |

---

## 📚 KNOWLEDGE BASE

### โครงสร้าง
```
knowledge-base/
├── historical/              # ข้อมูลประวัติศาสตร์
├── medical/                 # ข้อมูลทางการแพทย์
├── crime-legal/             # กฎหมาย/อาชญากรรม
├── genre-guides/            # คู่มือแนวนิยาย
└── profession-industry/     # ข้อมูลอาชีพ/วงการ
```

### วิธีใช้
- Skills ที่เกี่ยวข้อง (historical-research, fact-checker, genre-adapter) จะบันทึกผล research ไว้ที่นี่
- เมื่อเขียนนิยายเรื่องใหม่ ให้ตรวจ Knowledge Base ก่อนว่ามีข้อมูลอยู่แล้วหรือไม่
- ทุกไฟล์ต้องมีแหล่งอ้างอิงและวันที่ research

---

## 📋 IMPLEMENTATION CHECKLIST

### Phase 1: Setup Claude Code (Week 1-2)

**Week 1:**
- [ ] ติดตั้ง Claude Code CLI
- [ ] Setup Anthropic API key
- [ ] สร้างโครงสร้างไดเรกทอรี
  - [ ] /projects
  - [ ] /skills
  - [ ] /templates
  - [ ] /tools
  - [ ] /docs
- [ ] ทดสอบคำสั่งพื้นฐาน
- [ ] เขียน README.md

**Week 2:**
- [ ] สร้าง custom skills
  - [ ] novel-writer skill
  - [ ] character-creator skill
  - [ ] plot-manager skill
  - [ ] consistency-checker skill
- [ ] สร้าง templates สำหรับแนวต่างๆ
  - [ ] romantic-comedy
  - [ ] fantasy
  - [ ] horror
  - [ ] mystery
  - [ ] bl-gl
- [ ] ทดสอบสร้างโปรเจคแรก
- [ ] ทดสอบเขียนบท 1-3
- [ ] Setup backup system

### Phase 2: Setup n8n System (Week 3-4)

**Week 3:**
- [ ] เตรียม VPS/Server
  - [ ] เช่า VPS (2GB+ RAM)
  - [ ] ติดตั้ง Ubuntu 22.04
  - [ ] Setup firewall
  - [ ] Setup SSH keys
- [ ] ติดตั้ง Docker & Docker Compose
- [ ] สร้าง docker-compose.yml
- [ ] สร้าง .env file
- [ ] รัน n8n container
- [ ] Setup PostgreSQL
- [ ] เข้าถึง n8n UI (port 5678)

**Week 4:**
- [ ] สร้าง API credentials ใน n8n
  - [ ] Gemini API
  - [ ] OpenAI API
  - [ ] Anthropic API
  - [ ] Telegram bot
- [ ] สร้าง database schema
- [ ] สร้าง workflows
  - [ ] Character generator
  - [ ] Plot outliner
  - [ ] Chapter writers (Gemini/GPT/Claude)
  - [ ] QC system
  - [ ] Batch writer
  - [ ] Scheduler
  - [ ] Publisher
- [ ] ทดสอบแต่ละ workflow
- [ ] Setup monitoring

### Phase 3: Integration (Week 5)

- [ ] สร้าง /shared directory
- [ ] Setup shared templates
- [ ] สร้าง backup-all.sh
- [ ] สร้าง unified-dashboard.py
- [ ] สร้าง sync-templates.sh
- [ ] ทดสอบ integration scenarios
- [ ] Setup automated backups (cron)
- [ ] เขียน integration documentation

### Phase 4: Production Launch (Week 6+)

**Claude Code:**
- [ ] เริ่มโปรเจคจริง 1 (แฟนตาซี)
- [ ] เริ่มโปรเจคจริง 2 (สยองขวัญ)
- [ ] เริ่มโปรเจคจริง 3 (BL)

**n8n:**
- [ ] เริ่มโปรเจคจริง 5 เรื่อง
  - [ ] 2 โรแมนติก
  - [ ] 1 แฟนตาซี
  - [ ] 1 สยองขวัญ
  - [ ] 1 สืบสวน

**Operations:**
- [ ] Monitor daily
- [ ] Check quality scores
- [ ] Review flagged chapters
- [ ] Track costs
- [ ] Collect analytics
- [ ] Adjust workflows
- [ ] Plan scaling

---

## 💰 BUDGET PLANNING

### Initial Setup Costs

```
VPS (2GB RAM, 50GB SSD):    $10/month
Domain (optional):          $12/year (~$1/month)
SSL Certificate:            Free (Let's Encrypt)
Total Setup:                ~$11/month
```

### Monthly Operating Costs

#### Claude Code System
```
API Costs:
├─ Claude Sonnet 4:         $50-80/month (primary model)
├─ Claude Opus 4.5:         $20-30/month (special chapters)
└─ Context caching:         -$10-15/month (savings)
Total:                      $60-95/month
```

#### n8n System
```
VPS Hosting:                $10/month

API Costs:
├─ Gemini API:
│  ├─ Free tier:            $0 (60 req/min)
│  └─ Paid (overflow):      $5-10/month
├─ OpenAI API:
│  ├─ GPT-4o mini:          $5-10/month
│  └─ GPT-4o:               $5-10/month (occasional)
└─ Claude API:
   └─ Haiku (QC only):      $5-10/month

Total:                      $30-50/month
```

#### Combined Monthly Cost
```
VPS:                        $10
Claude Code API:            $60-95
n8n APIs:                   $20-40
Misc (backup storage):      $5
────────────────────────────
TOTAL:                      $95-150/month
                            (2,850-4,500 บาท)
```

### Revenue Projections

#### Month 1-2 (Starting Phase)
```
Claude Code:
└─ 1 story × 10 chapters × 150฿ = 1,500฿

n8n:
└─ 3 stories × 10 chapters × 40฿ = 1,200฿

Total:                      2,700฿
Costs:                      -3,500฿
Net:                        -800฿ (investment phase)
```

#### Month 3 (Ramping Up)
```
Claude Code:
└─ 2 stories × 20 chapters × 150฿ = 6,000฿

n8n:
└─ 6 stories × 20 chapters × 40฿ = 4,800฿

Total:                      10,800฿
Costs:                      -4,000฿
Net:                        +6,800฿
```

#### Month 6 (Full Operation)
```
Claude Code:
└─ 3 stories × 25 chapters × 175฿ = 13,125฿

n8n:
└─ 10 stories × 25 chapters × 45฿ = 11,250฿

Total:                      24,375฿
Costs:                      -4,500฿
Net:                        +19,875฿
```

#### Month 12 (Mature)
```
Claude Code:
└─ 5 stories × 30 chapters × 200฿ = 30,000฿

n8n:
└─ 15 stories × 30 chapters × 50฿ = 22,500฿

Total:                      52,500฿
Costs:                      -5,000฿
Net:                        +47,500฿
```

**ROI:**
- Month 3: Break even
- Month 6: 400% ROI
- Month 12: 950% ROI

---

## 📊 SUCCESS METRICS & KPIs

### Quality Metrics

**Claude Code:**
```
Overall Quality:            ≥ 85/100
Character Consistency:      ≥ 90/100
Plot Coherence:             ≥ 90/100
Grammar & Style:            ≥ 88/100
Reader Rating:              ≥ 4.5/5 stars
Completion Rate:            ≥ 80% of readers finish
```

**n8n:**
```
Overall Quality:            ≥ 75/100
Character Consistency:      ≥ 80/100
Plot Coherence:             ≥ 80/100
Grammar & Style:            ≥ 78/100
Reader Rating:              ≥ 4.0/5 stars
Auto-Approval Rate:         ≥ 80%
Manual Review Rate:         ≤ 20%
```

### Productivity Metrics

**Claude Code:**
```
Chapters/Week:              7-10
Words/Chapter:              4,000-6,000
Time Investment/Day:        1-2 hours (manual work)
Stories Concurrent:         3-5
```

**n8n:**
```
Chapters/Day:               10-15
Words/Chapter:              3,000-5,000
Automation Rate:            ≥ 90%
Stories Concurrent:         10-15
```

### Financial Metrics

**Revenue:**
```
Monthly Revenue Target:     ≥ 20,000฿ (month 6)
Cost per Chapter:
├─ Claude Code:             60-80฿
└─ n8n:                     8-15฿
Profit Margin:              ≥ 85%
ROI:                        ≥ 400% (month 6)
```

**Growth:**
```
Month-over-Month Growth:    ≥ 20%
New Readers/Month:          ≥ 50
Reader Retention:           ≥ 60%
Repeat Purchase Rate:       ≥ 40%
```

### Operational Metrics

**Uptime & Reliability:**
```
n8n Uptime:                 ≥ 99%
Workflow Success Rate:      ≥ 95%
API Failure Rate:           ≤ 2%
Backup Success Rate:        100%
```

**Quality Control:**
```
Chapters Regenerated:       ≤ 10%
Manual Interventions/Day:   ≤ 3
False Positives (QC):       ≤ 5%
```

---

## 🚨 RISK MANAGEMENT

### Technical Risks

**Risk 1: API Outage**
```
Probability: Medium
Impact: High

Mitigation:
├─ ใช้ multiple AI providers
├─ มี fallback workflows
├─ Cache context สำคัญ
└─ Monitor API status

Recovery Plan:
├─ Switch to backup AI
├─ Use cached data
└─ Resume when service restored
```

**Risk 2: VPS/Server Downtime**
```
Probability: Low
Impact: High

Mitigation:
├─ Daily automated backups
├─ Store backups off-server
├─ Document recovery procedures
└─ Consider redundancy for production

Recovery Plan:
├─ Restore from latest backup
├─ Resume workflows
└─ Verify data integrity
```

**Risk 3: Quality Degradation**
```
Probability: Medium
Impact: Medium

Mitigation:
├─ Multi-layer QC system
├─ Random sampling
├─ Reader feedback loops
└─ Regular prompt optimization

Recovery Plan:
├─ Identify degradation source
├─ Adjust prompts/parameters
├─ Re-run QC on affected chapters
└─ Manual review if needed
```

**Risk 4: Data Loss**
```
Probability: Low
Impact: Critical

Mitigation:
├─ Automated daily backups
├─ Off-site backup storage
├─ Version control for code
└─ Database replication (production)

Recovery Plan:
├─ Restore from latest backup
├─ Verify integrity
└─ Resume operations
```

### Financial Risks

**Risk 1: API Costs Spike**
```
Probability: Medium
Impact: Medium

Mitigation:
├─ Set budget limits in code
├─ Monitor daily usage
├─ Optimize prompts for efficiency
├─ Use cheaper models when possible
└─ Alert at 80% budget

Response:
├─ Switch to cheaper AI models
├─ Reduce volume temporarily
├─ Optimize workflows
└─ Review ROI
```

**Risk 2: Revenue Below Projection**
```
Probability: Medium
Impact: Medium

Mitigation:
├─ Start small (5 stories)
├─ Test market first
├─ A/B test pricing
├─ Diversify platforms
└─ Build email list

Response:
├─ Adjust pricing strategy
├─ Improve quality
├─ Increase marketing
├─ Try different genres
└─ Reduce costs
```

**Risk 3: Platform Policy Changes**
```
Probability: Low
Impact: High

Mitigation:
├─ Publish on multiple platforms
├─ Own website as backup
├─ Build direct audience
├─ Diversify revenue streams
└─ Monitor platform announcements

Response:
├─ Pivot to alternative platforms
├─ Increase own-platform presence
└─ Adjust content if needed
```

### Market Risks

**Risk 1: Reader Preferences Change**
```
Probability: Medium
Impact: Medium

Mitigation:
├─ A/B test different styles
├─ Monitor trends
├─ Flexible genre approach
├─ Gather reader feedback
└─ Quick pivot capability

Response:
├─ Analyze trend data
├─ Adjust content strategy
├─ Test new genres
└─ Optimize for demand
```

**Risk 2: AI Detection Concerns**
```
Probability: Medium
Impact: Medium

Mitigation:
├─ Maintain high quality
├─ Add human editing layer
├─ Transparent about process
├─ Focus on value to readers
└─ Differentiate with quality

Response:
├─ Increase human involvement
├─ Enhance post-processing
├─ Emphasize unique value
└─ Build reader trust
```

**Risk 3: Market Saturation**
```
Probability: Low (short-term)
Impact: Medium

Mitigation:
├─ Focus on niche genres
├─ Build unique brand
├─ Quality over quantity
├─ Direct reader relationships
└─ Continuous innovation

Response:
├─ Find underserved niches
├─ Improve differentiation
├─ Add unique value
└─ Build loyal community
```

---

## 📚 APPENDIX

### A. Example Prompts

#### Character Generation (Fantasy)

```
สร้างตัวละครหลักสำหรับนิยายแฟนตาซี cultivation ในรูปแบบ JSON:

Requirements:
- ชื่อ: [ภาษาไทย, มีความหมาย]
- อายุ: 16-25 ปี
- Cultivation Level: เริ่มต้น (Foundation Building)
- Talent: ปานกลาง (มีอุปสรรคที่ต้องเอาชนะ)
- Personality: กล้าหาญ แต่มีจุดอ่อน
- Background: มีความลับในอดีต
- Motivation: ชัดเจนและน่าเชื่อ
- Character Arc: มีการพัฒนาตัวละคร

Response Format:
{
  "name": "",
  "age": 0,
  "gender": "",
  "cultivation_level": "",
  "talent_grade": "",
  "personality": {
    "traits": [],
    "strengths": [],
    "weaknesses": []
  },
  "background": {
    "origin": "",
    "family": "",
    "secrets": []
  },
  "motivation": "",
  "abilities": [],
  "character_arc": ""
}
```

#### Chapter Writing (Romantic Comedy)

```
เขียนบทที่ {{chapter_number}} ของนิยายโรแมนติกคอมเมดี้

Context:
- เรื่อง: {{title}}
- ตัวละคร: {{characters}}
- โครงเรื่อง: {{outline}}
- บทก่อนหน้า: {{previous_chapter_summary}}

Requirements:
1. ความยาว: 3,500-4,500 คำ
2. โทน: สนุกสนาน ตลกขบขัน อบอุ่น
3. Dialogue: เน้นบทสนทนาที่มีไหวพริบ
4. Chemistry: แสดงความสัมพันธ์ระหว่างตัวละคร
5. Comedy: มี comedy moments 2-3 ครั้ง
6. Romantic Tension: สร้างความตึงเครียงทางโรแมนติก
7. Pacing: จังหวะเหมาะสม ไม่เร็วเกินไป
8. Ending: จบด้วย cliffhanger เบาๆ

โครงสร้าง:
- Opening: ต่อจากบทที่แล้ว
- Development: พัฒนาความสัมพันธ์
- Comedy Moment: ฉากตลก
- Romantic Moment: ฉากโรแมนติก
- Complication: ปัญหาเล็กน้อย
- Resolution: แก้ปัญหาบางส่วน
- Cliffhanger: ทิ้งท้ายให้อยากอ่านต่อ
```

#### Quality Check Prompt

```
ตรวจสอบคุณภาพบทนิยายนี้:

Chapter:
{{chapter_text}}

Genre: {{genre}}
Expected Length: {{expected_length}}

ให้คะแนนและวิเคราะห์ในรูปแบบ JSON:

{
  "overall_score": 0-100,
  "breakdown": {
    "grammar": 0-20,
    "character_consistency": 0-20,
    "plot_coherence": 0-20,
    "emotional_impact": 0-20,
    "genre_appropriateness": 0-20
  },
  "issues": [
    {
      "type": "grammar|character|plot|pacing",
      "severity": "minor|moderate|major",
      "description": "",
      "location": "paragraph X"
    }
  ],
  "strengths": [],
  "suggestions": [],
  "verdict": "approve|review|regenerate"
}

เกณฑ์การตัดสิน:
- 80-100: Auto-approve (ดีเยี่ยม)
- 70-79: Approve with notes (ดี)
- 60-69: Manual review (พอใช้)
- <60: Regenerate (ต้องเขียนใหม่)
```

### B. Troubleshooting Guide

#### n8n Workflow Not Running

**Symptoms:**
- Workflow ไม่เริ่มตาม schedule
- Execution logs ว่างเปล่า

**Solutions:**
1. ตรวจสอบ timezone setting
2. ตรวจสอบ workflow active/inactive status
3. ตรวจสอบ trigger configuration
4. ดู n8n container logs: `docker logs n8n`
5. Restart n8n: `docker-compose restart n8n`

#### API Rate Limit Errors

**Symptoms:**
- "Rate limit exceeded" errors
- Workflows failing intermittently

**Solutions:**
1. ลด parallelism ใน batch processing
2. เพิ่ม delay ระหว่าง requests
3. Switch to backup AI model
4. Upgrade API tier
5. Implement retry logic with exponential backoff

#### Quality Scores Too Low

**Symptoms:**
- Average scores < 70
- Many chapters flagged for review

**Solutions:**
1. Review และ optimize prompts
2. Adjust AI model temperature
3. Provide more context in prompts
4. Add more examples to prompts
5. Consider using higher-tier AI model
6. Review genre-specific guidelines

#### Database Connection Errors

**Symptoms:**
- "Can't connect to database"
- Workflows fail at database steps

**Solutions:**
1. Check PostgreSQL container: `docker ps`
2. Verify credentials in .env
3. Restart database: `docker-compose restart postgres`
4. Check database logs: `docker logs n8n-postgres`
5. Verify database exists: `docker exec -it n8n-postgres psql -U n8n -l`

#### Backup Failures

**Symptoms:**
- Backup script errors
- Missing backup files

**Solutions:**
1. Check disk space: `df -h`
2. Verify directory permissions
3. Check cron logs: `/var/log/syslog`
4. Test script manually: `./backup-all.sh`
5. Verify paths in script

### C. Useful Commands

#### Docker Commands

```bash
# View running containers
docker ps

# View all containers
docker ps -a

# View n8n logs
docker logs -f n8n

# Restart n8n
docker-compose restart n8n

# Stop all
docker-compose down

# Start all
docker-compose up -d

# View resource usage
docker stats
```

#### Database Commands

```bash
# Connect to database
docker exec -it n8n-postgres psql -U n8n -d n8n

# Backup database
docker exec n8n-postgres pg_dump -U n8n n8n > backup.sql

# Restore database
docker exec -i n8n-postgres psql -U n8n -d n8n < backup.sql

# List tables
docker exec -it n8n-postgres psql -U n8n -d n8n -c "\dt"
```

#### Maintenance Commands

```bash
# Check disk usage
du -sh /home/user/n8n-novels/*

# Clean old logs
find /home/user/n8n-novels/logs -name "*.log" -mtime +30 -delete

# Backup now
/home/user/shared/tools/backup-all.sh

# View dashboard
python3 /home/user/shared/tools/unified-dashboard.py

# Check cron jobs
crontab -l
```

### D. Resources & Links

#### Official Documentation

- **Claude API:** https://docs.anthropic.com
- **Claude Code:** https://docs.claude.com/code
- **n8n:** https://docs.n8n.io
- **OpenAI:** https://platform.openai.com/docs
- **Google AI:** https://ai.google.dev/docs

#### Communities

- **n8n Community:** https://community.n8n.io
- **Reddit r/ClaudeAI:** https://reddit.com/r/ClaudeAI
- **Reddit r/n8n:** https://reddit.com/r/n8n

#### Tools

- **Pandoc** (EPUB conversion): https://pandoc.org
- **Calibre** (eBook management): https://calibre-ebook.com
- **VS Code:** https://code.visualstudio.com

#### Thai Novel Platforms

- **Ookbee:** https://www.ookbee.com
- **Meb:** https://www.meb.in.th
- **ReadAWrite:** https://www.readawrite.com
- **Dek-D:** https://www.dek-d.com/writer

---

## 🎊 CONCLUSION

### Summary

คุณได้รับ data sheet ที่ครอบคลุมสำหรับ:

1. **Claude Code System** - ระบบเขียนนิยายคุณภาพสูง
2. **n8n Multi-AI System** - ระบบเขียนนิยายอัตโนมัติปริมาณมาก
3. **Integration Strategy** - วิธีใช้ทั้ง 2 ระบบร่วมกัน
4. **Implementation Plan** - แผนการทำงานทีละขั้นตอน
5. **Budget & ROI** - ต้นทุนและผลตอบแทน
6. **Risk Management** - การจัดการความเสี่ยง

### Next Steps

1. **อ่าน data sheet นี้ให้ละเอียด**
2. **ตัดสินใจว่าจะเริ่มจากไหน** (Claude Code หรือ n8n)
3. **เตรียม budget และ resources**
4. **เริ่ม Phase 1: Setup**
5. **ติดตามตาม checklist**

### Success Factors

✅ **ความอดทน** - Setup ใช้เวลา แต่คุ้มค่า  
✅ **ความสม่ำเสมอ** - Monitor และปรับปรุงทุกวัน  
✅ **การเรียนรู้** - ปรับปรุงจาก feedback  
✅ **ความยืดหยุ่น** - พร้อม adapt ตามสถานการณ์  
✅ **Quality Focus** - คุณภาพนำไปสู่ความสำเร็จ  

### Final Encouragement

ระบบนี้ออกแบบมาเพื่อให้คุณสามารถ:
- สร้างรายได้จากการเขียนนิยาย
- Scale ได้ตามความต้องการ
- ควบคุมคุณภาพได้
- ลดงานซ้ำซ้อน
- เพิ่มประสิทธิภาพ

**คุณพร้อมแล้ว! เริ่มกันเลย! 🚀**

---

**Document Version:** 1.0  
**Created:** January 31, 2026  
**Created By:** Claude (Anthropic)  
**For:** Novel Writing Automation Project  
**Language:** Thai/English  
**Status:** Ready for Implementation  

---

**📝 Notes:**
- บันทึกไฟล์นี้เป็น reference
- อัพเดทเมื่อมีการเปลี่ยนแปลง
- Share กับทีมถ้ามี
- ใช้เป็น single source of truth

**🔗 Related Files:**
- README.md (แต่ละระบบ)
- docker-compose.yml (n8n)
- .env (configuration)
- workflow JSONs (n8n)
- skill files (Claude Code)

**💬 Support:**
หากมีคำถามหรือต้องการความช่วยเหลือ:
1. อ้างอิง document นี้
2. ระบุ section ที่เกี่ยวข้อง
3. ให้บริบทที่ชัดเจน
4. ถาม Claude ผ่าน claude.ai

---

# 🎯 END OF DOCUMENT

**Good luck with your novel writing empire! 📚✨**

**May your stories be compelling, your automation flawless, and your revenue abundant! 💰🚀**
