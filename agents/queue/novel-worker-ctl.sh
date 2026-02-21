#!/bin/bash
# =============================================================
# Novel Worker Control Script
# ควบคุม background worker: start / stop / status / log
# =============================================================

PROJECT_DIR="/Users/chawalitnoi/Projects/Novel Writing Automation Project"
WORKER_SCRIPT="$PROJECT_DIR/agents/queue/novel-worker.sh"
LOG_DIR="$PROJECT_DIR/agents/queue/data"
LOG_FILE="$LOG_DIR/worker.log"
PID_FILE="$LOG_DIR/worker.pid"
STATE_FILE="$PROJECT_DIR/writing-state.json"
PLIST_NAME="com.novelempire.worker"
PLIST_FILE="$HOME/Library/LaunchAgents/$PLIST_NAME.plist"

# สี
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo ""
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE}  Novel Worker Control${NC}"
    echo -e "${BLUE}================================================${NC}"
    echo ""
}

is_running() {
    if [ -f "$PID_FILE" ]; then
        local pid
        pid=$(cat "$PID_FILE")
        if kill -0 "$pid" 2>/dev/null; then
            return 0
        fi
    fi
    return 1
}

get_worker_status() {
    python3 -c "
import json
try:
    with open('$STATE_FILE') as f:
        state = json.load(f)
    ws = state.get('worker_status', {})
    status = ws.get('status', 'unknown')
    pid = ws.get('pid', 'N/A')
    updated = ws.get('updated_at', 'N/A')

    task = state.get('active_task')
    if task:
        story = task.get('story_id', '?')
        current = task.get('current_chapter', '?')
        target = task.get('target_chapter', '?')
        last = task.get('last_completed_chapter', '?')
        print(f'status:{status}')
        print(f'pid:{pid}')
        print(f'updated:{updated}')
        print(f'story:{story}')
        print(f'current:{current}')
        print(f'target:{target}')
        print(f'last_completed:{last}')
    else:
        print(f'status:{status}')
        print(f'pid:{pid}')
        print(f'updated:{updated}')
        print('story:none')
except Exception as e:
    print(f'status:error')
    print(f'error:{e}')
" 2>/dev/null
}

cmd_start() {
    print_header

    # เช็คว่า claude CLI ติดตั้งแล้วยัง
    if ! command -v claude &>/dev/null; then
        echo -e "${RED}Claude Code CLI ยังไม่ได้ติดตั้ง${NC}"
        echo ""
        echo "ติดตั้งด้วยคำสั่ง:"
        echo -e "  ${YELLOW}npm install -g @anthropic-ai/claude-code${NC}"
        echo ""
        echo "แล้ว login ครั้งเดียว:"
        echo -e "  ${YELLOW}claude${NC}  (เปิด interactive → login → แล้วออก)"
        exit 1
    fi

    if is_running; then
        local pid
        pid=$(cat "$PID_FILE")
        echo -e "${YELLOW}Worker กำลังทำงานอยู่แล้ว (PID: $pid)${NC}"
        return
    fi

    mkdir -p "$LOG_DIR"

    echo -e "${GREEN}Starting Novel Worker...${NC}"
    nohup bash "$WORKER_SCRIPT" >> "$LOG_FILE" 2>&1 &

    sleep 1

    if is_running; then
        local pid
        pid=$(cat "$PID_FILE")
        echo -e "${GREEN}Worker started (PID: $pid)${NC}"
        echo ""
        echo "ดู log: $0 log"
        echo "ดูสถานะ: $0 status"
    else
        echo -e "${RED}Failed to start worker${NC}"
        echo "ดู log: tail -20 $LOG_FILE"
    fi
}

cmd_stop() {
    print_header

    if ! is_running; then
        echo -e "${YELLOW}Worker ไม่ได้ทำงานอยู่${NC}"
        rm -f "$PID_FILE"
        return
    fi

    local pid
    pid=$(cat "$PID_FILE")
    echo -e "${YELLOW}Stopping worker (PID: $pid)...${NC}"
    kill "$pid" 2>/dev/null

    # รอให้หยุด
    local count=0
    while kill -0 "$pid" 2>/dev/null && [ $count -lt 10 ]; do
        sleep 1
        count=$((count + 1))
    done

    if kill -0 "$pid" 2>/dev/null; then
        echo -e "${RED}Force killing...${NC}"
        kill -9 "$pid" 2>/dev/null
    fi

    rm -f "$PID_FILE"
    echo -e "${GREEN}Worker stopped${NC}"
}

