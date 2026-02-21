# Batch Processing Skill

## Overview
Skill สำหรับประมวลผลงานจำนวนมากพร้อมกันอย่างมีประสิทธิภาพ

## Batch Processing Concepts

### What Can Be Batched
1. **Character Generation** - สร้างตัวละครหลายโปรเจคพร้อมกัน
2. **Plot Outlining** - วางโครงเรื่องหลายเรื่อง
3. **Chapter Writing** - เขียนหลายบทพร้อมกัน
4. **Quality Control** - ตรวจคุณภาพเป็น batch
5. **Export** - Export หลายเรื่องพร้อมกัน

### Batch Configurations
```yaml
batch_limits:
  character_generation:
    max_parallel: 10
    timeout_per_item: 120s

  chapter_writing:
    max_parallel: 5  # เพราะใช้ resource มาก
    timeout_per_item: 300s

  qc_processing:
    max_parallel: 20  # QC เบากว่า
    timeout_per_item: 60s

  export:
    max_parallel: 10
    timeout_per_item: 180s
```

## Batch Job Structure

### Job Definition
```json
{
  "job_id": "batch-2025-01-15-001",
  "job_type": "chapter_writing",
  "created_at": "2025-01-15T00:00:00Z",
  "priority": "normal",

  "items": [
    {
      "item_id": "item-001",
      "project_id": "proj-123",
      "chapter_num": 5,
      "status": "pending"
    },
    {
      "item_id": "item-002",
      "project_id": "proj-456",
      "chapter_num": 8,
      "status": "pending"
    }
  ],

  "config": {
    "max_parallel": 5,
    "retry_on_failure": true,
    "max_retries": 2,
    "model_rotation": true
  },

  "status": "running",
  "progress": {
    "total": 20,
    "completed": 12,
    "failed": 1,
    "pending": 7
  }
}
```

## Processing Strategies

### 1. Round-Robin Model Distribution
```python
def distribute_to_models(items, models):
    """
    กระจายงานไปยัง models อย่างเท่าเทียม
    """
    assignments = []
    for i, item in enumerate(items):
        model = models[i % len(models)]
        assignments.append((item, model))
    return assignments

# Example
models = ["gemini", "gpt-4o", "claude-haiku"]
items = [chapter1, chapter2, chapter3, chapter4, chapter5, chapter6]
# Result:
# chapter1 → gemini
# chapter2 → gpt-4o
# chapter3 → claude-haiku
# chapter4 → gemini
# ...
```

### 2. Genre-Based Routing
```python
def route_by_genre(items):
    """
    ส่งงานไป model ที่ถนัด genre นั้น
    """
    routing = {
        "romantic-comedy": "gemini",
        "fantasy": "gpt-4o",
        "horror": "claude-haiku",
        "mystery": "gpt-4o",
        "bl-gl": "claude-haiku"
    }

    for item in items:
        item.model = routing.get(item.genre, "gemini")
    return items
```

### 3. Load-Based Distribution
```python
def distribute_by_load(items):
    """
    ส่งงานไป model ที่ว่างมากที่สุด
    """
    model_loads = get_current_loads()

    for item in items:
        # เลือก model ที่ load น้อยที่สุด
        best_model = min(model_loads, key=model_loads.get)
        item.model = best_model
        model_loads[best_model] += 1

    return items
```

## Queue Management

### Priority Queue
```
Priority Levels:
┌─────────────────────────────────────┐
│ 1. CRITICAL - Deadline < 24h        │
│ 2. HIGH     - Deadline < 3 days     │
│ 3. NORMAL   - Regular queue         │
│ 4. LOW      - Background tasks      │
└─────────────────────────────────────┘
```

### Queue Operations
```python
class BatchQueue:
    def __init__(self):
        self.queues = {
            "critical": [],
            "high": [],
            "normal": [],
            "low": []
        }

    def enqueue(self, item, priority="normal"):
        self.queues[priority].append(item)

    def dequeue(self):
        # ดึงจาก priority สูงสุดก่อน
        for priority in ["critical", "high", "normal", "low"]:
            if self.queues[priority]:
                return self.queues[priority].pop(0)
        return None

    def get_position(self, item_id):
        position = 0
        for priority in ["critical", "high", "normal", "low"]:
            for item in self.queues[priority]:
                position += 1
                if item.id == item_id:
                    return position
        return -1
```

## Progress Tracking

### Real-time Progress
```
Batch Job: batch-2025-01-15-001
Type: Chapter Writing
Started: 00:00:00
Elapsed: 00:45:23

Progress: [████████████░░░░░░░░] 60%
           12/20 completed

Status Breakdown:
✅ Completed: 12
🔄 Running: 3
⏳ Pending: 4
❌ Failed: 1

Current Processing:
• proj-123/ch7 → gemini (30s)
• proj-456/ch9 → gpt-4o (45s)
• proj-789/ch4 → claude-haiku (20s)

Estimated Completion: 00:30:00
```

