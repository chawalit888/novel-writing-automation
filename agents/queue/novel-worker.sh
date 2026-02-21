#!/bin/bash
# =============================================================
# Novel Worker Daemon
# Background process ที่เขียนนิยายอัตโนมัติผ่าน Claude Code CLI
# ทำงาน 24/7 — ติด rate limit ก็รอแล้วเขียนต่อเอง
# =============================================================

PROJECT_DIR="/Users/chawalitnoi/Projects/Novel Writing Automation Project"
STATE_FILE="$PROJECT_DIR/writing-state.json"
LOG_DIR="$PROJECT_DIR/agents/queue/data"
LOG_FILE="$LOG_DIR/worker.log"
PID_FILE="$LOG_DIR/worker.pid"

# Config
RETRY_WAIT=120        # วินาทีที่รอเมื่อ error/rate limit
SUCCESS_WAIT=10       # วินาทีพักระหว่างตอน
IDLE_WAIT=300         # วินาทีรอเมื่อไม่มีงาน (5 นาที)
MAX_CONSECUTIVE_FAILS=5  # หยุดชั่วคราวหลัง fail ติดกัน X ครั้ง
LONG_WAIT=600         # วินาทีรอหลัง max consecutive fails (10 นาที)

# สร้าง directories ถ้ายังไม่มี
mkdir -p "$LOG_DIR"

# ============= Logging =============
log() {
    local level="$1"
    local msg="$2"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $msg" >> "$LOG_FILE"
}

log_info() { log "INFO" "$1"; }
log_warn() { log "WARN" "$1"; }
log_error() { log "ERROR" "$1"; }

# ============= State Management =============
check_active_task() {
    # อ่าน writing-state.json ดูว่ามี active_task ไหม
    python3 -c "
import json, sys
try:
    with open('$STATE_FILE') as f:
        state = json.load(f)
    task = state.get('active_task')
    if task and task is not None:
        print('yes')
        print(task.get('story_id', 'unknown'))
        print(task.get('current_chapter', 0))
        print(task.get('target_chapter', 0))
        print(task.get('last_completed_chapter', 0))
    else:
        print('no')
except Exception as e:
    print('error')
    print(str(e), file=sys.stderr)
" 2>>"$LOG_FILE"
}

update_worker_status() {
    local status="$1"
    python3 -c "
import json
from datetime import datetime
try:
    with open('$STATE_FILE', 'r') as f:
        state = json.load(f)
    state['worker_status'] = {
        'status': '$status',
        'pid': $(echo $$),
        'updated_at': datetime.now().isoformat()
    }
    with open('$STATE_FILE', 'w') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
except Exception:
    pass
" 2>>"$LOG_FILE"
}

# ============= Process Management =============
write_pid() {
    echo $$ > "$PID_FILE"
}

cleanup() {
    log_info "Worker shutting down (PID: $$)"
    update_worker_status "stopped"
    rm -f "$PID_FILE"
    exit 0
}

# Trap signals for graceful shutdown
trap cleanup SIGTERM SIGINT SIGHUP

# ============= Main Loop =============
main() {
    write_pid
    log_info "========================================="
    log_info "Novel Worker started (PID: $$)"
    log_info "Project: $PROJECT_DIR"
    log_info "Retry wait: ${RETRY_WAIT}s | Idle wait: ${IDLE_WAIT}s"
    log_info "========================================="
    update_worker_status "running"

    local consecutive_fails=0

    while true; do
        # อ่าน state
        local task_info
        task_info=$(check_active_task)
        local has_task
        has_task=$(echo "$task_info" | head -1)

        if [ "$has_task" = "yes" ]; then
            local story_id current_ch target_ch last_completed
            story_id=$(echo "$task_info" | sed -n '2p')
            current_ch=$(echo "$task_info" | sed -n '3p')
            target_ch=$(echo "$task_info" | sed -n '4p')
            last_completed=$(echo "$task_info" | sed -n '5p')

            log_info "Active task: $story_id | Chapter $current_ch/$target_ch (last completed: $last_completed)"
            update_worker_status "writing"

            # สั่ง Claude CLI เขียน 1 ตอน
            cd "$PROJECT_DIR"

            local output
            output=$(claude -p "อ่าน writing-state.json แล้วเขียนตอนถัดไป 1 ตอน ตาม auto-resume protocol ใน CLAUDE.md อัปเดต writing-state.json หลังเขียนเสร็จ" \
                --dangerously-skip-permissions \
                2>&1)

            local exit_code=$?

            if [ $exit_code -eq 0 ]; then
                log_info "Chapter completed successfully for $story_id"
                consecutive_fails=0
                update_worker_status "running"

                # เช็คว่ายังมีงานต่อไหม
                local new_info
                new_info=$(check_active_task)
                local still_has_task
                still_has_task=$(echo "$new_info" | head -1)

                if [ "$still_has_task" = "yes" ]; then
                    log_info "More chapters to write, continuing after ${SUCCESS_WAIT}s..."
                    sleep "$SUCCESS_WAIT"
                else
                    log_info "All chapters completed! Going idle."
                    update_worker_status "idle"
                    sleep "$IDLE_WAIT"
                fi
            else
                consecutive_fails=$((consecutive_fails + 1))
                log_warn "Failed (exit=$exit_code, consecutive=$consecutive_fails)"

                # Log output snippet for debugging
                local snippet
                snippet=$(echo "$output" | tail -5)
                log_warn "Last output: $snippet"

                if [ $consecutive_fails -ge $MAX_CONSECUTIVE_FAILS ]; then
                    log_error "Too many consecutive failures ($consecutive_fails). Long wait ${LONG_WAIT}s..."
                    update_worker_status "waiting_long"
                    sleep "$LONG_WAIT"
                    consecutive_fails=0  # Reset after long wait
                else
                    log_info "Waiting ${RETRY_WAIT}s before retry..."
                    update_worker_status "waiting_retry"
                    sleep "$RETRY_WAIT"
                fi
            fi

        elif [ "$has_task" = "error" ]; then
            log_error "Error reading state file"
            sleep "$RETRY_WAIT"

        else
            # ไม่มีงาน
            update_worker_status "idle"
            sleep "$IDLE_WAIT"
        fi
    done
}

# Run
main
