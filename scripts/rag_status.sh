#!/bin/bash
# Complete RAG System Status Check

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Detect Data Directory
if [ -n "$RAG_DATA_DIR" ]; then
    DATA_DIR="$RAG_DATA_DIR"
elif [ -d "/opt/synapse/data" ]; then
    DATA_DIR="/opt/synapse/data"
else
    DATA_DIR="${PROJECT_ROOT}/data"
fi

echo "=============================================="
echo "  RAG System Status Check"
echo "=============================================="
echo "Project Root: $PROJECT_ROOT"
echo "Data Directory: $DATA_DIR"
echo ""

PASS=0
FAIL=0

# 1. Server Health
echo "1. MCP Server Status:"
if curl -s http://localhost:8002/health > /dev/null; then
    echo "   ✓ Server is running"
    ((PASS++))
    curl -s http://localhost:8002/health | python3 -m json.tool | grep -E '(status|tools_available)'
else
    echo "   ✗ Server is DOWN"
    ((FAIL++))
fi
echo ""

# 2. AGENTS.md Configuration
echo "2. AGENTS.md Configuration:"
AGENTS_FILE="${PROJECT_ROOT}/AGENTS.md"
if [ -f "$AGENTS_FILE" ]; then
    echo "   ✓ AGENTS.md exists"
    AGENT_LINES=$(wc -l < "$AGENTS_FILE")
    echo "   Size: $AGENT_LINES lines"
    if grep -q "RAG STRICT MANDATE" "$AGENTS_FILE"; then
        echo "   ✓ RAG strict mandate found"
        ((PASS++))
    else
        echo "   ✗ RAG mandate not found"
        ((FAIL++))
    fi
else
    echo "   ✗ AGENTS.md not found at $AGENTS_FILE"
    ((FAIL++))
fi
echo ""

# 3. Data Statistics
echo "3. Semantic Memory:"
CHUNKS_FILE="${DATA_DIR}/semantic_index/chunks.json"
if [ -f "$CHUNKS_FILE" ]; then
    CHUNKS=$(python3 -c "import json; print(len(json.load(open('$CHUNKS_FILE'))))" 2>/dev/null || echo "0")
    echo "   Chunks: $CHUNKS"
    if [ "$CHUNKS" -ge 4000 ]; then
        echo "   ✓ Sufficient chunks"
        ((PASS++))
    else
        echo "   ⚠ Low chunk count (Warning only)"
    fi
else
    echo "   ✗ No chunks file at $CHUNKS_FILE"
    ((FAIL++))
fi

DOCS_FILE="${DATA_DIR}/semantic_index/metadata/documents.json"
if [ -f "$DOCS_FILE" ]; then
    DOCS=$(python3 -c "import json; d=json.load(open('$DOCS_FILE')); print(len(d))" 2>/dev/null || echo "0")
    echo "   Documents: $DOCS"
    if [ "$DOCS" -ge 250 ]; then
        echo "   ✓ Sufficient documents"
        ((PASS++))
    else
        echo "   ⚠ Low document count (Warning only)"
    fi
else
    echo "   ✗ No documents metadata at $DOCS_FILE"
    ((FAIL++))
fi
echo ""

# 4. Symbolic Memory (Authoritative Facts)
echo "4. Symbolic Memory (Authoritative Facts):"
MEMORY_DB="${DATA_DIR}/memory.db"
if [ -f "$MEMORY_DB" ]; then
    FACTS=$(sqlite3 "$MEMORY_DB" "SELECT COUNT(*) FROM memory_facts;" 2>/dev/null || echo "0")
    echo "   Total facts: $FACTS"
    if [ "$FACTS" -ge 20 ]; then
        echo "   ✓ Sufficient authoritative facts"
        ((PASS++))
    else
        echo "   ⚠ Low fact count (need 20+)"
    fi

    echo "   Recent facts:"
    sqlite3 "$MEMORY_DB" "SELECT fact_key, category FROM memory_facts WHERE scope='global' ORDER BY created_at DESC LIMIT 10;" 2>/dev/null | while read line; do
        echo "     - $line"
    done
else
    echo "   ✗ Database not found at $MEMORY_DB"
    ((FAIL++))
