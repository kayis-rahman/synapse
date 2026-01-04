#!/bin/bash
# Complete RAG System Status Check

echo "=============================================="
echo "  RAG System Status Check"
echo "=============================================="
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
if [ -f /home/dietpi/synapse/AGENTS.md ]; then
    echo "   ✓ AGENTS.md exists"
    AGENT_LINES=$(wc -l < /home/dietpi/synapse/AGENTS.md)
    echo "   Size: $AGENT_LINES lines"
    if grep -q "RAG STRICT MANDATE" /home/dietpi/synapse/AGENTS.md; then
        echo "   ✓ RAG strict mandate found"
        ((PASS++))
    else
        echo "   ✗ RAG mandate not found"
        ((FAIL++))
    fi
else
    echo "   ✗ AGENTS.md not found"
    ((FAIL++))
fi
echo ""

# 3. Data Statistics
echo "3. Semantic Memory:"
if [ -f /opt/synapse/data/semantic_index/chunks.json ]; then
    CHUNKS=$(python3 -c "import json; print(len(json.load(open('/opt/synapse/data/semantic_index/chunks.json'))))" 2>/dev/null || echo "0")
    echo "   Chunks: $CHUNKS"
    if [ "$CHUNKS" -ge 4000 ]; then
        echo "   ✓ Sufficient chunks"
        ((PASS++))
    else
        echo "   ⚠ Low chunk count"
    fi
else
    echo "   ✗ No chunks file"
    ((FAIL++))
fi

if [ -f /opt/synapse/data/semantic_index/metadata/documents.json ]; then
    DOCS=$(python3 -c "import json; d=json.load(open('/opt/synapse/data/semantic_index/metadata/documents.json')); print(len(d))" 2>/dev/null || echo "0")
    echo "   Documents: $DOCS"
    if [ "$DOCS" -ge 250 ]; then
        echo "   ✓ Sufficient documents"
        ((PASS++))
    else
        echo "   ⚠ Low document count"
    fi
else
    echo "   ✗ No documents metadata"
    ((FAIL++))
fi
echo ""

# 4. Symbolic Memory (Authoritative Facts)
echo "4. Symbolic Memory (Authoritative Facts):"
FACTS=$(sqlite3 /opt/synapse/data/memory.db "SELECT COUNT(*) FROM memory_facts;" 2>/dev/null || echo "0")
echo "   Total facts: $FACTS"
if [ "$FACTS" -ge 20 ]; then
    echo "   ✓ Sufficient authoritative facts"
    ((PASS++))
else
    echo "   ⚠ Low fact count (need 20+)"
fi

echo "   Recent facts:"
sqlite3 /opt/synapse/data/memory.db "SELECT fact_key, category FROM memory_facts WHERE scope='global' ORDER BY created_at DESC LIMIT 10;" 2>/dev/null | while read line; do
    echo "     - $line"
done
echo ""

# 5. Episodic Memory (Advisory Lessons)
echo "5. Episodic Memory (Advisory Lessons):"
EPISODES=$(sqlite3 /opt/synapse/data/episodic.db "SELECT COUNT(*) FROM episodic_memory WHERE project_id="synapse"';" 2>/dev/null || echo "0")
echo "   Total episodes: $EPISODES"
if [ "$EPISODES" -ge 4 ]; then
    echo "   ✓ Sufficient lessons"
    ((PASS++))
else
    echo "   ⚠ Low episode count (need 4+)"
fi

echo "   Recent episodes:"
sqlite3 /opt/synapse/data/episodic.db "SELECT lesson, outcome FROM episodic_memory WHERE project_id="synapse"' ORDER BY created_at DESC LIMIT 5;" 2>/dev/null | while read line; do
    echo "     - $line"
done
echo ""

# 6. Project Registration
echo "6. Registered Projects:"
sqlite3 /opt/synapse/data/registry.db "SELECT project_id, name FROM projects;" 2>/dev/null | while read line; do
    echo "   - $line"
done
PROJECT_EXISTS=$(sqlite3 /opt/synapse/data/registry.db "SELECT COUNT(*) FROM projects WHERE project_id="synapse"';" 2>/dev/null || echo "0")
if [ "$PROJECT_EXISTS" -gt 0 ]; then
    echo "   ✓ Project 'pi-rag' is registered"
    ((PASS++))
else
    echo "   ✗ Project 'pi-rag' not registered"
    ((FAIL++))
fi
echo ""

# 7. opencode MCP Configuration
echo "7. opencode MCP Configuration:"
if [ -f ~/.opencode/opencode.jsonc ]; then
    if grep -q '"rag"' ~/.opencode/opencode.jsonc 2>/dev/null; then
        echo "   ✓ RAG MCP server configured in opencode"
        ((PASS++))
        if grep -q '"enabled": true' ~/.opencode/opencode.jsonc; then
            echo "   ✓ MCP server is enabled"
            ((PASS++))
        else
            echo "   ✗ MCP server not enabled"
            ((FAIL++))
        fi
    else
        echo "   ✗ RAG MCP server not configured"
        ((FAIL++))
    fi
else
    echo "   ⚠ opencode config not found at ~/.opencode/opencode.jsonc"
    echo "   Checking alternative location..."
    if [ -f ~/.config/opencode/opencode.jsonc ]; then
        if grep -q '"rag"' ~/.config/opencode/opencode.jsonc 2>/dev/null; then
            echo "   ✓ RAG MCP server configured"
            ((PASS++))
        fi
    fi
fi
echo ""

# 8. Data Directory Integrity
echo "8. Data Directory Integrity:"
REQUIRED_FILES=(
    "/opt/synapse/data/memory.db"
    "/opt/synapse/data/episodic.db"
    "/opt/synapse/data/semantic_index/chunks.json"
    "/opt/synapse/data/semantic_index/metadata/documents.json"
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
if [ -d /opt/synapse/data/backup_before_cleanup_* ]; then
    BACKUP_DIRS=$(find /opt/synapse/data -type d -name "backup_before_cleanup_*" | wc -l)
    echo "   ✓ $BACKUP_DIRS backup(s) found"
    ((PASS++))
else
    echo "   ⚠ No backup directory found"
fi
echo ""

# Summary
echo "=============================================="
echo "  Test Results"
echo "=============================================="
echo "  Passed: $PASS/9"
echo "  Failed: $FAIL/9"
echo ""

if [ $FAIL -eq 0 ]; then
    echo "  ✓ ALL TESTS PASSED - System Ready for opencode!"
    echo ""
    echo "  NEXT STEPS:"
    echo "  1. Restart opencode if needed"
    echo "  2. Test RAG tools in opencode interface"
    echo "  3. Try query: 'What is pi-rag project?'"
    echo ""
    exit 0
else
    echo "  ✗ Some tests failed - Review above"
    echo ""
    echo "  FAILED TESTS:"
    if [ $FAIL -gt 0 ]; then
        echo "  Fix issues and re-run: bash /home/dietpi/synapse/scripts/rag_status.sh"
    fi
    echo ""
    exit 1
fi
