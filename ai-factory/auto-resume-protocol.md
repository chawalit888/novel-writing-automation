# Auto-Resume Protocol

## ปัญหาเดิม
เมื่อ Claude ถูก interrupt (rate limit, context limit, error) แล้วเปิด conversation ใหม่
→ Claude ลืมทุกอย่าง ไม่รู้ว่ากำลังแต่งเรื่องอะไร ตอนที่เท่าไหร่

## วิธีแก้: writing-state.json
ไฟล์ `writing-state.json` ที่ root ของโปรเจกต์ เป็น "ความจำถาวร" ของ Claude

### Flow ปกติ

```
User สั่ง "เขียนตอนที่ 15 ของเรื่อง X"
    ↓
Claude อัปเดต writing-state.json: active_task = เรื่อง X ตอน 15
    ↓
Claude เขียนตอนที่ 15
    ↓
Claude อัปเดต writing-state.json: last_completed = 15, current = 16
    ↓
Claude เขียนตอนที่ 16
    ↓
... (วนไปจนถึง target_chapter)
```

### Flow เมื่อถูก Interrupt

```
Claude กำลังเขียนตอนที่ 18 → ติด rate limit → conversation ตัด
    ↓
writing-state.json ยังบันทึกอยู่:
  active_task.last_completed_chapter = 17
  active_task.current_chapter = 18
    ↓
User เปิด conversation ใหม่ (อาจจะวันถัดไป)
    ↓
Claude อ่าน CLAUDE.md → เห็นกฎ Auto-Resume
    ↓
Claude อ่าน writing-state.json → เห็น active_task
    ↓
Claude เขียนตอนที่ 18 ต่อเลย ไม่ต้องถาม
    ↓
... (ต่อจนจบ target)
```

### Flow เมื่อ User ต้องการสั่งอย่างอื่น

```
Claude กำลังจะ auto-resume เรื่อง X
    ↓
User พิมพ์ "หยุด" หรือ "pause" หรือสั่งทำอย่างอื่น
    ↓
Claude ย้าย active_task ไป queued_tasks
    ↓
Claude ทำตามคำสั่ง User
    ↓
เมื่อ User ไม่มีคำสั่งใหม่ → Claude หยิบจาก queued_tasks มาทำต่อ
```

## โครงสร้าง writing-state.json

```json
{
  "active_task": {
    "type": "write_chapter",
    "story_id": "ชื่อเรื่อง",
    "story_path": "path/to/story/folder/",
    "current_chapter": 18,
    "target_chapter": 36,
    "last_completed_chapter": 17,
    "chapter_title_pattern": "ตอนที่{NUM:02d}-{TITLE}.txt",
    "notes": "หมายเหตุเพิ่มเติม",
    "interrupted_reason": "rate_limit",
    "resume_instructions": "คำแนะนำพิเศษสำหรับ resume"
  },
  "queued_tasks": [],
  "completed_today": [],
  "daily_stats": {
    "date": "2026-02-09",
    "chapters_written": 3,
    "words_written": 15000
  }
}
```

### ฟิลด์สำคัญ

| ฟิลด์ | คำอธิบาย |
|-------|---------|
| `active_task` | งานที่กำลังทำอยู่ (null = ไม่มี) |
| `type` | ประเภทงาน: `write_chapter`, `qc_check`, `create_plot` |
| `story_path` | path ไปยังโฟลเดอร์เรื่อง |
| `current_chapter` | ตอนที่กำลังจะเขียน (ตอนถัดไป) |
| `target_chapter` | เป้าหมายสุดท้าย |
| `last_completed_chapter` | ตอนสุดท้ายที่เสร็จจริง |
| `interrupted_reason` | เหตุผลที่ถูก interrupt |
| `resume_instructions` | คำแนะนำพิเศษตอน resume |
| `queued_tasks` | งานที่รอคิว (array ของ task objects) |
| `completed_today` | งานที่เสร็จวันนี้ |

## กฎสำคัญ

1. **อัปเดต state ทุกครั้งหลังเขียนเสร็จแต่ละตอน** - ก่อนเริ่มตอนถัดไป
2. **ไม่ต้องถาม user** - ถ้ามี active_task ให้ทำต่อเลย
3. **User สั่งหยุดได้ทุกเมื่อ** - พิมพ์ "หยุด" / "pause" / "stop"
4. **ถ้า User สั่งงานอื่น** → pause งานเดิม ทำงานใหม่ก่อน
5. **ทำต่อไม่หยุด** จนกว่าจะถึง target หรือ user สั่งหยุด