fi
echo ""

# 5. Episodic Memory (Advisory Lessons)
echo "5. Episodic Memory (Advisory Lessons):"
EPISODIC_DB="${DATA_DIR}/episodic.db"
PROJECT_ID="SYNAPSE"

if [ -f "$EPISODIC_DB" ]; then
    EPISODES=$(sqlite3 "$EPISODIC_DB" "SELECT COUNT(*) FROM episodic_memory WHERE project_id='$PROJECT_ID';" 2>/dev/null || echo "0")
    echo "   Total episodes: $EPISODES"
    if [ "$EPISODES" -ge 1 ]; then
        echo "   ✓ Sufficient lessons"
        ((PASS++))
    else
        echo "   ⚠ Low episode count"
    fi

    echo "   Recent episodes:"
    sqlite3 "$EPISODIC_DB" "SELECT lesson, outcome FROM episodic_memory WHERE project_id='$PROJECT_ID' ORDER BY created_at DESC LIMIT 5;" 2>/dev/null | while read line; do
        echo "     - $line"
    done
else
    echo "   ✗ Database not found at $EPISODIC_DB"
    ((FAIL++))
fi
echo ""

# 6. Project Registration
echo "6. Registered Projects:"
REGISTRY_DB="${DATA_DIR}/registry.db"
if [ -f "$REGISTRY_DB" ]; then
    sqlite3 "$REGISTRY_DB" "SELECT project_id, name FROM projects;" 2>/dev/null | while read line; do
        echo "   - $line"
    done
    PROJECT_EXISTS=$(sqlite3 "$REGISTRY_DB" "SELECT COUNT(*) FROM projects WHERE project_id='$PROJECT_ID';" 2>/dev/null || echo "0")
    if [ "$PROJECT_EXISTS" -gt 0 ]; then
        echo "   ✓ Project '$PROJECT_ID' is registered"
        ((PASS++))
    else
        echo "   ⚠ Project '$PROJECT_ID' not registered in registry DB"
        # Not failing hard as registry might be optional or auto-created
    fi
else
    echo "   ⚠ Registry DB not found (Optional)"
fi
echo ""

# 7. MCP Configuration Check (Optional)
echo "7. MCP Configuration Check:"
echo "   (Skipping client specific checks)"
echo ""

# 8. Data Directory Integrity
echo "8. Data Directory Integrity:"
REQUIRED_FILES=(
    "$MEMORY_DB"
    "$EPISODIC_DB"
    "$CHUNKS_FILE"
    "$DOCS_FILE"
)

ALL_PRESENT=true
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "   ✗ Missing: $file"
        ALL_PRESENT=false
    fi
done

if [ "$ALL_PRESENT" = true ]; then
    echo "   ✓ All required data files present"
    ((PASS++))
else
    echo "   ✗ Some files missing"
    ((FAIL++))
fi

# 9. Backup Verification
echo "9. Backup Verification:"
if [ -d "${DATA_DIR}" ]; then
    BACKUP_DIRS=$(find "$DATA_DIR" -maxdepth 1 -type d -name "backup_before_cleanup_*" | wc -l)
    if [ "$BACKUP_DIRS" -gt 0 ]; then
        echo "   ✓ $BACKUP_DIRS backup(s) found"
        ((PASS++))
    else
        echo "   ⚠ No backup directory found"
    fi
else
    echo "   ⚠ Data directory does not exist to check backups"
fi
echo ""

# Summary
echo "=============================================="
echo "  Test Results"
echo "=============================================="
echo "  Passed: $PASS/8"  # Adjusted total
echo "  Failed: $FAIL/8"
echo ""

if [ $FAIL -eq 0 ]; then
    echo "  ✓ ALL TESTS PASSED - System Ready!"
    echo ""
    echo "  Try query: 'What is SYNAPSE?'"
    echo ""
    exit 0
else
    echo "  ✗ Some tests failed - Review above"
    echo ""
    echo "  FAILED TESTS:"
    if [ $FAIL -gt 0 ]; then
        echo "  Fix issues and re-run: bash $0"
    fi
    echo ""
    exit 1
fi