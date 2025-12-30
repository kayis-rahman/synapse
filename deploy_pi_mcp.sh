#!/bin/bash
# Quick Start Script - MCP Server on Pi 5
# This script helps deploy RAG MCP Server quickly

set -e

echo "========================================="
echo "RAG MCP Server - Quick Start"
echo "========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Check prerequisites
echo "Step 1: Checking prerequisites..."

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}✗ Docker not installed${NC}"
    echo "Please install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi
echo -e "${GREEN}✓${NC} Docker installed"

# Check Docker Compose
if ! command -v docker compose &> /dev/null; then
    echo -e "${RED}✗ Docker Compose not installed${NC}"
    echo "Please install Docker Compose"
    exit 1
fi
echo -e "${GREEN}✓${NC} Docker Compose installed"

# Check if models exist
if [ ! -f ~/models/bge-m3-q8_0.gguf ]; then
    echo -e "${YELLOW}⚠${NC} BGE-M3 model not found at ~/models/bge-m3-q8_0.gguf"
    echo "Please download the model to ~/models/"
    echo "From: https://huggingface.co/BAAI/bge-m3"
    read -p "Continue anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    MODEL_SIZE=$(du -h ~/models/bge-m3-q8_0.gguf | cut -f1)
    echo -e "${GREEN}✓${NC} BGE-M3 model found ($MODEL_SIZE)"
fi

echo ""

# Step 2: Build Docker image
echo "Step 2: Building Docker image..."
echo "This may take 3-5 minutes..."
docker compose -f docker-compose.mcp.yml build --no-cache

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Docker image built successfully"
else
    echo -e "${RED}✗${NC} Docker image build failed"
    exit 1
fi

echo ""

# Step 3: Start MCP server
echo "Step 3: Starting MCP server..."
docker compose -f docker-compose.mcp.yml up -d

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} MCP server started successfully"
else
    echo -e "${RED}✗${NC} MCP server failed to start"
    docker compose -f docker-compose.mcp.yml logs
    exit 1
fi

echo ""

# Step 4: Verify deployment
echo "Step 4: Verifying deployment..."
sleep 3

# Check if container is running
CONTAINER_STATUS=$(docker ps --filter "name=rag-mcp" --format "{{.Status}}")
if [[ "$CONTAINER_STATUS" == "Up" ]]; then
    echo -e "${GREEN}✓${NC} Container is running"
else
    echo -e "${RED}✗${NC} Container is not running: $CONTAINER_STATUS"
    exit 1
fi

# Check logs for tool availability
echo ""
echo "Checking MCP server logs..."
sleep 2
docker compose -f docker-compose.mcp.yml logs --tail 20 | grep "Available tools"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} MCP tools are available"
else
    echo -e "${YELLOW}⚠${NC} Tools not yet initialized (waiting for startup)"
fi

echo ""

# Step 5: Get Pi IP address
echo "Step 5: Getting Pi 5 IP address..."
PI_IP=$(hostname -I | awk '{print $1}')
echo -e "${GREEN}✓${NC} Pi 5 IP: $PI_IP"

echo ""

# Step 6: Instructions for Mac M1
echo "========================================="
echo "Instructions for Mac M1"
echo "========================================="
echo ""
echo "1. Generate SSH key on Mac M1:"
echo "   ssh-keygen -t ed25519 -f ~/.ssh/pi_rag_ed25519 -N \"\""
echo ""
echo "2. Copy public key to Pi 5:"
echo "   ssh-copy-id -i ~/.ssh/pi_rag_ed25519.pub dietpi@$PI_IP"
echo "   # Or paste manually to ~/.ssh/authorized_keys on Pi 5"
echo ""
echo "3. Configure SSH on Mac M1 (~/.ssh/config):"
echo ""
cat <<EOF
Host pi-rag
    HostName $PI_IP
    User dietpi
    IdentityFile ~/.ssh/pi_rag_ed25519
    ServerAliveInterval 60
    ServerAliveCountMax 3
EOF
echo ""
echo "4. Configure Claude Desktop:"
echo "   Edit: ~/Library/Application Support/Claude/claude_desktop_config.json"
echo ""
cat <<EOF
{
  "mcpServers": {
    "pi-rag-server": {
      "command": "ssh",
      "args": [
        "-i", "~/.ssh/pi_rag_ed25519",
        "pi-rag",
        "docker", "run", "-i", "--rm",
        "-e", "RAG_DATA_DIR=/app/data",
        "-v", "rag-mcp-data:/app/data",
        "-v", "rag-mcp-models:/app/models:ro",
        "rag-mcp:latest"
      ],
      "env": {}
    }
  }
}
EOF
echo ""
echo "5. Restart Claude Desktop to load new MCP server"
echo ""
echo "========================================="
echo "Deployment Complete!"
echo "========================================="
echo ""
echo "To check logs:"
echo "  docker compose -f docker-compose.mcp.yml logs -f"
echo ""
echo "To stop server:"
echo "  docker compose -f docker-compose.mcp.yml down"
echo ""
echo "To restart server:"
echo "  docker compose -f docker-compose.mcp.yml restart"
echo ""
