# Template 06: Cover Prompt Generator

## สำหรับสร้าง Prompt หน้าปกนิยาย (Nanobanana Pro)

---

## ข้อมูลที่ต้องใส่

| Field | คำอธิบาย | ตัวอย่าง |
|-------|---------|---------|
| `title` | ชื่อเรื่อง | หลงภพ ณ วังหลวง |
| `genre` | แนวนิยาย | palace, mafia, romance, fantasy, horror, bl-gl, ceo |
| `mood` | อารมณ์ | dark, romantic, mysterious, bright, elegant |
| `color1` | สีหลัก | red, black, pink, purple, gold |
| `color2` | สีรอง | gold, white, silver, cream |

---

## Prompt Template

### Base Structure
```
[STYLE] book cover design,
[BACKGROUND] background [TEXTURE],
[MAIN_ELEMENT] decorative element,
typography-focused design,
title text "[TITLE]" in [FONT_STYLE] font,
[COMPOSITION] composition, [COLOR_SCHEME] color scheme,
[ADDITIONAL_ELEMENTS],
square format 900x900, high quality professional design,
no people, no faces, no characters, abstract only

--negative: people, faces, characters, anime, realistic photo,
copyrighted content, logos, watermark, low quality, blurry
```

---

## Genre Presets

### 1. Palace / Thai Historical (วังหลวง)
```
Regal Thai palace book cover design,
rich {{color1:red}} silk textured background with subtle brocade pattern,
traditional Thai Lai Thai pattern decorative border,
golden lotus motif centered,
typography-focused design,
title text "{{title}}" in elegant traditional Thai gold font,
imperial centered composition, {{color1:red}} and {{color2:gold}} color scheme,
ornate golden corner flourishes, subtle golden sparkles,
square format 900x900, high quality professional design,
no people, no faces, no characters, abstract only

--negative: people, faces, characters, anime, realistic photo,
copyrighted content, logos, watermark, low quality, blurry
```

### 2. Mafia / Dark Romance (มาเฟีย)
```
Dark luxury book cover design,
solid {{color1:black}} background with subtle velvet texture,
golden crown silhouette centered at top,
decorative chain pattern border,
typography-focused design,
title text "{{title}}" in bold {{color2:gold}} metallic serif font,
dramatic centered composition, {{color1:black}} and {{color2:gold}} color scheme,
rose silhouette with thorns accent, elegant frame,
square format 900x900, high quality professional design,
no people, no faces, no characters, abstract only

--negative: people, faces, characters, anime, photo, watermark
```

### 3. Romance / Rom-Com (โรแมนติก)
```
Elegant romantic book cover design,
soft {{color1:pink}} to {{color2:peach}} gradient background,
floating rose petals scattered pattern,
typography-focused design,
title text "{{title}}" in elegant rose gold script font,
romantic centered composition, pastel {{color1:pink}} gold color scheme,
subtle heart confetti, soft bokeh lights, decorative flourishes,
square format 900x900, high quality professional design,
no people, no faces, no characters, abstract only

--negative: people, faces, characters, anime, photo, watermark
```

### 4. Fantasy / Isekai (แฟนตาซี)
```
Mystical fantasy book cover design,
deep {{color1:purple}} to {{color2:blue}} gradient background,
scattered stars and magical sparkles,
crescent moon symbol centered,
typography-focused design,
title text "{{title}}" in ornate {{color2:silver}} font with magical glow,
ethereal centered composition, fantasy {{color1:purple}} {{color2:silver}} color scheme,
mystical mist effects, floating light particles,
square format 900x900, high quality professional design,
no people, no faces, no characters, abstract only

--negative: people, faces, characters, anime, photo, watermark
```

### 5. Horror / Thriller (สยองขวัญ)
```
Dark atmospheric book cover design,
textured {{color1:black}} grunge background with fog effect,
abstract blood splatter pattern, cracked texture overlay,
typography-focused design,
title text "{{title}}" in distressed {{color2:red}} horror style font,
ominous centered composition, {{color1:black}} {{color2:red}} color scheme,
dark vignette, eerie glow effects,
square format 900x900, high quality professional design,
no people, no faces, no characters, abstract only

--negative: people, faces, characters, gore, anime, photo, watermark
```

