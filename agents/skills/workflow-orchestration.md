# Workflow Orchestration Skill

## Overview
Skill สำหรับ N8n Manager ในการจัดการ workflows และ coordinate งาน

## N8n Workflow Architecture

```
                    ┌─────────────────┐
                    │ Daily Scheduler │
                    │   (Cron)        │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
       ┌──────────┐   ┌──────────┐   ┌──────────┐
       │ Project  │   │ Project  │   │ Project  │
       │    A     │   │    B     │   │    C     │
       └────┬─────┘   └────┬─────┘   └────┬─────┘
            │              │              │
            ▼              ▼              ▼
    ┌───────────────────────────────────────────┐
    │            GENERATION LAYER               │
    │  ┌─────────────┐  ┌─────────────┐        │
    │  │ Character   │  │    Plot     │        │
    │  │ Generator   │  │  Outliner   │        │
    │  └─────────────┘  └─────────────┘        │
    └───────────────────────────────────────────┘
                        │
                        ▼
    ┌───────────────────────────────────────────┐
    │            WRITING LAYER                  │
    │  ┌─────────┐ ┌─────────┐ ┌─────────┐     │
    │  │ Gemini  │ │  GPT    │ │ Claude  │     │
    │  │ Writer  │ │ Writer  │ │ Writer  │     │
    │  └─────────┘ └─────────┘ └─────────┘     │
    └───────────────────────────────────────────┘
                        │
                        ▼
    ┌───────────────────────────────────────────┐
    │            QC LAYER                       │
    │  ┌─────────┐ ┌─────────┐ ┌─────────┐     │
    │  │QC Basic │→│QC Score │→│QC Deep  │     │
    │  └─────────┘ └─────────┘ └─────────┘     │
    └───────────────────────────────────────────┘
```

## Workflow Definitions

### 1. Character Generator Workflow
```yaml
workflow: character-generator
trigger: webhook
steps:
  1. Receive project params
  2. Load genre prompt template
  3. Call AI API (Gemini/GPT/Claude by genre)
  4. Parse JSON response
  5. Validate character data
  6. Save to database
  7. Save to project folder
  8. Notify completion
```

### 2. Plot Outliner Workflow
```yaml
workflow: plot-outliner
trigger: webhook
steps:
  1. Receive project + characters
  2. Load outline prompt
  3. Call AI API
  4. Parse outline structure
  5. Validate completeness
  6. Save to database
  7. Trigger chapter planning
  8. Notify completion
```

### 3. Chapter Writer Workflows
```yaml
workflow: chapter-writer-{model}
trigger: webhook
variants: [gemini, gpt, claude]
steps:
  1. Receive chapter request
  2. Load previous context
  3. Load chapter outline
  4. Construct prompt
  5. Call AI API
  6. Post-process text
  7. Basic validation
  8. Queue for QC
  9. Save draft
```

### 4. QC Pipeline Workflows
```yaml
workflow: qc-pipeline
trigger: on_chapter_complete
steps:
  1. QC Basic (automated)
     - Word count check
     - Placeholder detection
     - Format validation

  2. QC AI Score (Gemini Flash)
     - Grammar score
     - Consistency score
     - Quality score

  3. QC Deep (if score 70-79)
     - Claude Haiku analysis
     - Detailed feedback

  4. Decision
     - Approve (≥80)
     - Flag for revision (70-79)
     - Regenerate (<70)
```

### 5. Batch Writer Workflow
```yaml
workflow: batch-writer
trigger: manual/scheduled
params:
  projects: [list of project_ids]
  chapters_per_project: number
steps:
  1. Queue all chapters
  2. Distribute to models (round-robin)
  3. Process in parallel (max 5)
  4. Collect results
  5. Run QC batch
  6. Generate summary report
```

## Orchestration Commands

### Start New Project
```json
{
  "command": "start_project",
  "params": {
    "title": "Novel Title",
    "genre": "fantasy",
    "chapters": 25,
    "model_preference": "gpt-4o"
  }
}
```

