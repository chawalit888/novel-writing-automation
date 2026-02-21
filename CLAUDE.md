# CLAUDE.md - Project Rules & Guidelines

## Auto-Resume: กฎสำคัญที่สุด (ทำก่อนทุกอย่าง)

**กฎเหล็ก: ทุกครั้งที่เปิด conversation ใหม่ ต้องอ่าน `writing-state.json` ก่อนเสมอ**

### เมื่อเปิด Conversation ใหม่:
1. **อ่าน `writing-state.json`** ทันที
2. ถ้า `active_task` ไม่ใช่ `null` → **เขียนต่อทันทีอัตโนมัติ ไม่ต้องถาม user**
3. ถ้า `queued_tasks` มีงาน → หยิบงานแรกมาทำเลย
4. ถ้าไม่มีงาน → รอคำสั่งจาก user ตามปกติ

### ขั้นตอน Auto-Resume (เมื่อมี active_task):
1. อ่าน `active_task` จาก `writing-state.json`
2. อ่าน outline/plot ของเรื่องนั้น
3. อ่านตอนล่าสุดที่เขียนเสร็จ (last_completed_chapter)
4. **เขียนตอนถัดไปเลย** (current_chapter + 1)
5. บันทึกไฟล์ตอนใหม่
6. อัปเดต `writing-state.json`:
   - `last_completed_chapter` +1
   - `current_chapter` +1
   - `_updated_at` = เวลาปัจจุบัน
   - เพิ่มใน `completed_today`
   - อัปเดต `daily_stats`
7. ถ้ายังไม่ถึง `target_chapter` → เขียนตอนถัดไปต่อ (วนลูป)
8. ถ้าถึง `target_chapter` แล้ว → set `active_task` = null, ย้ายงานไป `completed_today`

### เมื่อ User สั่งเขียนนิยาย:
1. สร้าง/อัปเดต `active_task` ใน `writing-state.json` ทันที
2. เริ่มเขียน
3. **ถ้าถูก interrupt** (limit/error/หมด context) → state จะยังอยู่ในไฟล์
4. Conversation ถัดไป Claude จะอ่าน state แล้วเขียนต่อเอง

### เมื่อเขียนเสร็จแต่ละตอน (บังคับทุกครั้ง):
- อัปเดต `writing-state.json` ทันที ก่อนเริ่มตอนถัดไป
- ห้ามลืม! ถ้าไม่อัปเดตแล้วถูก interrupt จะสูญเสีย progress

### การหยุด Auto-Resume:
- User พิมพ์ "หยุด" หรือ "pause" → set `active_task` = null
- User สั่งทำอย่างอื่น → pause งานปัจจุบัน ย้ายไป `queued_tasks`

### Background Worker (ทำงานเอง 24/7):
มี background worker (`agents/queue/novel-worker.sh`) ที่รัน Claude CLI อยู่ตลอด
- Worker อ่าน `writing-state.json` ทุก 5 นาที
- ถ้ามี `active_task` → สั่ง Claude CLI เขียนตอนถัดไป
- ถ้าติด rate limit → รอ 2 นาที แล้วลองใหม่อัตโนมัติ
- ไม่ต้องเปิด VS Code หรือกดอะไร

### Limit Handoff Protocol (VS Code → Background Worker):
เมื่อ Claude Code ใน VS Code กำลังเขียนแล้วใกล้ถูก interrupt:
1. **อัปเดต `writing-state.json` ทันที** — บันทึก last_completed_chapter ล่าสุด
2. แจ้ง user: "บันทึก state แล้ว background worker จะเขียนต่อเอง"
3. Background worker จะหยิบ active_task ไปทำต่ออัตโนมัติ
4. เมื่อ user เปิด VS Code ใหม่: เช็ค `worker_status` ใน state file
   - ถ้า worker กำลังทำอยู่ → แจ้ง "worker กำลังเขียนตอนที่ X อยู่"
   - ถ้า worker เสร็จแล้ว → แจ้ง "worker เขียนเสร็จถึงตอนที่ X แล้ว"

### Worker Control:
```bash
./agents/queue/novel-worker-ctl.sh start     # เริ่ม worker
./agents/queue/novel-worker-ctl.sh stop      # หยุด
./agents/queue/novel-worker-ctl.sh status    # ดูสถานะ
./agents/queue/novel-worker-ctl.sh install   # ติดตั้ง auto-start on boot
```

---

## Brave Search API Quota Rules

**Limit: 2,000 queries/เดือน (Free Tier)**

### กฎบังคับ
1. **ก่อนค้นหาทุกครั้ง** ต้องอ่านไฟล์ `knowledge-base/brave-search-usage.md` เพื่อตรวจยอดใช้งาน
2. **ห้ามค้นหาถ้ายอดเหลือ 0** ให้แจ้ง user ว่า quota หมดแล้ว รอเดือนถัดไป
3. **หลังค้นหาทุกครั้ง** ต้องอัปเดตยอดใช้งานในไฟล์ `knowledge-base/brave-search-usage.md`
4. **เตือน user เมื่อเหลือ < 200 queries** (10% ของ quota)

### กลยุทธ์ประหยัด Quota
- ตรวจ Knowledge Base ก่อนเสมอ ถ้ามีข้อมูลแล้วไม่ต้องค้นหาใหม่
- รวมคำค้นหาให้กระชับ ไม่ค้นซ้ำซ้อน
- ใช้ WebFetch กับ URL ที่รู้อยู่แล้วแทน (ไม่นับ quota)
- บันทึกผล research ทุกครั้งลง Knowledge Base เพื่อใช้ซ้ำ
- ใช้ความรู้ที่มีอยู่แล้วก่อน ค้นหาเฉพาะสิ่งที่ไม่แน่ใจจริงๆ

### Budget แนะนำ
| หมวด | Queries/เดือน | หมายเหตุ |
|------|-------------|---------|
| Historical Research | 600 | นิยายย้อนยุค |
| Fact Checking | 400 | การแพทย์/กฎหมาย/อาชีพ |
| Genre Research | 300 | ศึกษาแนวใหม่ |
| General Research | 500 | ทั่วไป |
| Reserve | 200 | สำรองฉุกเฉิน |
| **รวม** | **2,000** | |
