#!/bin/bash
# RAG MCP Server Startup Script
# This script handles the graceful fallback for semantic memory

cd /home/dietpi/pi-rag

# Set environment variables
export RAG_DATA_DIR="/home/dietpi/pi-rag/data"
export LOG_LEVEL="INFO"

# Start RAG MCP server
echo "Starting RAG MCP Server..."
echo "Data directory: $RAG_DATA_DIR"
echo "Log level: $LOG_LEVEL"

python3 -m mcp_server.rag_server
