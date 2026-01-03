#!/bin/bash
# RAG MCP HTTP Server Startup Script - Config-Aware Version
# Shows which ingestion modes are available based on config

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="/tmp/mcp_server.pid"
LOG_FILE="/tmp/mcp_server.log"
HOST="0.0.0.0"
PORT=8002
SERVER_MODULE="mcp_server.http_wrapper"
CONFIG_FILE="/home/dietpi/pi-rag/configs/rag_config.json"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ============================================================================
# Configuration Check Functions
get_config_flag() {
    local flag="$1"
    local default_value="$2"
    local value

    if [ -f "$CONFIG_FILE" ]; then
        # Simple JSON extraction without full Python context
        value=$(python3 -c "import json; config = json.load(open('$CONFIG_FILE')); print(str(config.get('$flag', '$default_value')).lower())" 2>/dev/null)
    else
        value="$default_value"
    fi

    echo "$value"
}

display_ingestion_status() {
    local context_injection=$(get_config_flag "context_injection_enabled" "false")
    local remote_upload=$(get_config_flag "remote_file_upload_enabled" "true")

    echo ""
    echo "Ingestion Modes:"
    echo "─────────────────────────────────────────────────────────────────"

    echo ""
    echo -e "${RED}✗${NC} Content Mode: DISABLED"
    echo "  └─ Mode removed from configuration"

    echo ""
    echo -e "${RED}✗${NC} File Path Mode: DISABLED"
    echo "  └─ Mode removed from configuration"

    echo ""

    if [ "$context_injection" = "true" ]; then
        echo -e "${GREEN}✓${NC} Context Injection: ENABLED"
        echo "  └─ Orchestrator auto-injects context into prompts"
    else
        echo -e "${RED}✗${NC} Context Injection: DISABLED"
        echo "  └─ Orchestrator does NOT inject context"
    fi

    echo ""

    if [ "$remote_upload" = "true" ]; then
        echo -e "${GREEN}✓${NC} HTTP Upload Flow: ENABLED"
        echo "  └─ Endpoint: POST http://$HOST:$PORT/v1/upload"
        echo "  └─ Workflow: Upload → Get file_path → Ingest → Auto-delete"
    else
        echo -e "${RED}✗${NC} HTTP Upload Flow: DISABLED"
        echo "  └─ Endpoint: POST http://$HOST:$PORT/v1/upload"
        echo "  └─ To enable: Set remote_file_upload_enabled=true in config"
    fi

    echo "─────────────────────────────────────────────────────────"
}

# ============================================================================
# PID Management
# ============================================================================

get_server_pid() {
    # Try PID file first
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            echo "$PID"
            return 0
        fi
    fi

    # Fallback: find by process name using ps
    PID=$(ps aux | grep -E "python3 -m $SERVER_MODULE" | grep -v grep | awk '{print $2}' | head -1)
    if [ -n "$PID" ]; then
        echo "$PID"
        return 0
    fi

    return 1
}

is_server_running() {
    PID=$(get_server_pid)
    [ -n "$PID" ]
}

stop_server() {
    if ! is_server_running; then
        echo -e "${YELLOW}⚠ Server is not running${NC}"
        return 1
    fi
    
    PID=$(get_server_pid)
    echo -e "${BLUE}Stopping server (PID: $PID)...${NC}"
    
    kill "$PID" 2>/dev/null
    
    # Wait for graceful shutdown
    for i in {1..10}; do
        if ! ps -p "$PID" > /dev/null 2>&1; then
            echo -e "${GREEN}✓ Server stopped gracefully${NC}"
            rm -f "$PID_FILE"
            return 0
        fi
        sleep 1
    done
    
    echo -e "${RED}✗ Server did not stop gracefully${NC}"
    kill -9 "$PID" 2>/dev/null
    rm -f "$PID_FILE"
    return 1
}

# ============================================================================
# Server Start
# ============================================================================

