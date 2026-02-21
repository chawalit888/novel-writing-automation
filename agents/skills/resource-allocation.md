# Resource Allocation Skill

## Overview
Skill สำหรับจัดสรร resources ระหว่างทีมและโปรเจค

## Resources to Manage

### 1. API Budget
```yaml
daily_budget: $25
monthly_budget: $500

allocation:
  claude_team: 60%  # $15/day
  n8n_team: 40%     # $10/day

per_model_costs:
  claude-opus: $0.015/1K input, $0.075/1K output
  claude-sonnet: $0.003/1K input, $0.015/1K output
  claude-haiku: $0.00025/1K input, $0.00125/1K output
  gpt-4o: $0.005/1K input, $0.015/1K output
  gpt-4o-mini: $0.00015/1K input, $0.0006/1K output
  gemini-pro: $0.00125/1K input, $0.00375/1K output
  gemini-flash: $0.0001/1K input, $0.0004/1K output
```

### 2. Team Capacity

| Team | Max Parallel Projects | Chapters/Day |
|------|----------------------|--------------|
| Claude Code | 3-5 | 3-5 |
| N8n | 10-15 | 10-15 |

### 3. Model Availability
```python
model_limits = {
    "gemini": {"rpm": 60, "tpm": 1_000_000},
    "gpt-4o": {"rpm": 60, "tpm": 800_000},
    "claude": {"rpm": 40, "tpm": 400_000}
}
```

## Allocation Strategies

### Strategy 1: Quality-First
```
ใช้เมื่อ: คุณภาพสำคัญกว่าความเร็ว

- Claude Team: 70%
- N8n Team: 30%
- Model: Claude Sonnet/Opus
- QC: Full 5-layer
```

### Strategy 2: Volume-First
```
ใช้เมื่อ: ต้องการ output มาก

- Claude Team: 20%
- N8n Team: 80%
- Model: Gemini Flash/GPT-4o-mini
- QC: Layer 1-2 only
```

### Strategy 3: Balanced
```
ใช้เมื่อ: ต้องการทั้งคุณภาพและปริมาณ

- Claude Team: 40%
- N8n Team: 60%
- Model: Mixed based on genre
- QC: Full for premium, Layer 1-3 for standard
```

### Strategy 4: Emergency
```
ใช้เมื่อ: Deadline ใกล้มาก

- Claude Team: 50%
- N8n Team: 50%
- Model: Fastest available
- QC: Layer 1-2, manual review
```

## Cost Optimization

### Per-Chapter Cost Estimates
| Model | Avg Cost/Chapter | Quality |
|-------|------------------|---------|
| Claude Opus | $0.50-1.00 | Excellent |
| Claude Sonnet | $0.15-0.30 | Very Good |
| GPT-4o | $0.10-0.20 | Very Good |
| Claude Haiku | $0.03-0.05 | Good |
| Gemini Pro | $0.02-0.04 | Good |
| GPT-4o-mini | $0.01-0.02 | Acceptable |
| Gemini Flash | $0.005-0.01 | Acceptable |

### Cost-Saving Tips
1. ใช้ Gemini Flash สำหรับ QC Layer 1-2
2. ใช้ Claude Haiku สำหรับ horror/BL-GL (ถนัด)
3. Batch requests เมื่อเป็นไปได้
4. Cache repeated prompts

## Workload Balancing

### Formula
```python
def calculate_load(team):
    active_projects = len(team.projects)
    pending_chapters = sum(p.remaining_chapters for p in team.projects)
    capacity = team.max_capacity

    load_percentage = (active_projects / capacity) * 100

    if load_percentage > 80:
        return "OVERLOADED"
    elif load_percentage > 60:
        return "BUSY"
    elif load_percentage > 30:
        return "NORMAL"
    else:
        return "AVAILABLE"
```

### Rebalancing Triggers
- Team load > 90% → Transfer to other team
- API cost > 80% budget → Switch to cheaper models
- Error rate > 10% → Reduce parallel tasks

## Monitoring Dashboard

```
╔══════════════════════════════════════════════════════╗
║           RESOURCE ALLOCATION DASHBOARD              ║
╠══════════════════════════════════════════════════════╣
║ Budget Today: $18.50 / $25.00 (74%)                  ║
║ [████████████████████░░░░░░░]                        ║
╠══════════════════════════════════════════════════════╣
║ CLAUDE TEAM              N8N TEAM                    ║
║ Load: 65% [BUSY]         Load: 78% [BUSY]           ║
║ Projects: 3/5            Projects: 12/15            ║
║ Chapters: 8 pending      Chapters: 45 pending       ║
║ Cost: $11.20             Cost: $7.30                ║
╠══════════════════════════════════════════════════════╣
║ Model Usage Today:                                   ║
║ • Gemini: 245 calls ($2.50)                         ║
║ • GPT-4o: 89 calls ($4.20)                          ║
║ • Claude: 156 calls ($11.80)                        ║
╚══════════════════════════════════════════════════════╝
```

## Allocation Commands

### Assign Project
```json
{
  "action": "allocate",
  "resource_type": "project",
  "project_id": "novel-123",
  "target_team": "claude-code",
  "priority": "high",
  "budget_cap": 50.00
}
```

### Rebalance
```json
{
  "action": "rebalance",
  "from_team": "n8n",
  "to_team": "claude-code",
  "projects": ["novel-456"],
  "reason": "quality_issue"
}
```

### Budget Alert
```json
{
  "action": "budget_alert",
  "current_spend": 22.50,
  "budget": 25.00,
  "remaining": 2.50,
  "recommendation": "switch_to_cheaper_models"
}
```
