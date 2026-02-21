# Strategic Planning Skill

## Overview
Skill สำหรับ CEO Agent ในการวางแผนกลยุทธ์และตัดสินใจระดับสูง

## Capabilities

### 1. Task Analysis
วิเคราะห์คำขอจาก User เพื่อกำหนดทิศทางการทำงาน

```
Input Analysis Checklist:
□ ประเภทงาน (single novel / batch / urgent)
□ ระดับคุณภาพที่ต้องการ (premium / standard)
□ จำนวนนิยาย
□ แนวนิยาย
□ กำหนดส่ง
□ งบประมาณ (ถ้าระบุ)
```

### 2. Team Assignment Logic

```python
def assign_team(task):
    if task.quality == "premium" or task.novel_count <= 3:
        return "claude-code-team"
    elif task.novel_count > 3 or task.mode == "batch":
        return "n8n-team"
    elif task.deadline_days < 7:
        return "both_teams_parallel"
    else:
        return "n8n-team"  # default for efficiency
```

### 3. Resource Allocation

| Scenario | Claude Team | N8n Team |
|----------|-------------|----------|
| Premium single novel | 100% | 0% |
| Standard batch (5+) | 0% | 100% |
| Urgent deadline | 50% | 50% |
| Mixed quality batch | 30% | 70% |

### 4. Priority Management

**Priority Levels:**
1. **Critical** - ต้องทำทันที (deadline ภายใน 24 ชม.)
2. **High** - ต้องจัดการภายในวัน (deadline ภายใน 3 วัน)
3. **Normal** - ทำตามลำดับ
4. **Low** - ทำเมื่อว่าง

### 5. Risk Assessment

```
Risk Factors:
- Tight deadline → เพิ่ม resource
- Complex genre (mystery) → ใช้ premium team
- Large volume → ระวังเรื่อง cost
- First-time genre → allocate extra QC
```

## Decision Templates

### Template 1: New Project Request
```markdown
## Project Analysis

**Request:** {{user_request}}
**Parsed:**
- Type: {{novel_type}}
- Genre: {{genre}}
- Quantity: {{count}}
- Quality: {{quality_level}}
- Deadline: {{deadline}}

**Decision:**
- Assigned to: {{team}}
- Reason: {{reason}}
- Priority: {{priority}}
- Estimated completion: {{eta}}
```

### Template 2: Escalation Decision
```markdown
## Escalation Analysis

**Issue:** {{issue_description}}
**Source:** {{source_agent}}
**Severity:** {{severity}}

**Options:**
1. {{option_1}} - {{pros_cons_1}}
2. {{option_2}} - {{pros_cons_2}}

**Decision:** {{chosen_option}}
**Rationale:** {{rationale}}
```

## Metrics to Monitor

1. **Project Health**
   - Progress vs. timeline
   - Quality scores trend
   - Error rates

2. **Resource Utilization**
   - Team capacity
   - API costs
   - Model availability

3. **Output Quality**
   - Average scores per team
   - Revision rates
   - Completion rates

## Communication Protocols

### To Managers
```json
{
  "type": "task_assignment",
  "priority": "high",
  "task": {
    "project_id": "...",
    "action": "create_novel",
    "parameters": {...}
  },
  "deadline": "2025-01-15",
  "special_instructions": "..."
}
```

### To User (Reports)
```markdown
# Daily Summary

## Completed Today
- {{completed_items}}

## In Progress
- {{in_progress_items}}

## Blockers
- {{blockers}}

## Tomorrow's Plan
- {{tomorrow_plan}}
```

## Best Practices

1. **Always analyze before assigning** - อย่ารีบส่งงานโดยไม่วิเคราะห์
2. **Balance quality and efficiency** - Premium ไม่ได้ดีเสมอ
3. **Monitor costs proactively** - อย่าให้งบบานปลาย
4. **Escalate early** - ปัญหาเล็กง่ายกว่าปัญหาใหญ่
5. **Document decisions** - บันทึกเหตุผลการตัดสินใจ