start_server() {
    display_ingestion_status
    
    if is_server_running; then
        PID=$(get_server_pid)
        echo -e "${RED}✗ Server is already running (PID: $PID)${NC}"
        echo ""
        echo "Use --restart to restart server"
        return 1
    fi
    
    # Ensure directories exist
    mkdir -p "$(dirname "$LOG_FILE")"
    
    echo "=========================================="
    echo -e "${GREEN}Starting RAG MCP HTTP Server${NC}"
    echo "=========================================="
    echo ""
    
    echo "Configuration:"
    echo "  Script directory: $SCRIPT_DIR"
    echo "  Log file: $LOG_FILE"
    echo "  Config file: $CONFIG_FILE"
    echo "  Host: $HOST"
    echo "  Port: $PORT"
    echo "  Server module: $SERVER_MODULE"
    echo ""
    
    echo "Endpoints:"
    echo "  MCP Protocol: http://$HOST:$PORT/mcp"
    echo "  Health Check: http://$HOST:$PORT/health"
    echo "  HTTP Upload: http://$HOST:$PORT/v1/upload"
    echo ""
    
    echo "Available Tools (7 total):"
    echo "  1. list_projects"
    echo "  2. list_sources"
    echo " 3. get_context"
    echo "  4. search"
    echo "  5. ingest_file"
    echo "  6. add_fact"
    echo "  7. add_episode"
    echo ""
    echo "=========================================="
    
    # Start server in background with logging
    python3 -m "$SERVER_MODULE" >> "$LOG_FILE" 2>&1 &
    SERVER_PID=$!
    
    # Save PID
    echo "$SERVER_PID" > "$PID_FILE"
    
    # Wait for server to start
    echo "Starting server (PID: $SERVER_PID)..."
    
    # Check if server is responding
    for i in {1..15}; do
        if curl -s http://localhost:$PORT/health > /dev/null 2>&1; then
            echo -e "${GREEN}✓ Server started successfully${NC}"
            echo ""
            echo "Useful commands:"
            echo "  View logs: tail -f $LOG_FILE"
            echo "  Check health: curl http://$HOST:$PORT/health"
            echo "  Stop server: $0 --stop"
            echo ""
            return 0
        fi
        sleep 1
    done
    
    # Server is running but not responding yet
    echo -e "${YELLOW}⚠ Server is running but not yet responding${NC}"
    echo "Check logs: tail -20 $LOG_FILE"
    rm -f "$PID_FILE"
    return 1
}

# ============================================================================
# Status Display
# ============================================================================

show_status() {
    display_ingestion_status
    
    echo ""
    echo "=========================================="
    echo -e "${BLUE}RAG MCP HTTP Server Status${NC}"
    echo "=========================================="
    echo ""
    
    # Check if running
    if is_server_running; then
        PID=$(get_server_pid)
        echo -e "${GREEN}✓ Server Status: RUNNING${NC}"
        echo "  Process ID: $PID"
        echo "  Port: $PORT"
        echo ""
        echo "Ingestion Modes:"
        display_ingestion_status
        echo ""
        echo "Endpoints:"
        echo "  MCP: http://$HOST:$PORT/mcp"
        echo "  HTTP Upload: http://$HOST:$PORT/v1/upload"
        echo "  Health: http://$HOST:$PORT/health"
        echo ""
    else
        echo -e "${RED}✗ Server Status: NOT RUNNING${NC}"
        echo ""
        echo "Ingestion Modes:"
        display_ingestion_status
        echo ""
        echo "Start server: $0 (default)"
        echo "Check status: $0 --status"
        echo ""
        echo "Configuration file: $CONFIG_FILE"
    fi
    
    echo "=========================================="
}

# ============================================================================
# Help
# ============================================================================

show_help() {
    echo "RAG MCP HTTP Server - Control Script"
    echo ""
    echo "USAGE: $0 [OPTION]"
    echo ""
    echo "OPTIONS:"
    echo "  (no args)   Start server (error if already running)"
    echo "  --restart   Restart server (stop existing, start new)"
    echo "  --stop      Stop running server"
    echo "  --status     Show server status and configuration"
    echo "  --help       Show this help message"
    echo ""
    echo "EXAMPLES:"
    echo "  $0              # Start server"
    echo "  $0 --restart    # Restart server"
    echo "  $0 --status     # Show status"
    echo "  $0 --help        # Show this help"
    echo ""
    echo "FILES:"
    echo "  Config: $CONFIG_FILE"
    echo "  Script: $0"
    echo "  Logs: $LOG_FILE"
    echo ""
    echo "To enable modes, edit config and restart:"
    echo "  vim $CONFIG_FILE"
}

# ============================================================================
# Main
# ============================================================================

case "${1:-}" in
    "")
        # Start server (default)
        start_server
        ;;
    
    --restart)
        stop_server
        sleep 1
        start_server
        ;;
    
    --stop)
        stop_server
        ;;
    
    --status)
        show_status
        ;;
    
    --help|-h)
        show_help
        ;;
    
    *)
        echo -e "${RED}✗ Unknown option: $1${NC}"
        show_help
        exit 1
        ;;
esac
