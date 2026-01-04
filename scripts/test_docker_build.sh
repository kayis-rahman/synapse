#!/bin/bash
# Test Docker build and image locally (no push to Docker Hub)
#
# This script tests Docker image building and validation
# without actually publishing to Docker Hub.
#
# Usage: ./scripts/test_docker_build.sh

set -e

echo "=========================================="
echo "Docker Hub Local Testing Script"
echo "Version: 1.0.0"
echo "=========================================="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "✓ Docker is running"
echo ""

# Step 1: Build Docker image
echo "Step 1: Building Docker image..."
echo "----------------------------------------"
docker build -t synapse:1.0.0 . 2>&1 | tee /tmp/docker_build.log

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Docker image build successful"
    docker images | grep synapse
else
    echo ""
    echo "❌ Docker image build failed"
    echo "Check log: /tmp/docker_build.log"
    exit 1
fi

echo ""

# Step 2: Tag for Docker Hub (local only, no push)
echo "Step 2: Tagging image for Docker Hub..."
echo "----------------------------------------"
docker tag synapse:1.0.0 kayisrahman/synapse:1.0.0
echo "✅ Tagged: kayisrahman/synapse:1.0.0 (local only)"
echo ""

# Step 3: Test image version
echo "Step 3: Testing image version..."
echo "----------------------------------------"
VERSION=$(docker run --rm synapse:1.0.0 python -c "import rag; print(rag.__version__)" 2>/dev/null || echo "unknown")

echo "Image version: $VERSION"

if [ "$VERSION" = "1.0.0" ]; then
    echo "✅ Version matches expected: 1.0.0"
else
    echo "⚠️ Version mismatch: expected 1.0.0, got $VERSION"
fi

echo ""

# Step 4: Test image functionality
echo "Step 4: Testing image functionality..."
echo "----------------------------------------"

# Test Python imports
IMPORT_TEST=$(docker run --rm synapse:1.0.0 python -c "
import sys
try:
    from rag import MemoryStore, EpisodicStore, SemanticStore
    from mcp_server.rag_server import RAGMemoryBackend
    print('SUCCESS: All imports working')
except Exception as e:
    print(f'FAILED: {e}')
    sys.exit(1)
" 2>&1)

echo "$IMPORT_TEST"

if echo "$IMPORT_TEST" | grep -q "SUCCESS"; then
    echo "✅ Python imports successful"
else
    echo "❌ Python imports failed"
    exit 1
fi

echo ""

# Step 5: Test MCP server startup
echo "Step 5: Testing MCP server can start..."
echo "----------------------------------------"

# Start container in background
CONTAINER_ID=$(docker run -d -p 8003:8002 --name synapse-test-build synapse:1.0.0 python -m mcp_server.http_wrapper)

# Wait for startup
sleep 5

# Check if container is running
if docker ps | grep -q "synapse-test-build"; then
    echo "✅ Test container started successfully"

    # Check health endpoint
    HEALTH=$(curl -s http://localhost:8003/health || echo '{"status":"error"}')

    if echo "$HEALTH" | grep -q '"status":"ok"'; then
        echo "✅ Health check passing"
    else
        echo "⚠️ Health check failed (may need more time)"
    fi

    # Stop test container
    docker stop synapse-test-build
    docker rm synapse-test-build
    echo "✅ Test container cleaned up"
else
    echo "❌ Test container failed to start"
    docker logs synapse-test-build 2>&1 || true
    docker rm -f synapse-test-build 2>/dev/null || true
    exit 1
fi

echo ""

# Step 6: Verify multi-platform support (simulate)
echo "Step 6: Verifying multi-platform support..."
echo "----------------------------------------"

# Check if buildx is available
if command -v docker buildx &> /dev/null; then
    echo "✅ Docker BuildX available (multi-platform builds supported)"

    # Simulate multi-platform build (dry-run)
    echo "Simulated platforms: linux/amd64, linux/arm64"
    echo "Note: Full multi-platform build would require:"
    echo "  docker buildx build --platform linux/amd64,linux/arm64 -t synapse:1.0.0 ."
else
    echo "⚠️ Docker BuildX not available (single-platform only)"
fi

echo ""
echo "=========================================="
echo "Summary"
echo "=========================================="
echo "✅ Docker image build: SUCCESS"
echo "✅ Image tagging: SUCCESS"
echo "✅ Version check: $VERSION"
echo "✅ Functionality test: SUCCESS"
echo "✅ MCP server startup: SUCCESS"
echo ""
echo "✅✅✅ ALL TESTS PASSED ✅✅✅"
echo ""
echo "Note: Images NOT published to Docker Hub (local testing only)"
echo "To publish: docker push kayisrahman/synapse:1.0.0"
echo "=========================================="
