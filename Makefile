.PHONY: help install dev test lint clean docker-build docker-run

help:
	@echo "SYNAPSE Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  make install   - Install package"
	@echo "  make dev        - Install with dev dependencies"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Run linting (black, mypy)"
	@echo "  make clean      - Clean build artifacts"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run  - Run Docker container"

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

test:
	pytest tests/ -v

lint:
	black mcp_server/ rag/ scripts/
	mypy mcp_server/ rag/

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache/ .mypy_cache/
	find . -type d -name "__pycache__" -exec rm -rf {} +

docker-build:
	docker build -t synapse:latest .

docker-run:
	docker compose -f docker-compose.mcp.yml up -d
