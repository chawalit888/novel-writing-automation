# NC Automation Skills Index

## Overview
รวม Skills ทั้งหมดสำหรับ NC Scene Generation และ Enhancement

---

## Skills ที่มี (5 Skills)

### 1. nc-scene-polish
**หน้าที่:** ขัดเงาและปรับปรุง NC scenes ให้มีคุณภาพสูงขึ้น

**ใช้เมื่อ:**
- Raw scene จาก Ollama ยังไม่สมบูรณ์
- ต้องการเพิ่ม sensory details
- ต้องการปรับ pacing
- ต้องการเพิ่ม emotional depth

**Key Features:**
- Sensory details guide (5 senses)
- Pacing techniques
- Emotional layer enhancement
- Dialogue polish
- Before/After examples

📁 [nc-scene-polish/SKILL.md](nc-scene-polish/SKILL.md)

---

### 2. nc-translation-specialist
**หน้าที่:** แปล NC scenes จากอังกฤษเป็นไทย อย่างมีคุณภาพ

**ใช้เมื่อ:**
- แปล raw scene จาก Ollama (English)
- ต้องการภาษาไทยที่ natural
- ต้องการรักษา intensity

**Key Features:**
- Word choice guide (body parts, actions, sounds)
- Sentence structure patterns
- Dialogue translation rules
- Platform-specific language
- Intensity preservation guide

📁 [nc-translation-specialist/SKILL.md](nc-translation-specialist/SKILL.md)

---

### 3. nc-qc-validator
**หน้าที่:** ตรวจสอบคุณภาพและความเหมาะสมของ NC scenes

**ใช้เมื่อ:**
- ก่อนใช้งาน NC scene
- ตรวจ consent clarity
- ตรวจ character consistency
- ตรวจ intensity accuracy

**Key Features:**
- Consent validation checklist
- Character consistency checks
- Intensity validation scale
- Technical quality metrics
- Validation report template

📁 [nc-qc-validator/SKILL.md](nc-qc-validator/SKILL.md)

---

### 4. character-chemistry-builder
**หน้าที่:** สร้าง Chemistry ระหว่างตัวละครให้น่าเชื่อถือ

**ใช้เมื่อ:**
- วางแผน NC scene ใหม่
- สร้าง tension ระหว่างตัวละคร
- พัฒนา relationship dynamics
- ก่อนเขียน first NC scene

**Key Features:**
- Chemistry types (slow burn, instant spark, etc.)
- Tension techniques
- Dialogue for chemistry
- Physical chemistry cues
- Chemistry template

📁 [character-chemistry-builder/SKILL.md](character-chemistry-builder/SKILL.md)

---

### 5. scene-integration-handler
**หน้าที่:** เชื่อม NC scenes เข้ากับ main story

**ใช้เมื่อ:**
- เขียน transition เข้า NC scene
- เขียน aftermath หลัง NC
- รวม NC เข้ากับ plot
- ต้องการ scene ไม่ลอยตัว

**Key Features:**
- Lead-in techniques
- Transition out patterns
- Story impact integration
- Different scenario handling
- Full integration template

📁 [scene-integration-handler/SKILL.md](scene-integration-handler/SKILL.md)

---

## Workflow แนะนำ

### สร้าง NC Scene ใหม่:
```
1. character-chemistry-builder → สร้าง chemistry
2. Ollama generate → Raw NC scene (English)
3. nc-scene-polish → ขัดเงา
4. nc-translation-specialist → แปลเป็นไทย
5. nc-qc-validator → ตรวจสอบ
6. scene-integration-handler → รวมเข้ากับเรื่อง
```

### ปรับปรุง NC Scene ที่มีอยู่:
```
1. nc-qc-validator → ตรวจหา issues
2. nc-scene-polish → แก้ไข issues
3. nc-translation-specialist → ปรับภาษา (ถ้าจำเป็น)
4. nc-qc-validator → ตรวจสอบอีกครั้ง
```

### เชื่อมเข้ากับเรื่อง:
```
1. scene-integration-handler → วาง lead-in
2. [NC Scene]
3. scene-integration-handler → เขียน aftermath
4. nc-qc-validator → ตรวจสอบ integration
```

---

## Quick Reference

| Skill | ใช้ทำอะไร | Input | Output |
|-------|----------|-------|--------|
| nc-scene-polish | ขัดเงา scene | Raw NC | Polished NC |
| nc-translation-specialist | แปลเป็นไทย | English NC | Thai NC |
| nc-qc-validator | ตรวจคุณภาพ | NC scene | QC Report |
| character-chemistry-builder | สร้าง chemistry | Characters | Chemistry Profile |
| scene-integration-handler | เชื่อมเข้าเรื่อง | NC + Context | Integrated Scene |

---

## Version History

- **v1.0** (2024-01): Initial release with 5 skills
