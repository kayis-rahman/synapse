#!/bin/bash
# Phase 3 Production Deployment Script
# Focus: Episodic Memory + MCP Server (100% tested components)

set -e  # Exit on error

cd /home/dietpi/pi-rag

# Color output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Phase 3 Production Deployment${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Step 1: Environment Setup
echo -e "${BLUE}Step 1: Environment Setup${NC}"
export RAG_DATA_DIR="/home/dietpi/pi-rag/data"
export LOG_LEVEL="INFO"
export RAG_PHASE_MODE="phase3"
mkdir -p "$RAG_DATA_DIR"
echo -e "${GREEN}✓ Data directory: $RAG_DATA_DIR${NC}"
echo ""

# Step 2: Verify Dependencies
echo -e "${BLUE}Step 2: Verify Dependencies${NC}"
python3 -c "from mcp.server import Server; from mcp.types import Tool" 2>/dev/null && echo -e "${GREEN}✓ MCP SDK installed${NC}" || { echo -e "${RED}✗ MCP SDK not found${NC}"; exit 1; }
python3 -c "from rag import EpisodicStore, Episode, get_episodic_store" 2>/dev/null && echo -e "${GREEN}✓ Phase 3 (Episodic) imports OK${NC}" || { echo -e "${RED}✗ Phase 3 imports failed${NC}"; exit 1; }
echo ""

# Step 3: Run Phase 3 Tests
echo -e "${BLUE}Step 3: Run Phase 3 Tests${NC}"
python3 -m pytest tests/test_episodic_memory.py -q 2>&1 | tail -5
if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo -e "${GREEN}✓ Phase 3 tests PASSED${NC}"
else
    echo -e "${RED}✗ Phase 3 tests FAILED${NC}"
    echo "This is critical - Phase 3 should pass 100%"
    exit 1
fi
echo ""

# Step 4: Run MCP Server Tests
echo -e "${BLUE}Step 4: Run MCP Server Tests${NC}"
python3 test_mcp_server_comprehensive.py 2>&1 | tail -3
if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo -e "${GREEN}✓ MCP Server tests PASSED${NC}"
else
    echo -e "${RED}✗ MCP Server tests FAILED${NC}"
    exit 1
fi
echo ""

# Step 5: Verify Episodic Database
echo -e "${BLUE}Step 5: Verify Episodic Database${NC}"
if [ -f "$RAG_DATA_DIR/episodic.db" ]; then
    EPISODE_COUNT=$(python3 -c "
from rag import get_episodic_store
store = get_episodic_store('$RAG_DATA_DIR/episodic.db')
print(len(store.list_all()))
" 2>/dev/null || echo "0")
    echo -e "${GREEN}✓ Episodic DB exists with $EPISODE_COUNT episodes${NC}"
else
    echo -e "${BLUE}ⓘ Episodic DB will be created on first episode${NC}"
fi
echo ""

# Step 6: Start MCP Server
echo -e "${BLUE}Step 6: Start MCP Server${NC}"
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Starting Phase 3 MCP Server${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Configuration:"
echo "  Mode: Phase 3 (Episodic Memory + MCP Server)"
echo "  Data Dir: $RAG_DATA_DIR"
echo "  Log Level: $LOG_LEVEL"
echo ""
echo "Available Tools (Phase 3):"
echo "  - rag.list_projects"
echo "  - rag.add_episode"
echo "  - rag.get_context"
echo "  - rag.search"
echo "  - rag.list_sources"
echo ""
echo "Press Ctrl+C to stop server"
echo ""
echo "========================================"
echo ""

# Start server
python3 -m mcp_server.rag_server