### Trigger Workflow
```json
{
  "command": "trigger_workflow",
  "workflow_id": "chapter-writer-gemini",
  "input": {
    "project_id": "proj-123",
    "chapter_num": 5
  }
}
```

### Batch Process
```json
{
  "command": "batch_process",
  "workflow_id": "batch-writer",
  "projects": ["proj-123", "proj-456", "proj-789"],
  "chapters_each": 3,
  "parallel_limit": 5
}
```

### Check Status
```json
{
  "command": "get_status",
  "execution_id": "exec-abc123"
}
```

## Error Handling

### Workflow Failures
```python
def handle_workflow_failure(execution):
    error = execution.error

    if error.type == "API_RATE_LIMIT":
        # Wait and retry with different model
        wait(60)
        retry_with_backup_model(execution)

    elif error.type == "API_ERROR":
        # Retry with exponential backoff
        for attempt in range(3):
            wait(10 * (2 ** attempt))
            if retry(execution):
                return SUCCESS
        mark_failed(execution)

    elif error.type == "VALIDATION_ERROR":
        # Try regeneration
        regenerate_with_feedback(execution, error.details)

    else:
        # Unknown error - escalate
        escalate_to_manager(execution)
```

### Recovery Procedures
1. **Partial Completion** - Resume from last checkpoint
2. **Data Corruption** - Restore from backup, retry
3. **System Down** - Queue for later execution
4. **Budget Exceeded** - Pause non-critical, notify CEO

## Scheduling

### Daily Schedule
```
00:00 - 06:00: Batch writing (low traffic)
06:00 - 08:00: QC processing
08:00 - 18:00: On-demand (user requests)
18:00 - 20:00: Reports generation
20:00 - 00:00: Maintenance window
```

### Cron Expressions
```yaml
daily_batch: "0 0 * * *"      # Midnight
hourly_check: "0 * * * *"     # Every hour
weekly_report: "0 18 * * 0"   # Sunday 6PM
cleanup: "0 3 * * *"          # 3AM daily
```

## Monitoring

### Execution Metrics
```sql
SELECT
    workflow_name,
    COUNT(*) as total_runs,
    AVG(duration_seconds) as avg_duration,
    SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as successes,
    SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failures
FROM execution_logs
WHERE executed_at > NOW() - INTERVAL '24 hours'
GROUP BY workflow_name;
```

### Real-time Dashboard
```
╔═══════════════════════════════════════════════════════╗
║         WORKFLOW ORCHESTRATION DASHBOARD              ║
╠═══════════════════════════════════════════════════════╣
║ Active Executions: 5                                  ║
║ Queued: 12                                            ║
║ Completed Today: 87                                   ║
║ Failed Today: 3                                       ║
╠═══════════════════════════════════════════════════════╣
║ Running Now:                                          ║
║ • chapter-writer-gemini [proj-123/ch5] 45s ago       ║
║ • chapter-writer-gpt [proj-456/ch8] 30s ago          ║
║ • qc-ai-scorer [proj-789/ch3] 15s ago                ║
║ • batch-writer [5 projects] 2min ago                 ║
║ • plot-outliner [proj-999] 1min ago                  ║
╠═══════════════════════════════════════════════════════╣
║ Queue (next 5):                                       ║
║ 1. chapter-writer-claude [proj-123/ch6]              ║
║ 2. qc-basic [proj-456/ch8]                           ║
║ 3. character-generator [proj-new]                     ║
║ ...                                                   ║
╚═══════════════════════════════════════════════════════╝
```

## Best Practices

1. **Parallel Wisely** - Don't exceed model rate limits
2. **Queue Management** - Prioritize correctly
3. **Checkpoint Often** - Save state for recovery
4. **Monitor Costs** - Track per-execution costs
5. **Log Everything** - Debugging needs history
6. **Graceful Degradation** - Fallback to simpler workflows
