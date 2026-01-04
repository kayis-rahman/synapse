# syntax=docker/dockerfile:1.4
# check=experimental=true
# ================================================================================
# SYNAPSE v1.0.0 - Your Data Meets Intelligence
# ================================================================================
# Multi-stage build for SYNAPSE MCP Server
#
# Docker Hub: https://hub.docker.com/r/kayisrahman/synapse
# Repository: https://github.com/kayis-rahman/synapse
# Build Optimization: BuildKit inline cache enabled
# ================================================================================

FROM python:3.11-slim as builder

# Docker Hub Metadata
LABEL maintainer="kaisbk1@gmail.com"
LABEL version="1.0.0"
LABEL description="SYNAPSE - Your Data Meets Intelligence"
LABEL repository="https://github.com/kayis-rahman/synapse"
LABEL org.opencontainers.image.source="https://github.com/kayis-rahman/synapse"
LABEL org.opencontainers.image.title="SYNAPSE"
LABEL org.opencontainers.image.description="Your Data Meets Intelligence - A local-first RAG system with semantic, episodic and symbolic memory"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.vendor="Kayis Rahman"

WORKDIR /app

# Install system dependencies including OpenMP library
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    sqlite3 \
    libgomp1 \
    git \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install llama-cpp-python with CPU support (no compilation needed)
RUN pip install --no-cache-dir \
    llama-cpp-python \
    --index-url https://abetlen.github.io/llama-cpp-python/whl/cpu

# Install MCP SDK
RUN pip install --no-cache-dir --break-system-packages mcp-server

# Copy application code
COPY . .

# Cleanup build artifacts
RUN rm -rf /tmp/* /var/tmp/*

# Verify imports work
RUN python -c "from mcp.server import Server; from mcp.types import Tool; print('✅ MCP SDK OK')" && \
    python -c "from rag import MemoryStore, EpisodicStore, SemanticStore; print('✅ RAG imports OK')" && \
    python -m py_compile mcp_server/rag_server.py && echo "✅ Server syntax OK"

# Final stage
FROM python:3.11-slim

# Docker Hub Metadata (inherit from builder)
LABEL maintainer="kaisbk1@gmail.com"
LABEL version="1.0.0"
LABEL description="SYNAPSE - Your Data Meets Intelligence"

WORKDIR /app

# Install runtime dependencies only
# CRITICAL: libgomp1 is required by llama-cpp-python (runtime dependency)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy from builder
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=builder /app /app

# Create data directories
RUN mkdir -p /app/data /app/data/semantic_index /app/data/episodic

# Set environment variables
ENV PYTHONPATH=/app
ENV LD_LIBRARY_PATH=/usr/local/lib/python3.11/site-packages/llama_cpp/lib:/usr/local/lib
ENV RAG_DATA_DIR=/app/data
ENV LOG_LEVEL=INFO

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from rag import MemoryStore; store = MemoryStore(); print('healthy')" || exit 1

# Run MCP HTTP server (for HTTP transport support)
CMD ["python", "-m", "mcp_server.http_wrapper"]