### Progress Callbacks
```python
def on_item_complete(item, result):
    """
    เรียกเมื่อ item เสร็จ
    """
    update_progress(item.batch_id)

    if result.success:
        log_success(item)
        trigger_next_step(item)  # เช่น QC
    else:
        log_failure(item, result.error)
        if should_retry(item):
            requeue(item)
        else:
            mark_failed(item)

def on_batch_complete(batch):
    """
    เรียกเมื่อ batch ทั้งหมดเสร็จ
    """
    generate_summary_report(batch)
    notify_manager(batch)
    cleanup_resources(batch)
```

## Error Handling in Batch

### Retry Strategy
```yaml
retry_config:
  max_retries: 3
  retry_delay:
    initial: 10s
    multiplier: 2
    max: 120s

  retryable_errors:
    - API_RATE_LIMIT
    - TIMEOUT
    - TEMPORARY_ERROR

  non_retryable_errors:
    - INVALID_INPUT
    - AUTH_ERROR
    - QUOTA_EXCEEDED
```

### Failure Handling
```python
def handle_batch_failure(batch, failed_items):
    """
    จัดการเมื่อมี items fail
    """
    failure_rate = len(failed_items) / batch.total_items

    if failure_rate > 0.5:
        # มากกว่าครึ่ง fail - หยุดทั้ง batch
        pause_batch(batch)
        escalate_to_manager(batch, "High failure rate")

    elif failure_rate > 0.2:
        # 20-50% fail - continue แต่ notify
        notify_manager(batch, "Elevated failure rate")
        continue_batch(batch)

    else:
        # น้อยกว่า 20% - ทำต่อปกติ
        continue_batch(batch)
```

## Resource Management

### Rate Limiting
```python
class RateLimiter:
    def __init__(self, model, rpm_limit, tpm_limit):
        self.model = model
        self.rpm_limit = rpm_limit
        self.tpm_limit = tpm_limit
        self.requests_this_minute = 0
        self.tokens_this_minute = 0

    def can_process(self, estimated_tokens):
        if self.requests_this_minute >= self.rpm_limit:
            return False
        if self.tokens_this_minute + estimated_tokens > self.tpm_limit:
            return False
        return True

    def record_usage(self, tokens_used):
        self.requests_this_minute += 1
        self.tokens_this_minute += tokens_used
```

### Cost Tracking
```python
def track_batch_cost(batch):
    """
    ติดตามค่าใช้จ่ายของ batch
    """
    total_cost = 0

    for item in batch.completed_items:
        model_cost = MODEL_COSTS[item.model]
        item_cost = (
            (item.input_tokens / 1000) * model_cost["input"] +
            (item.output_tokens / 1000) * model_cost["output"]
        )
        total_cost += item_cost

    return {
        "total_cost": total_cost,
        "cost_per_item": total_cost / len(batch.completed_items),
        "budget_remaining": batch.budget - total_cost
    }
```

## Batch Reports

### Summary Report Template
```markdown
# Batch Processing Report

## Job Information
- **Job ID:** {{job_id}}
- **Type:** {{job_type}}
- **Started:** {{start_time}}
- **Completed:** {{end_time}}
- **Duration:** {{duration}}

## Results Summary
| Status | Count | Percentage |
|--------|-------|------------|
| Success | {{success_count}} | {{success_pct}}% |
| Failed | {{failed_count}} | {{failed_pct}}% |
| Skipped | {{skipped_count}} | {{skipped_pct}}% |

## Performance Metrics
- **Average Processing Time:** {{avg_time}}
- **Throughput:** {{items_per_minute}} items/min
- **Total Cost:** ${{total_cost}}
- **Cost per Item:** ${{cost_per_item}}

## Model Usage
| Model | Items | Tokens | Cost |
|-------|-------|--------|------|
{{#models}}
| {{name}} | {{items}} | {{tokens}} | ${{cost}} |
{{/models}}

## Failed Items
{{#failed_items}}
- {{item_id}}: {{error_message}}
{{/failed_items}}

## Recommendations
{{recommendations}}
```

## Best Practices

1. **Start Small** - ทดสอบด้วย batch เล็กก่อน
2. **Monitor Closely** - ดู progress ตลอด
3. **Set Budgets** - กำหนด cost limit
4. **Handle Failures Gracefully** - อย่าให้ fail หนึ่งทำ batch พัง
5. **Clean Up** - ลบ temp files หลังจบ
6. **Document Results** - บันทึกผลทุก batch
