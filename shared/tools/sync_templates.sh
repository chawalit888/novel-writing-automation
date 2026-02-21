#!/bin/bash
# ===========================================
# Sync Templates Script
# ซิงค์ templates ระหว่าง 2 ระบบ
# ===========================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"

SHARED_TEMPLATES="${BASE_DIR}/shared/templates"
CLAUDE_TEMPLATES="${BASE_DIR}/claude-code-novels/templates"
N8N_TEMPLATES="${BASE_DIR}/n8n-novels/templates"

echo "🔄 Syncing templates..."
echo "   Base: ${BASE_DIR}"
echo ""

# Ensure shared directory exists
mkdir -p "$SHARED_TEMPLATES"

# ===========================================
# Sync Claude Code → Shared
# ===========================================
echo "📤 Syncing Claude Code templates to Shared..."
if [ -d "$CLAUDE_TEMPLATES" ]; then
    rsync -av --update "$CLAUDE_TEMPLATES/" "$SHARED_TEMPLATES/" 2>/dev/null || \
        cp -r "$CLAUDE_TEMPLATES/"* "$SHARED_TEMPLATES/" 2>/dev/null || true
    echo "✅ Claude Code → Shared complete"
else
    echo "⚠️  Claude Code templates not found"
fi

# ===========================================
# Sync Shared → n8n
# ===========================================
echo ""
echo "📥 Syncing Shared templates to n8n..."
if [ -d "$SHARED_TEMPLATES" ]; then
    mkdir -p "$N8N_TEMPLATES"
    rsync -av --update "$SHARED_TEMPLATES/" "$N8N_TEMPLATES/" 2>/dev/null || \
        cp -r "$SHARED_TEMPLATES/"* "$N8N_TEMPLATES/" 2>/dev/null || true
    echo "✅ Shared → n8n complete"
else
    echo "⚠️  Shared templates not found"
fi

# ===========================================
# Sync Prompts
# ===========================================
echo ""
echo "📤 Syncing prompts..."

SHARED_PROMPTS="${BASE_DIR}/shared/prompts"
N8N_PROMPTS="${BASE_DIR}/n8n-novels/prompts"

mkdir -p "$SHARED_PROMPTS"

# Copy any new prompts from n8n to shared
if [ -d "$N8N_PROMPTS" ]; then
    rsync -av --update "$N8N_PROMPTS/" "$SHARED_PROMPTS/" 2>/dev/null || \
        cp -r "$N8N_PROMPTS/"* "$SHARED_PROMPTS/" 2>/dev/null || true
fi

echo "✅ Prompts synced"

# ===========================================
# Summary
# ===========================================
echo ""
echo "=========================================="
echo "✅ Template sync complete!"
echo "=========================================="
echo ""
echo "Directories synced:"
echo "  📁 Shared:      ${SHARED_TEMPLATES}"
echo "  📁 Claude Code: ${CLAUDE_TEMPLATES}"
echo "  📁 n8n:         ${N8N_TEMPLATES}"
echo ""

# Count files
SHARED_COUNT=$(find "$SHARED_TEMPLATES" -type f 2>/dev/null | wc -l | tr -d ' ')
echo "📊 Total template files in shared: ${SHARED_COUNT}"
echo "=========================================="