cmd_status() {
    print_header

    # Process status
    if is_running; then
        local pid
        pid=$(cat "$PID_FILE")
        echo -e "Process: ${GREEN}Running${NC} (PID: $pid)"
    else
        echo -e "Process: ${RED}Stopped${NC}"
    fi

    # Worker status from state file
    local info
    info=$(get_worker_status)

    local status story current target last_completed
    status=$(echo "$info" | grep "^status:" | cut -d: -f2-)
    story=$(echo "$info" | grep "^story:" | cut -d: -f2-)
    current=$(echo "$info" | grep "^current:" | cut -d: -f2-)
    target=$(echo "$info" | grep "^target:" | cut -d: -f2-)
    last_completed=$(echo "$info" | grep "^last_completed:" | cut -d: -f2-)

    echo -e "Worker status: ${BLUE}$status${NC}"
    echo ""

    if [ "$story" != "none" ] && [ -n "$story" ]; then
        echo -e "${BLUE}--- งานปัจจุบัน ---${NC}"
        echo "  เรื่อง: $story"
        echo "  ตอนถัดไป: $current"
        echo "  เป้าหมาย: $target"
        echo "  ตอนล่าสุดที่เสร็จ: $last_completed"

        if [ "$target" != "?" ] && [ "$last_completed" != "?" ]; then
            local progress
            progress=$(python3 -c "
t = int('$target') if '$target'.isdigit() else 0
l = int('$last_completed') if '$last_completed'.isdigit() else 0
pct = (l / t * 100) if t > 0 else 0
bar_len = 30
filled = int(pct / 100 * bar_len)
bar = '#' * filled + '-' * (bar_len - filled)
print(f'[{bar}] {pct:.0f}% ({l}/{t})')
" 2>/dev/null)
            echo "  Progress: $progress"
        fi
    else
        echo -e "${YELLOW}ไม่มีงานอยู่ในคิว${NC}"
    fi

    # launchd status
    echo ""
    if [ -f "$PLIST_FILE" ]; then
        if launchctl list | grep -q "$PLIST_NAME" 2>/dev/null; then
            echo -e "launchd service: ${GREEN}Loaded (auto-start on boot)${NC}"
        else
            echo -e "launchd service: ${YELLOW}Installed but not loaded${NC}"
        fi
    else
        echo -e "launchd service: ${RED}Not installed${NC}"
        echo "  ติดตั้ง: $0 install"
    fi

    echo ""
}

cmd_log() {
    if [ ! -f "$LOG_FILE" ]; then
        echo "ยังไม่มี log"
        return
    fi

    echo -e "${BLUE}=== Worker Log (last 30 lines) ===${NC}"
    tail -30 "$LOG_FILE"
    echo ""
    echo -e "${YELLOW}ดู log แบบ real-time: tail -f $LOG_FILE${NC}"
}

cmd_install() {
    print_header
    echo -e "${BLUE}Installing macOS launchd service...${NC}"

    # สร้าง plist
    mkdir -p "$HOME/Library/LaunchAgents"

    cat > "$PLIST_FILE" << PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>$PLIST_NAME</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$WORKER_SCRIPT</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>WorkingDirectory</key>
    <string>$PROJECT_DIR</string>
    <key>StandardOutPath</key>
    <string>$LOG_DIR/launchd-out.log</string>
    <key>StandardErrorPath</key>
    <string>$LOG_DIR/launchd-err.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/opt/homebrew/bin</string>
    </dict>
</dict>
</plist>
PLIST

    echo -e "${GREEN}Plist created: $PLIST_FILE${NC}"

    # Load
    launchctl load "$PLIST_FILE" 2>/dev/null
    echo -e "${GREEN}Service loaded! Worker จะทำงานอัตโนมัติเมื่อเปิดเครื่อง${NC}"
    echo ""
    echo "คำสั่งอื่น:"
    echo "  หยุด service: launchctl unload $PLIST_FILE"
    echo "  ดูสถานะ: $0 status"
}

cmd_uninstall() {
    print_header

    if [ -f "$PLIST_FILE" ]; then
        launchctl unload "$PLIST_FILE" 2>/dev/null
        rm -f "$PLIST_FILE"
        echo -e "${GREEN}Service removed${NC}"
    else
        echo -e "${YELLOW}Service ไม่ได้ติดตั้ง${NC}"
    fi
}

# ============= Main =============
case "${1:-}" in
    start)
        cmd_start
        ;;
    stop)
        cmd_stop
        ;;
    restart)
        cmd_stop
        sleep 2
        cmd_start
        ;;
    status)
        cmd_status
        ;;
    log)
        cmd_log
        ;;
    install)
        cmd_install
        ;;
    uninstall)
        cmd_uninstall
        ;;
    *)
        print_header
        echo "Usage: $0 {start|stop|restart|status|log|install|uninstall}"
        echo ""
        echo "  start      เริ่ม worker (manual)"
        echo "  stop       หยุด worker"
        echo "  restart    restart worker"
        echo "  status     ดูสถานะ worker + งานปัจจุบัน"
        echo "  log        ดู log ล่าสุด"
        echo "  install    ติดตั้ง macOS service (auto-start on boot)"
        echo "  uninstall  ลบ macOS service"
        echo ""
        ;;
esac
