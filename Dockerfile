# Multi-stage build for RAG MCP Server
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies including OpenMP library
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    sqlite3 \
    libgomp1 \
    g++ \
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

# Verify imports work
RUN python -c "from mcp.server import Server; from mcp.types import Tool; print('✅ MCP SDK OK')" && \
    python -c "from rag import MemoryStore, EpisodicStore, SemanticStore; print('✅ RAG imports OK')" && \
    python -m py_compile mcp_server/rag_server.py && echo "✅ Server syntax OK"

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    sqlite3 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

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

# Run MCP server
CMD ["python", "-m", "mcp_server.rag_server"]
