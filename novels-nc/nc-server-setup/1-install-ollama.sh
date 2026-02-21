#!/bin/bash

# ===========================================
# NC Server Setup - Step 1: Install Ollama & Models
# สำหรับ Mac Studio M1 Max 64GB
# ===========================================

set -e

echo "============================================"
echo "  NC Writing Server Setup - Step 1"
echo "  ติดตั้ง Ollama และ Models"
echo "============================================"
echo ""

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ---------------------------------------------
# Step 1.1: ตรวจสอบ Homebrew
# ---------------------------------------------
echo -e "${BLUE}[1/5]${NC} ตรวจสอบ Homebrew..."

if ! command -v brew &> /dev/null; then
    echo -e "${YELLOW}ไม่พบ Homebrew กำลังติดตั้ง...${NC}"
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
    eval "$(/opt/homebrew/bin/brew shellenv)"
else
    echo -e "${GREEN}✓ Homebrew พร้อมใช้งาน${NC}"
fi

# ---------------------------------------------
# Step 1.2: ติดตั้ง Ollama
# ---------------------------------------------
echo ""
echo -e "${BLUE}[2/5]${NC} ติดตั้ง Ollama..."

if ! command -v ollama &> /dev/null; then
    echo "กำลังติดตั้ง Ollama..."
    brew install ollama
else
    echo -e "${GREEN}✓ Ollama ติดตั้งแล้ว${NC}"
fi

# ---------------------------------------------
# Step 1.3: Start Ollama Service
# ---------------------------------------------
echo ""
echo -e "${BLUE}[3/5]${NC} เริ่ม Ollama service..."

ollama serve &> /dev/null &
sleep 3
echo -e "${GREEN}✓ Ollama service กำลังทำงาน${NC}"

# ---------------------------------------------
# Step 1.4: ดาวน์โหลด Models
# ---------------------------------------------
echo ""
echo -e "${BLUE}[4/5]${NC} ดาวน์โหลด Models (ใช้เวลาสักครู่)..."
echo ""

echo -e "${YELLOW}กำลังดาวน์โหลด Dolphin Mistral (Uncensored)...${NC}"
ollama pull dolphin-mistral:7b

echo ""
echo -e "${YELLOW}กำลังดาวน์โหลด Dolphin Mixtral 8x7B (คุณภาพสูง)...${NC}"
echo "ขนาดประมาณ 26GB - รอสักครู่..."
ollama pull dolphin-mixtral:8x7b

echo ""
echo -e "${GREEN}✓ ดาวน์โหลด Models เสร็จสิ้น${NC}"

# ---------------------------------------------
# Step 1.5: ตั้งค่าให้เข้าถึงจากเครื่องอื่นได้
# ---------------------------------------------
echo ""
echo -e "${BLUE}[5/5]${NC} ตั้งค่า Network Access..."

PLIST_PATH="$HOME/Library/LaunchAgents/com.ollama.server.plist"
mkdir -p "$HOME/Library/LaunchAgents"

cat > "$PLIST_PATH" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.ollama.server</string>
    <key>ProgramArguments</key>
    <array>
        <string>/opt/homebrew/bin/ollama</string>
        <string>serve</string>
    </array>
    <key>EnvironmentVariables</key>
    <dict>
        <key>OLLAMA_HOST</key>
        <string>0.0.0.0</string>
        <key>OLLAMA_ORIGINS</key>
        <string>*</string>
    </dict>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
EOF

launchctl unload "$PLIST_PATH" 2>/dev/null || true
launchctl load "$PLIST_PATH"

echo -e "${GREEN}✓ Ollama ตั้งค่าให้เข้าถึงจาก network ได้แล้ว${NC}"

# ---------------------------------------------
# แสดงผลสรุป
# ---------------------------------------------
echo ""
echo "============================================"
echo -e "${GREEN}  ✓ ติดตั้ง Ollama เสร็จสิ้น!${NC}"
echo "============================================"
echo ""
echo "Models ที่ติดตั้ง:"
ollama list
echo ""
echo "ทดสอบโดยรัน:"
echo "  ollama run dolphin-mistral:7b"
echo ""
echo "IP ของเครื่องนี้:"
ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "ไม่พบ IP"
echo ""
echo "ขั้นตอนถัดไป: รัน ./2-install-sillytavern.sh"
echo ""