### 6. BL / GL (วาย/ยูริ)
```
Dreamy romantic book cover design,
soft {{color1:blue}} to {{color2:pink}} gradient background,
intertwined ribbons abstract pattern,
twin stars symbolic element,
typography-focused design,
title text "{{title}}" in modern elegant {{color2:white}} font,
tender centered composition, pastel {{color1:blue}} {{color2:pink}} color scheme,
soft light effects, gentle sparkles, flowing lines,
square format 900x900, high quality professional design,
no people, no faces, no characters, abstract only

--negative: people, faces, characters, anime, photo, watermark
```

### 7. CEO / Modern (ซีอีโอ)
```
Minimalist modern book cover design,
clean {{color1:charcoal}} solid background,
geometric lines abstract pattern,
minimal shapes decorative element,
typography-focused design,
title text "{{title}}" in bold sans-serif {{color2:white}} font,
sophisticated centered composition, {{color1:charcoal}} {{color2:gold}} color scheme,
thin gold line accents, subtle grid pattern,
square format 900x900, high quality professional design,
no people, no faces, no characters, abstract only

--negative: people, faces, characters, anime, photo, watermark
```

### 8. Chinese Historical (จีนโบราณ)
```
Elegant Chinese historical book cover design,
rich {{color1:crimson}} silk textured background,
traditional cloud pattern decorative border,
golden Chinese knot motif centered,
typography-focused design,
title text "{{title}}" in elegant traditional Chinese brush {{color2:gold}} font,
imperial centered composition, {{color1:crimson}} and {{color2:gold}} color scheme,
plum blossom pattern accents, ornate corner flourishes,
square format 900x900, high quality professional design,
no people, no faces, no characters, abstract only

--negative: people, faces, characters, anime, photo, watermark
```

---

## Color Presets

| Genre | Color1 | Color2 | Accent |
|-------|--------|--------|--------|
| Palace/Thai | red, crimson | gold | white |
| Mafia | black | gold | red |
| Romance | pink, peach | rose gold | white |
| Fantasy | purple, indigo | silver, blue | gold |
| Horror | black | red, blood | gray |
| BL/GL | blue, lavender | pink | white |
| CEO | charcoal, navy | white | gold |
| Chinese | crimson | gold | jade |

---

## Settings สำหรับ Nanobanana Pro

```
Size: 900 x 900
Aspect Ratio: 1:1 (Square)
Quality: High / Best
Style Preset: Graphic Design หรือ Illustration
Guidance Scale: 7-9
Steps: 30-50
```

---

## ตัวอย่างสำเร็จรูป

### "หลงภพ ณ วังหลวง" (Palace)
```
Regal Thai palace book cover design,
rich red silk textured background with subtle brocade pattern,
traditional Thai Lai Thai pattern decorative border,
golden lotus motif centered,
typography-focused design,
title text "หลงภพ ณ วังหลวง" in elegant traditional Thai gold font,
imperial centered composition, red and gold color scheme,
ornate golden corner flourishes, subtle golden sparkles,
square format 900x900, high quality professional design,
no people, no faces, no characters, abstract only

--negative: people, faces, characters, anime, realistic photo,
copyrighted content, logos, watermark, low quality, blurry
```

### "ท่านประธานหมื่นล้านหลงรักยัยคนตาย" (Mafia)
```
Dark luxury book cover design,
solid black background with subtle velvet texture,
golden crown silhouette centered at top,
decorative chain pattern border,
typography-focused design,
title text "ท่านประธานหมื่นล้านหลงรักยัยคนตาย" in bold gold metallic serif font,
dramatic centered composition, black and gold color scheme,
rose silhouette with thorns accent, elegant frame,
square format 900x900, high quality professional design,
no people, no faces, no characters, abstract only

--negative: people, faces, characters, anime, photo, watermark
```

---

## Checklist

- [ ] ชื่อเรื่องถูกต้อง
- [ ] สีเหมาะกับแนว
- [ ] มี negative prompt
- [ ] ไม่มี people/faces/characters
- [ ] ขนาด 900x900
- [ ] Typography อ่านได้ชัด

---

## วิธีใช้

1. **เลือก Genre Preset** ที่ตรงกับแนวนิยาย
2. **แทนที่ {{title}}** ด้วยชื่อเรื่อง
3. **ปรับสี** ตาม Color Presets (ถ้าต้องการ)
4. **Copy prompt** ไปใส่ Nanobanana Pro
5. **ตั้งค่า** Size: 900x900, Quality: High
6. **Generate!**
