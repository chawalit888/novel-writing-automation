# Cover Generator Skill (06)

## Overview
Skill สำหรับสร้าง Prompt หน้าปกนิยาย สำหรับใช้กับ AI Image Generator (Nanobanana Pro)

---

## Specifications

| Setting | Value |
|---------|-------|
| ขนาด | 900 x 900 px (Square) |
| สไตล์ | Typography-Focused |
| หลีกเลี่ยง | รูปภาพที่อาจติดลิขสิทธิ์ |

---

## หลักการ Typography-Focused Cover

### ทำไมต้อง Typography-Focused?

1. **หลีกเลี่ยงลิขสิทธิ์** - ไม่ใช้รูปคน/ตัวละคร/ฉากที่อาจละเมิด
2. **ดูมืออาชีพ** - นิยายดังหลายเรื่องใช้แบบนี้
3. **อ่านง่ายบน Platform** - thumbnail เล็กยังอ่านชื่อได้
4. **สร้างง่าย** - AI ทำได้ดี ไม่ผิดพลาด

---

## องค์ประกอบหน้าปก Typography-Focused

```
┌─────────────────────────────────────┐
│                                     │
│     [BACKGROUND TEXTURE/COLOR]      │
│                                     │
│         ┌─────────────────┐         │
│         │   TITLE TEXT    │         │
│         │   (ชื่อเรื่อง)    │         │
│         └─────────────────┘         │
│                                     │
│         ┌─────────────────┐         │
│         │   SUBTITLE      │         │
│         │   (แนว/tagline) │         │
│         └─────────────────┘         │
│                                     │
│   [DECORATIVE ELEMENTS/SYMBOLS]     │
│                                     │
│         ──── Author ────            │
│                                     │
└─────────────────────────────────────┘
```

---

## สไตล์หน้าปกตามแนวนิยาย

### 1. Romance / Rom-Com
```
Background: Soft gradient (pink, peach, lavender)
Typography: Elegant script font, cursive
Elements: Hearts, flowers, ribbons (abstract)
Colors: Pastel tones, rose gold accents
```

### 2. Mafia / Dark Romance
```
Background: Dark solid (black, deep red, navy)
Typography: Bold serif, gold/silver metallic
Elements: Crown, chains, roses (silhouette)
Colors: Black + Gold, Black + Red
```

### 3. Fantasy / Isekai
```
Background: Gradient (purple, blue, starry)
Typography: Ornate serif, magical glow
Elements: Stars, moons, mystical symbols
Colors: Deep purple, gold, silver, cyan
```

### 4. CEO / Modern
```
Background: Minimal solid (white, gray, black)
Typography: Clean sans-serif, bold
Elements: Geometric lines, minimal shapes
Colors: Black + White, Navy + Gold
```

### 5. Horror / Thriller
```
Background: Dark textured (grunge, fog)
Typography: Distressed, sharp edges
Elements: Blood splatter (abstract), cracks
Colors: Black, red, dark gray
```

### 6. BL / GL
```
Background: Soft gradient, dreamy
Typography: Modern elegant, clean
Elements: Abstract shapes, soft lines
Colors: Blue + Pink, Purple + Pink
```

### 7. Historical / Palace
```
Background: Rich textured (silk, brocade pattern)
Typography: Traditional elegant, Chinese/Thai style
Elements: Cloud patterns, lotus, traditional motifs
Colors: Red + Gold, Jade + Gold
```

---

## Prompt Structure สำหรับ Nanobanana Pro

### Template

```
[STYLE], [BACKGROUND], [MAIN ELEMENT],
typography design, book cover,
title text "[ชื่อเรื่อง]" in [FONT STYLE],
[COLOR SCHEME], [ADDITIONAL ELEMENTS],
square format, 900x900, high quality, professional design,
no people, no faces, no characters, abstract only
```

### ตัวอย่างตามแนว

#### Romance Cover
```
Elegant book cover design, soft pink and peach gradient background,
abstract rose petals floating, typography design,
title text "รักครั้งสุดท้าย" in elegant gold script font,
romantic pastel color scheme, subtle heart patterns,
decorative flourishes, square format, 900x900,
high quality, professional design,
no people, no faces, abstract only
```

#### Mafia Cover
```
Dark luxury book cover design, solid black background with subtle texture,
golden crown silhouette at top, typography design,
title text "เจ้าพ่อหมื่นล้าน" in bold gold metallic serif font,
black and gold color scheme, elegant chain border pattern,
decorative rose silhouette, square format, 900x900,
high quality, professional design,
no people, no faces, abstract only
```

#### Fantasy Cover
```
Mystical book cover design, deep purple to blue gradient background,
scattered stars and magical sparkles, typography design,
title text "หลงภพ" in ornate silver font with magical glow,
fantasy color scheme purple gold silver, crescent moon symbol,
ethereal mist effects, square format, 900x900,
high quality, professional design,
no people, no faces, abstract only
```

---

## Prompts ที่มี

| Prompt | ใช้สำหรับ |
|--------|----------|
| typography-cover.txt | สร้าง prompt หน้าปกทุกแนว |
| color-schemes.txt | ชุดสีตามแนวนิยาย |
| elements-library.txt | องค์ประกอบตกแต่ง |

---

## สิ่งที่ควรใส่

✅ **ใช้ได้:**
- Abstract shapes
- Geometric patterns
- Gradients
- Textures (silk, marble, grunge)
- Symbols (crown, heart, star, moon)
- Silhouettes (flowers, leaves)
- Decorative borders/frames
- Light effects (glow, sparkle, bokeh)

---

## สิ่งที่ห้ามใส่

❌ **ห้ามใช้:**
- รูปคน/ใบหน้า
- ตัวละครจากนิยาย/อนิเมะ
- รูปดารา/นักแสดง
- โลโก้ยี่ห้อ
- ฉากจากหนัง/ซีรีส์
- ภาพถ่ายจริง
- งานศิลปะที่มีลิขสิทธิ์

---

## Negative Prompt

เพิ่มท้าย prompt เสมอ:
```
--negative: people, faces, characters, anime, realistic photo,
copyrighted content, logos, watermark, low quality, blurry
```

---

## Checklist

- [ ] ไม่มีรูปคน/ใบหน้า
- [ ] Typography อ่านชัดเจน
- [ ] สีเหมาะกับแนวนิยาย
- [ ] ขนาด 900x900
- [ ] ดูมืออาชีพ
- [ ] ไม่มีองค์ประกอบที่อาจติดลิขสิทธิ์
