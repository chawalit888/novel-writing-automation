# 🚀 Deployment Guide - Novel Promo Website

## ข้อมูลโครงการ
- **Framework**: Next.js 16.1.6
- **แพลตฟอร์มแนะนำ**: Vercel
- **นิยายทั้งหมด**: 24 เรื่อง
- **ตอนทั้งหมด**: ~650 ตอน
- **ตอนฟรี**: 10 ตอนแรกของแต่ละเรื่อง

---

## วิธี Deploy ไป Vercel (แนะนำ - ฟรี)

### ขั้นตอนที่ 1: เตรียม Git Repository

```bash
# เช็คสถานะ git
cd novel-promo-site
git status

# Commit การเปลี่ยนแปลงล่าสุด (ถ้ามี)
git add .
git commit -m "เตรียม deploy production"

# Push ขึ้น GitHub (ถ้ายังไม่มี remote)
# สร้าง repository ใหม่บน GitHub ก่อน
git remote add origin https://github.com/YOUR_USERNAME/novel-promo-site.git
git branch -M main
git push -u origin main
```

### ขั้นตอนที่ 2: Deploy ผ่าน Vercel Dashboard (ง่ายที่สุด)

1. **เปิดบราวเซอร์** ไปที่ https://vercel.com
2. **Sign up/Login** ด้วย GitHub account
3. **คลิก "Add New Project"**
4. **Import repository** `novel-promo-site` จาก GitHub
5. **Configure Project**:
   - Framework Preset: **Next.js** (จะตรวจจับอัตโนมัติ)
   - Root Directory: `./` (ถ้าเป็น monorepo ให้เลือก `novel-promo-site/`)
   - Build Command: `npm run build` (ใช้ default)
   - Output Directory: `.next` (ใช้ default)

6. **ตั้งค่า Environment Variables**:
   - คลิก "Environment Variables"
   - เพิ่ม:
     ```
     SITE_URL = https://your-project.vercel.app
     API_KEY = your-secure-random-api-key-here
     ```

7. **คลิก Deploy** 🚀

8. **รอประมาณ 2-3 นาที** Vercel จะ build และ deploy ให้อัตโนมัติ

9. **ได้ URL**: `https://your-project.vercel.app`

---

### ขั้นตอนที่ 3: Deploy ผ่าน Vercel CLI (สำหรับ Advanced)

```bash
# ติดตั้ง Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy (จากในโฟลเดอร์ novel-promo-site)
cd novel-promo-site
vercel

# ตอบคำถาม:
# - Set up and deploy? Yes
# - Which scope? (เลือก account ของคุณ)
# - Link to existing project? No
# - Project name? novel-promo-site
# - In which directory? ./
# - Want to override settings? No

# Deploy to production
vercel --prod
```

---

## ตั้งค่า Custom Domain (ถ้าต้องการ)

### ที่ Vercel Dashboard:
1. เข้า Project Settings
2. ไปที่ Domains
3. เพิ่ม domain ของคุณ: เช่น `novels.yourdomain.com`
4. ทำตาม DNS settings ที่ Vercel แนะนำ:
   - **A Record**: ชื่อ `@` ชี้ไป `76.76.21.21`
   - **CNAME**: ชื่อ `www` ชื้ไป `cname.vercel-dns.com`

5. รอ DNS propagate (5-60 นาที)
6. Vercel จะ issue SSL certificate อัตโนมัติ

---

## หลัง Deploy แล้ว

### ✅ เช็คว่าทำงานถูกต้อง:
- [ ] หน้าแรกโหลดได้
- [ ] รายชื่อนิยายแสดงครบ 24 เรื่อง
- [ ] คลิกเข้าหน้านิยายเห็นรายละเอียด + ปุ่มแพลตฟอร์ม
- [ ] อ่านตอนฟรี 10 ตอนแรกได้
- [ ] ตอนที่ 11+ แสดงว่า Premium
- [ ] ภาพปกขนาดถูกต้อง (1:1 square)
- [ ] Responsive บนมือถือ

### 🔄 อัปเดตเว็บในอนาคต:

ทุกครั้งที่ push ใหม่ไป GitHub:
```bash
git add .
git commit -m "อัปเดตตอนใหม่"
git push
```

**Vercel จะ auto-deploy ให้อัตโนมัติภายใน 1-2 นาที!** 🎉

---

## Environment Variables สำหรับ Production

อัปเดตค่าเหล่านี้ที่ Vercel Dashboard:

```env
# Site URL (เปลี่ยนเป็น domain จริงของคุณ)
SITE_URL=https://your-project.vercel.app

# API Key (สร้าง random key ที่ปลอดภัย)
API_KEY=prod-your-secure-random-api-key-min-32-chars
```

**วิธีสร้าง API Key ที่ปลอดภัย:**
```bash
# macOS/Linux
openssl rand -base64 32

# หรือใช้ online generator: https://www.uuidgenerator.net/
```

---

## ติดปัญหา?

### Build Error:
```bash
# ลอง build ใหม่ local
npm run build

# ถ้าผ่าน local แต่ fail บน Vercel
# ตรวจสอบ Node version ตรงกันไหม
```

### Environment Variables ไม่ทำงาน:
- ต้องใส่ที่ Vercel Dashboard → Settings → Environment Variables
- ใส่แล้วต้อง Redeploy

### 404 Error:
- ตรวจสอบว่า content files (novels, chapters) ถูก commit ขึ้น git แล้ว
- ตรวจสอบ `.gitignore` ไม่ได้ ignore `/src/content`

---

## Performance Tips

Vercel จัดการให้อัตโนมัติแล้ว:
- ✅ CDN ทั่วโลก
- ✅ Image optimization
- ✅ Edge caching
- ✅ Automatic HTTPS
- ✅ DDoS protection

---

## ค่าใช้จ่าย

**Vercel Hobby Plan (FREE):**
- ✅ Unlimited deployments
- ✅ Automatic HTTPS
- ✅ 100 GB bandwidth/เดือน
- ✅ Edge Network
- ✅ เว็บนิยายของคุณใช้ Free plan ได้สบายๆ

**ถ้าเว็บโตมาก** (มากกว่า 100 GB/เดือน):
- Vercel Pro: $20/เดือน (1 TB bandwidth)

---

## 🎯 Checklist ก่อน Deploy

- [x] ✅ Build local สำเร็จ (`npm run build`)
- [x] ✅ ตอนฟรี 10 ตอนแรกแสดงถูกต้อง
- [x] ✅ ปุ่มแพลตฟอร์มแสดงลิงก์ถูกต้อง
- [x] ✅ ภาพปกเป็น 1:1 square
- [x] ✅ นิยายทั้งหมด 24 เรื่อง มีตอนครบ
- [ ] Git commit & push ขึ้น GitHub
- [ ] Deploy ไป Vercel
- [ ] ตั้งค่า Environment Variables
- [ ] ทดสอบเว็บ production

---

## 📞 Support

ถ้าติดปัญหาการ deploy:
- Vercel Docs: https://vercel.com/docs
- Vercel Discord: https://vercel.com/discord
- Next.js Docs: https://nextjs.org/docs
