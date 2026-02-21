# Novel Empire Agent System

## Overview

ระบบ AI Agents สำหรับจัดการ Novel Writing Automation Project

```
                              ┌─────────────────────┐
                              │      CEO Agent      │
                              │  Strategic Control  │
                              └──────────┬──────────┘
                                         │
        ┌────────────────────────────────┼────────────────────────────────┐
        │                                │                                │
        ▼                                ▼                                ▼
┌───────────────────┐          ┌─────────────────────┐          ┌───────────────────┐
│ Claude Code Mgr   │          │  Cover Design Mgr   │          │    N8n Manager    │
│ Premium Quality   │          │    Book Covers      │          │    High Volume    │
└────────┬──────────┘          └──────────┬──────────┘          └─────────┬─────────┘
         │                                │                               │
   ┌─────┴─────┐              ┌───────────┼───────────┐        ┌─────────┼─────────┐
   │           │              │     │     │     │     │        │         │         │
   ▼           ▼              ▼     ▼     ▼     ▼     ▼        ▼         ▼         ▼
┌───────┐ ┌───────┐      ┌──────┐┌──────┐┌──────┐┌──────┐ ┌───────┐ ┌───────┐ ┌───────┐
│Writer │ │Quality│      │Image ││Prompt││Layout││Cover │ │Genera-│ │Writer │ │Quality│
│ Agent │ │ Agent │      │Scout ││Engnr ││Design││  QC  │ │ tor   │ │ Agent │ │ Agent │
└───────┘ └───────┘      └──────┘└──────┘└──────┘└──────┘ └───────┘ └───────┘ └───────┘
```

## Agent Summary

| Agent | Role | Model | Team |
|-------|------|-------|------|
| NovelEmpireCEO | Strategic oversight | Claude Opus | Management |
| ClaudeCodeManager | Premium team leader | Claude Sonnet | Claude Code |
| N8nManager | Volume team leader | GPT-4o-mini | N8n |
| **CoverDesignManager** | Cover team leader | Claude Sonnet | Cover Design |
| ClaudeWriter | Premium writing | Claude Sonnet | Claude Code |
| ClaudeQuality | Premium QC | Claude Sonnet | Claude Code |
| N8nGenerator | Character/Plot gen | Gemini Pro | N8n |
| N8nWriter | Volume writing | Mixed | N8n |
| N8nQuality | Volume QC | Gemini Flash | N8n |
| **ImageScout** | Find stock photos | Claude Sonnet | Cover Design |
| **PromptEngineer** | Write AI prompts | Claude Sonnet | Cover Design |
| **LayoutDesigner** | Design typography | Claude Sonnet | Cover Design |
| **CoverQC** | Quality check covers | Claude Sonnet | Cover Design |

**Total: 13 Agents (3 Managers + 10 Subagents)**

## Directory Structure

```
agents/
├── README.md              # This file
├── orchestrator.py        # Central message routing
├── agent_runner.py        # Agent execution
│
├── config/                # Agent configurations
│   ├── ceo.yaml
│   ├── claude-manager.yaml
│   ├── n8n-manager.yaml
│   ├── cover-design-manager.yaml    # 🆕 Cover Design Team
│   └── subagents/
│       ├── claude-writer.yaml
│       ├── claude-quality.yaml
│       ├── n8n-generator.yaml
│       ├── n8n-writer.yaml
│       ├── n8n-quality.yaml
│       ├── image-scout.yaml          # 🆕
│       ├── prompt-engineer.yaml      # 🆕
│       ├── layout-designer.yaml      # 🆕
│       └── cover-qc.yaml             # 🆕
│
├── skills/                # Agent skills
│   ├── strategic-planning.md
│   ├── resource-allocation.md
│   ├── workflow-orchestration.md
│   └── batch-processing.md
│
├── messages/              # Inter-agent messages
│   ├── ceo-inbox/
│   ├── claude-manager/
│   ├── n8n-manager/
│   ├── cover-manager/                # 🆕
│   ├── broadcasts/
│   └── archive/
│
└── logs/                  # Agent logs
    ├── ceo.log
    ├── claude-team.log
    ├── n8n-team.log
    └── cover-team.log                # 🆕

cover-design-team/         # 🆕 Cover Design Resources
├── README.md
├── templates/
│   ├── cover-brief-template.md
│   ├── color-schemes.json
│   └── font-guide.md
├── resources/
├── skills/
└── examples/
```

## Quick Start

### 1. Check System Status
```bash
python agents/orchestrator.py --status
```

### 2. Run an Agent
```bash
# Run CEO
python agents/agent_runner.py ceo

# Run Claude Manager
python agents/agent_runner.py claude-manager

# Run N8n Manager
python agents/agent_runner.py n8n-manager

# Run Subagents
python agents/agent_runner.py claude-writer
python agents/agent_runner.py n8n-generator
```

