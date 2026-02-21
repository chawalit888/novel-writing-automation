#!/bin/bash

# ===========================================
# NC Server Setup - Step 2: Install SillyTavern
# ===========================================

set -e

echo "============================================"
echo "  NC Writing Server Setup - Step 2"
echo "  ติดตั้ง SillyTavern"
echo "============================================"
echo ""

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ---------------------------------------------
# Step 2.1: ติดตั้ง Node.js
# ---------------------------------------------
echo -e "${BLUE}[1/4]${NC} ตรวจสอบ Node.js..."

if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}ไม่พบ Node.js กำลังติดตั้ง...${NC}"
    brew install node
else
    NODE_VERSION=$(node -v)
    echo -e "${GREEN}✓ Node.js พร้อมใช้งาน ($NODE_VERSION)${NC}"
fi

# ---------------------------------------------
# Step 2.2: ติดตั้ง Git
# ---------------------------------------------
echo ""
echo -e "${BLUE}[2/4]${NC} ตรวจสอบ Git..."

if ! command -v git &> /dev/null; then
    echo -e "${YELLOW}ไม่พบ Git กำลังติดตั้ง...${NC}"
    brew install git
else
    echo -e "${GREEN}✓ Git พร้อมใช้งาน${NC}"
fi

# ---------------------------------------------
# Step 2.3: Clone SillyTavern
# ---------------------------------------------
echo ""
echo -e "${BLUE}[3/4]${NC} ติดตั้ง SillyTavern..."

SILLYTAVERN_DIR="$HOME/SillyTavern"

if [ -d "$SILLYTAVERN_DIR" ]; then
    echo -e "${YELLOW}พบ SillyTavern อยู่แล้ว กำลังอัพเดท...${NC}"
    cd "$SILLYTAVERN_DIR"
    git pull
else
    echo "กำลัง Clone SillyTavern..."
    git clone https://github.com/SillyTavern/SillyTavern.git "$SILLYTAVERN_DIR"
    cd "$SILLYTAVERN_DIR"
fi

echo "กำลังติดตั้ง dependencies..."
npm install

echo -e "${GREEN}✓ SillyTavern ติดตั้งเสร็จ${NC}"

# ---------------------------------------------
# Step 2.4: สร้าง Startup Script
# ---------------------------------------------
echo ""
echo -e "${BLUE}[4/4]${NC} สร้าง Startup Scripts..."

STARTUP_SCRIPT="$HOME/start-nc-server.sh"

cat > "$STARTUP_SCRIPT" << 'EOF'
#!/bin/bash
echo "Starting NC Writing Server..."
echo ""

if ! pgrep -x "ollama" > /dev/null; then
    echo "Starting Ollama..."
    ollama serve &
    sleep 3
fi

echo "Starting SillyTavern..."
cd ~/SillyTavern
npm start
EOF

chmod +x "$STARTUP_SCRIPT"

# Desktop shortcut
DESKTOP_SCRIPT="$HOME/Desktop/NC-Server.command"

cat > "$DESKTOP_SCRIPT" << 'EOF'
#!/bin/bash
cd ~
./start-nc-server.sh
EOF

chmod +x "$DESKTOP_SCRIPT"

echo -e "${GREEN}✓ สร้าง Startup Scripts เสร็จ${NC}"

# ---------------------------------------------
# แสดงผลสรุป
# ---------------------------------------------
echo ""
echo "============================================"
echo -e "${GREEN}  ✓ ติดตั้ง SillyTavern เสร็จสิ้น!${NC}"
echo "============================================"
echo ""
echo "วิธีเริ่มใช้งาน:"
echo ""
echo "  1. ดับเบิลคลิก 'NC-Server' บน Desktop"
echo "     หรือรัน: ~/start-nc-server.sh"
echo ""
echo "  2. เปิด Browser ไปที่:"
echo "     http://localhost:8000"
echo ""
echo "  3. ตั้งค่า API:"
echo "     - Settings (ฟันเฟือง) → API"
echo "     - เลือก Text Completion → Ollama"
echo "     - URL: http://localhost:11434"
echo ""
