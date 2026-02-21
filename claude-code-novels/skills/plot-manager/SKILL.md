# Plot Manager Skill

## Overview
Skill สำหรับวางโครงเรื่องและจัดการ plot ของนิยาย

## Usage
```
"วางโครงเรื่องนิยายแฟนตาซี 25 ตอน"
"สร้าง master outline สำหรับ [ชื่อเรื่อง]"
"วาง subplot สำหรับตัวละครรอง"
```

## Plot Structures

### 1. Three-Act Structure
```
ACT 1 (25%): Setup
├── Introduction
├── Inciting Incident
└── Plot Point 1 (เข้าสู่ Act 2)

ACT 2 (50%): Confrontation
├── Rising Action
├── Midpoint (turning point)
├── More Complications
└── Plot Point 2 (เข้าสู่ Act 3)

ACT 3 (25%): Resolution
├── Pre-climax
├── Climax
└── Resolution
```

### 2. Hero's Journey
```
1. Ordinary World
2. Call to Adventure
3. Refusal of the Call
4. Meeting the Mentor
5. Crossing the Threshold
6. Tests, Allies, Enemies
7. Approach to the Inmost Cave
8. The Ordeal
9. Reward (Seizing the Sword)
10. The Road Back
11. Resurrection
12. Return with the Elixir
```

### 3. Save the Cat Beat Sheet
```
1. Opening Image (1%)
2. Theme Stated (5%)
3. Setup (1-10%)
4. Catalyst (10%)
5. Debate (10-20%)
6. Break into Two (20%)
7. B Story (22%)
8. Fun and Games (20-50%)
9. Midpoint (50%)
10. Bad Guys Close In (50-75%)
11. All Is Lost (75%)
12. Dark Night of the Soul (75-80%)
13. Break into Three (80%)
14. Finale (80-99%)
15. Final Image (99-100%)
```

## Outline Components

### Master Outline
- Premise (1-2 ประโยค)
- Theme
- Main conflict
- Character arcs
- Major plot points
- Subplots
- Chapter breakdown

### Chapter Outline
- Chapter number
- POV character
- Time/Location
- Main events
- Character development
- Subplot progress
- End hook

### Scene Outline
- Scene goal
- Characters present
- Conflict
- Outcome
- Emotion/Tone

## Creating Effective Plots

### The MICE Quotient
- **M**ilieu - เน้น setting/world
- **I**dea - เน้นคำถาม/ปริศนา
- **C**haracter - เน้น character arc
- **E**vent - เน้นเหตุการณ์ใหญ่

### Conflict Types
1. Person vs Person
2. Person vs Nature
3. Person vs Society
4. Person vs Self
5. Person vs Technology
6. Person vs Supernatural

### Tension Techniques
- Ticking clock
- Raising stakes
- Complications
- Reversals
- Revelations
- False victories

## Subplot Management

### Good Subplots
- Support main theme
- Develop characters
- Provide contrast/parallel
- Add complexity
- Have own arc

### Weaving Subplots
- Introduce early
- Touch on regularly
- Converge with main plot
- Resolve before/during climax

## Pacing Guidelines

### Fast Pacing For
- Action scenes
- Tension/suspense
- Chase sequences
- Arguments

### Slow Pacing For
- Character moments
- Emotional scenes
- World building
- Relationship development

### Chapter Length by Position
```
Opening chapters: Medium (establish)
Early middle: Longer (develop)
Midpoint: Medium-long (turning point)
Late middle: Variable (complications)
Climax chapters: Shorter (intensity)
Resolution: Medium (wrap up)
```

## Templates

### Three-Act Structure
ดู: `templates/three-act.md`

### Hero's Journey
ดู: `templates/heros-journey.md`

## Common Plot Problems

### ❌ Sagging Middle
**Problem:** Act 2 ยืดยาด ไม่มีอะไรเกิดขึ้น
**Solution:**
- เพิ่ม complications
- มี midpoint ที่แข็งแรง
- Subplots ที่น่าสนใจ

### ❌ Deus Ex Machina
**Problem:** แก้ปัญหาด้วยสิ่งที่โผล่มาจากไหนไม่รู้
**Solution:**
- Setup ก่อน payoff
- ให้ protagonist แก้ปัญหาเอง
- ใช้สิ่งที่ establish ไว้แล้ว

### ❌ Plot Holes
**Problem:** logic ไม่ต่อกัน
**Solution:**
- Timeline tracking
- Consistency checks
- Beta readers

### ❌ Predictable
**Problem:** ผู้อ่านเดาได้หมด
**Solution:**
- Subvert expectations
- Red herrings
- Unexpected complications

### ❌ No Stakes
**Problem:** ไม่รู้สึกว่าสำคัญ
**Solution:**
- Personal stakes
- Escalating consequences
- Show don't tell

## Checklist

### Before Writing
- [ ] Premise ชัดเจน
- [ ] Theme กำหนดแล้ว
- [ ] Major plot points วางแล้ว
- [ ] Character arcs สอดคล้องกับ plot
- [ ] Subplots วางแผนแล้ว
- [ ] Pacing วางแล้ว

### After Outline
- [ ] ทุก chapter มี purpose
- [ ] Stakes escalate
- [ ] ไม่มี plot holes
- [ ] Setups มี payoffs
- [ ] Climax สอดคล้องกับ theme

## Tools

### Timeline Tracker
ใช้ `metadata/timeline.json` เพื่อ track:
- วันเวลาของเหตุการณ์
- อายุตัวละคร
- ระยะเวลาที่ผ่านไป
- เหตุการณ์พร้อมกัน

### Relationship Tracker
ใช้ `metadata/relationships.json` เพื่อ track:
- ความสัมพันธ์ระหว่างตัวละคร
- การเปลี่ยนแปลงความสัมพันธ์
- Conflict และ alliance
