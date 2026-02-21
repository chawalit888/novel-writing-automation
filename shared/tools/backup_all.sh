#!/bin/bash
# ===========================================
# Backup All Script
# สำรองข้อมูลทั้ง 2 ระบบพร้อมกัน
# ===========================================

set -e

# Configuration
DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"

BACKUP_DIR="${BASE_DIR}/shared/backups/${DATE}"
CLAUDE_CODE_DIR="${BASE_DIR}/claude-code-novels"
N8N_DIR="${BASE_DIR}/n8n-novels"

echo "🔄 Starting backup process..."
echo "   Base directory: ${BASE_DIR}"
echo "   Backup directory: ${BACKUP_DIR}"
echo ""

mkdir -p "$BACKUP_DIR"

# ===========================================
# Backup Claude Code System
# ===========================================
echo "📦 Backing up Claude Code projects..."
if [ -d "${CLAUDE_CODE_DIR}/projects" ]; then
    tar -czf "${BACKUP_DIR}/claude-code-projects_${TIMESTAMP}.tar.gz" \
        -C "${CLAUDE_CODE_DIR}" projects 2>/dev/null || true
    echo "✅ Claude Code projects backed up"
else
    echo "⚠️  Claude Code projects directory not found"
fi

# Backup skills
if [ -d "${CLAUDE_CODE_DIR}/skills" ]; then
    tar -czf "${BACKUP_DIR}/claude-code-skills_${TIMESTAMP}.tar.gz" \
        -C "${CLAUDE_CODE_DIR}" skills 2>/dev/null || true
    echo "✅ Claude Code skills backed up"
fi

# Backup templates
if [ -d "${CLAUDE_CODE_DIR}/templates" ]; then
    tar -czf "${BACKUP_DIR}/claude-code-templates_${TIMESTAMP}.tar.gz" \
        -C "${CLAUDE_CODE_DIR}" templates 2>/dev/null || true
    echo "✅ Claude Code templates backed up"
fi

# ===========================================
# Backup n8n System
# ===========================================
echo ""
echo "📦 Backing up n8n stories..."
if [ -d "${N8N_DIR}/stories" ]; then
    tar -czf "${BACKUP_DIR}/n8n-stories_${TIMESTAMP}.tar.gz" \
        -C "${N8N_DIR}" stories 2>/dev/null || true
    echo "✅ n8n stories backed up"
else
    echo "⚠️  n8n stories directory not found"
fi

# Backup n8n workflows
echo "📦 Backing up n8n workflows..."
if [ -d "${N8N_DIR}/n8n-data/workflows" ]; then
    tar -czf "${BACKUP_DIR}/n8n-workflows_${TIMESTAMP}.tar.gz" \
        -C "${N8N_DIR}/n8n-data" workflows 2>/dev/null || true
    echo "✅ n8n workflows backed up"
else
    echo "⚠️  n8n workflows directory not found"
fi

# Backup n8n prompts
if [ -d "${N8N_DIR}/prompts" ]; then
    tar -czf "${BACKUP_DIR}/n8n-prompts_${TIMESTAMP}.tar.gz" \
        -C "${N8N_DIR}" prompts 2>/dev/null || true
    echo "✅ n8n prompts backed up"
fi

# Backup database (if docker is running)
echo ""
echo "📦 Attempting database backup..."
if command -v docker &> /dev/null; then
    if docker ps --format '{{.Names}}' | grep -q 'n8n-postgres'; then
        docker exec n8n-postgres pg_dump -U n8n n8n_novels > "${BACKUP_DIR}/database_${TIMESTAMP}.sql" 2>/dev/null || true
        if [ -s "${BACKUP_DIR}/database_${TIMESTAMP}.sql" ]; then
            gzip "${BACKUP_DIR}/database_${TIMESTAMP}.sql"
            echo "✅ Database backed up"
        else
            rm -f "${BACKUP_DIR}/database_${TIMESTAMP}.sql"
            echo "⚠️  Database backup empty or failed"
        fi
    else
        echo "⚠️  PostgreSQL container not running"
    fi
else
    echo "⚠️  Docker not available"
fi

# ===========================================
# Backup shared resources
# ===========================================
echo ""
echo "📦 Backing up shared resources..."
SHARED_DIR="${BASE_DIR}/shared"
if [ -d "${SHARED_DIR}/templates" ]; then
    tar -czf "${BACKUP_DIR}/shared-templates_${TIMESTAMP}.tar.gz" \
        -C "${SHARED_DIR}" templates 2>/dev/null || true
fi
if [ -d "${SHARED_DIR}/prompts" ]; then
    tar -czf "${BACKUP_DIR}/shared-prompts_${TIMESTAMP}.tar.gz" \
        -C "${SHARED_DIR}" prompts 2>/dev/null || true
fi
echo "✅ Shared resources backed up"

# ===========================================
# Create combined archive
# ===========================================
echo ""
echo "🗜️  Creating combined archive..."
COMBINED_ARCHIVE="${BASE_DIR}/shared/backups/full_backup_${TIMESTAMP}.tar.gz"
tar -czf "$COMBINED_ARCHIVE" -C "${BASE_DIR}/shared/backups" "${DATE}" 2>/dev/null || true
echo "✅ Combined archive created"

# ===========================================
# Cleanup old backups (keep last 30 days)
# ===========================================
echo ""
echo "🧹 Cleaning old backups..."
find "${BASE_DIR}/shared/backups" -name "full_backup_*.tar.gz" -mtime +30 -delete 2>/dev/null || true
find "${BASE_DIR}/shared/backups" -type d -empty -mtime +30 -delete 2>/dev/null || true
echo "✅ Cleanup complete"

# ===========================================
# Summary
# ===========================================
echo ""
echo "=========================================="
echo "✅ Backup Complete!"
echo "=========================================="
echo "📁 Location: ${BACKUP_DIR}"
echo "📦 Combined: ${COMBINED_ARCHIVE}"

# Calculate total size
if [ -f "$COMBINED_ARCHIVE" ]; then
    SIZE=$(du -sh "$COMBINED_ARCHIVE" | cut -f1)
    echo "📊 Size: ${SIZE}"
fi

echo "=========================================="
