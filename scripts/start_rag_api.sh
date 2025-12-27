#!/bin/bash
set -e

echo "=========================================="
echo "Starting RAG API Server"
echo "=========================================="
echo ""

# Configuration
HOST="${RAG_HOST:-0.0.0.0}"
PORT="${RAG_PORT:-8001}"
CONFIG="${RAG_CONFIG:-./configs/rag_config.json}"

echo "Host: $HOST"
echo "Port: $PORT"
echo "Config: $CONFIG"
echo ""

# Change to project directory
cd "$(dirname "$0")/.."

# Export environment variables
export RAG_HOST="$HOST"
export RAG_PORT="$PORT"
export RAG_CONFIG="$CONFIG"

# Start the API server
echo "Starting uvicorn..."
python3 -m uvicorn api.main:app --host "$HOST" --port "$PORT" --reload