### 3. Send a Task
```bash
python agents/orchestrator.py --send-task '{
  "title": "สร้างนิยายแฟนตาซี",
  "genre": "fantasy",
  "novel_count": 1,
  "quality": "premium",
  "chapters": 25,
  "priority": "normal"
}'
```

### 4. Generate Report
```bash
python agents/orchestrator.py --report
```

## Communication Protocol

### Message Format
```json
{
  "id": "msg-abc123",
  "timestamp": "2025-01-15T10:00:00Z",
  "from": "ceo-001",
  "to": "mgr-claude-001",
  "type": "task",
  "priority": "high",
  "subject": "New Novel Project",
  "body": {
    "action": "create_novel",
    "params": {...}
  },
  "requires_response": true,
  "deadline": "2025-01-20T10:00:00Z"
}
```

### Message Types
- `task` - งานที่ต้องทำ
- `status` - รายงานสถานะ
- `question` - คำถาม/ขอคำปรึกษา
- `report` - รายงานผลลัพธ์
- `alert` - แจ้งเตือน
- `broadcast` - ประกาศถึงทุกคน

### Priority Levels
- `critical` - ด่วนที่สุด
- `high` - สำคัญ
- `normal` - ปกติ
- `low` - ทำเมื่อว่าง

## Workflow Examples

### Example 1: Premium Novel
```
User → CEO: "สร้างนิยายแฟนตาซีคุณภาพสูง 25 บท"
       │
       ▼
CEO analyzes → assigns to ClaudeCodeManager
       │
       ▼
ClaudeCodeManager → ClaudeWriter: "สร้าง characters"
       │
       ▼
ClaudeWriter completes → reports back
       │
       ▼
ClaudeCodeManager → ClaudeWriter: "สร้าง plot"
       │
       ▼
ClaudeWriter completes → reports back
       │
       ▼
For each chapter:
  ClaudeCodeManager → ClaudeWriter: "เขียนบท X"
  ClaudeWriter completes → ClaudeQuality: "ตรวจบท X"
  ClaudeQuality reports → ClaudeCodeManager
       │
       ▼
ClaudeCodeManager → CEO: "เสร็จแล้ว"
       │
       ▼
CEO → User: "นิยายเสร็จสมบูรณ์"
```

### Example 2: Batch Novels
```
User → CEO: "สร้างนิยาย 5 เรื่อง หลายแนว"
       │
       ▼
CEO analyzes → assigns to N8nManager
       │
       ▼
N8nManager → N8nGenerator: "สร้าง characters ทั้ง 5 เรื่อง"
       │
       ▼
N8nGenerator completes (parallel)
       │
       ▼
N8nManager → N8nWriter: "batch write"
       │
       ▼
N8nWriter writes (parallel, multiple models)
       │
       ▼
N8nManager → N8nQuality: "QC pipeline"
       │
       ▼
N8nQuality runs 3-layer QC
       │
       ▼
N8nManager → CEO: "5 เรื่องเสร็จ"
       │
       ▼
CEO → User: "ทั้งหมดเสร็จแล้ว"
```

## Configuration

### Agent Config Structure (YAML)
```yaml
agent:
  id: "agent-id"
  name: "AgentName"
  role: "CEO/Manager/Subagent"
  model: "claude-sonnet-4"

responsibilities:
  - task1
  - task2

skills:
  - name: "skill-name"
    path: "path/to/skill.md"

communication:
  inbox: "agents/messages/inbox/"
  reports_to: "manager-id"
```

## Monitoring

### Check Logs
```bash
# CEO logs
tail -f agents/logs/ceo.log

# Claude team logs
tail -f agents/logs/claude-team.log

# N8n team logs
tail -f agents/logs/n8n-team.log
```

### View Pending Messages
```bash
ls agents/messages/ceo-inbox/
ls agents/messages/claude-manager/
ls agents/messages/n8n-manager/
```

## Error Handling

### Escalation Path
1. Subagent fails → reports to Manager
2. Manager retries (max 2 times)
3. Still fails → escalates to CEO
4. CEO evaluates:
   - Try other team
   - Adjust parameters
   - Escalate to human

### Recovery
- Messages are persisted to disk
- Agents can resume from last state
- Archive keeps history

## Development

### Adding New Agent
1. Create config in `config/` or `config/subagents/`
2. Add to agent mappings in `agent_runner.py`
3. Implement custom logic if needed

### Adding New Skill
1. Create markdown file in `skills/`
2. Reference in agent config
3. Implement execution logic

## Troubleshooting

### Agent won't start
- Check config file exists
- Verify YAML syntax
- Check logs for errors

### Messages not delivered
- Verify recipient agent ID
- Check message queue directories
- Review orchestrator logs

### Task stuck
- Check agent logs
- Verify agent is running
- Check for errors in processing

## License

Part of Novel Writing Automation Project
