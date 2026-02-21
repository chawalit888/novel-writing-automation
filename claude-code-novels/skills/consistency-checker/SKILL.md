# Consistency Checker Skill

## Overview
Skill สำหรับตรวจสอบความสอดคล้องของนิยาย ทั้งตัวละคร timeline และ world building

## Usage
```
"ตรวจ consistency บทที่ 1-5"
"ตรวจว่าตัวละครทำตัวสอดคล้องไหม"
"ตรวจ timeline ของเรื่อง"
"ตรวจ magic system consistency"
```

## Types of Consistency

### 1. Character Consistency
ตัวละครต้องทำตัวสอดคล้องกับ:
- บุคลิกที่กำหนดไว้
- Background และประสบการณ์
- Motivation และ goals
- Speech patterns
- Skill levels

### 2. Timeline Consistency
- ลำดับเหตุการณ์ถูกต้อง
- ระยะเวลาที่ผ่านไปสมเหตุสมผล
- อายุตัวละครถูกต้อง
- เหตุการณ์ไม่ขัดแย้งกัน
- วัน/เวลาที่กล่าวถึงตรงกัน

### 3. World Consistency
- กฎของโลก (physics, magic, society)
- ภูมิศาสตร์และระยะทาง
- วัฒนธรรมและขนบธรรมเนียม
- เทคโนโลยีและความสามารถ
- ประวัติศาสตร์ของโลก

### 4. Plot Consistency
- Cause and effect
- Setups และ payoffs
- ข้อมูลที่ตัวละครรู้
- การตัดสินใจสมเหตุสมผล

## Checking Process

### Step 1: Gather References
1. อ่าน character sheets
2. อ่าน world building docs
3. อ่าน timeline
4. อ่าน previous chapters

### Step 2: Analyze Chapter
1. List ตัวละครที่ปรากฏ
2. List เหตุการณ์ที่เกิด
3. List สถานที่
4. List เวลา/วันที่
5. List การใช้ magic/powers

### Step 3: Cross-Reference
1. ตรวจ character behavior vs character sheet
2. ตรวจ events vs timeline
3. ตรวจ abilities vs established rules
4. ตรวจ locations vs world map

### Step 4: Report Issues
1. ระดับความรุนแรง (Critical/Major/Minor)
2. บทและตำแหน่งที่พบ
3. รายละเอียดปัญหา
4. คำแนะนำในการแก้ไข

## Common Issues

### Character Issues

#### Personality Shift
**ปัญหา:** ตัวละครทำตัวขัดกับบุคลิก
**ตัวอย่าง:** ตัวละครขี้อายพูดมากผิดปกติ
**วิธีแก้:**
- ให้เหตุผลในเรื่อง
- หรือแก้ไขให้สอดคล้อง

#### Knowledge Inconsistency
**ปัญหา:** ตัวละครรู้สิ่งที่ไม่ควรรู้
**ตัวอย่าง:** รู้ความลับที่ยังไม่ถูกเปิดเผย
**วิธีแก้:**
- เพิ่มฉากที่รู้
- หรือเอาออก

#### Ability Inconsistency
**ปัญหา:** ทำสิ่งที่ไม่ควรทำได้
**ตัวอย่าง:** ใช้ magic ที่ยังไม่ได้เรียน
**วิธีแก้:**
- เพิ่ม training scene
- หรือลด ability level

### Timeline Issues

#### Impossible Timing
**ปัญหา:** เหตุการณ์เกิดในเวลาที่เป็นไปไม่ได้
**ตัวอย่าง:** เดินทาง 100 กม. ใน 1 ชั่วโมงด้วยเท้า
**วิธีแก้:**
- ปรับเวลา
- หรือเพิ่มวิธีการเดินทาง

#### Wrong Sequence
**ปัญหา:** เหตุการณ์เกิดผิดลำดับ
**ตัวอย่าง:** พูดถึงเหตุการณ์ที่ยังไม่เกิด
**วิธีแก้:**
- สลับลำดับเหตุการณ์
- หรือแก้ไขการอ้างอิง

#### Date/Time Errors
**ปัญหา:** วันเวลาไม่ตรงกัน
**ตัวอย่าง:** บอกว่าผ่านไป 3 วัน แต่กลายเป็นเดือนถัดไป
**วิธีแก้:**
- ตรวจสอบและแก้ไขตัวเลข

### World Issues

#### Rule Violations
**ปัญหา:** ทำสิ่งที่ขัดกับกฎของโลก
**ตัวอย่าง:** บินได้ทั้งที่ magic system บอกว่าทำไม่ได้
**วิธีแก้:**
- เพิ่มข้อยกเว้น (ถ้าสมเหตุสมผล)
- หรือแก้ไขฉาก

#### Geography Errors
**ปัญหา:** สถานที่ไม่ตรงกับแผนที่/คำอธิบาย
**ตัวอย่าง:** เมืองทางเหนือกลายเป็นทางใต้
**วิธีแก้:**
- แก้ไขทิศทาง
- หรืออัพเดทแผนที่

## Output Format

### Consistency Report
```markdown
# Consistency Report: [Project Name]
## Chapters Reviewed: X-Y
## Date: YYYY-MM-DD

---

## Critical Issues (ต้องแก้ไขทันที)

### Issue #1
- **Type:** [Character/Timeline/World/Plot]
- **Location:** Chapter X, paragraph Y
- **Description:**
- **Reference:** [เอกสารที่ขัดแย้ง]
- **Suggested Fix:**

---

## Major Issues (ควรแก้ไข)
...

## Minor Issues (แก้ไขถ้ามีเวลา)
...

---

## Summary
- Critical: X
- Major: X
- Minor: X

## Recommendations
1.
2.
```

## Rules Files

### character-rules.json
ดู: `rules/character-rules.json`
- กฎสำหรับตรวจ character consistency

### world-rules.json
ดู: `rules/world-rules.json`
- กฎสำหรับตรวจ world consistency

## Best Practices

1. **ตรวจทุก 3-5 บท** - ไม่รอจนจบเรื่อง
2. **Update metadata หลังเขียน** - Timeline, relationships
3. **ใช้ checklist** - ทุกครั้งที่เขียนจบบท
4. **Cross-reference เสมอ** - กับ character sheets
5. **Document exceptions** - ถ้ามีข้อยกเว้น ให้จดไว้

## Automation

สามารถใช้ `tools/consistency_checker.py` สำหรับ:
- ตรวจชื่อตัวละครที่พิมพ์ผิด
- ตรวจ timeline conflicts
- ตรวจคำที่ใช้ซ้ำมากเกินไป
- Generate report อัตโนมัติ
