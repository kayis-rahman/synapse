#!/bin/bash
export SHELL=/bin/bash

################################################################################
# Pi-RAG Docker Deployment Script for Raspberry Pi 5
# 
# This script automates the deployment of pi-rag using Docker on Raspberry Pi 5
# with external LLM server integration.
#
# Prerequisites:
#   - Raspberry Pi 5 with Raspberry Pi OS 64-bit
#   - Docker installed on Pi
#   - Docker context configured on local machine
#   - SSH access to Pi
#
# Usage:
#   ./scripts/deploy.sh [pi-hostname-or-ip]
#
# Example:
#   ./scripts/deploy.sh pi@192.168.1.100
#   ./scripts/deploy.sh pi@raspberrypi.local
################################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PI_USER=${PI_USER:-dietpi}
PI_HOST=${PI_HOST:-piworm.local}
PROJECT_NAME="pi-rag"
COMPOSE_FILE="docker-compose.pi.yml"
DOCKER_CONTEXT="${DOCKER_CONTEXT:-pi}"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check if Docker is available
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed or not in PATH"
        exit 1
    fi
    
    # Check if Docker context exists
    if ! docker context ls | grep -q "${DOCKER_CONTEXT}"; then
        log_error "Docker context '${DOCKER_CONTEXT}' not found"
        log_info "Create it with: docker context create ${DOCKER_CONTEXT} --docker host=ssh://${PI_USER}@${PI_HOST}"
        exit 1
    fi
    
    # Check if compose file exists
    if [ ! -f "${COMPOSE_FILE}" ]; then
        log_error "Docker compose file '${COMPOSE_FILE}' not found"
        exit 1
    fi
    
    log_success "Prerequisites check passed"
}

create_directories() {
    log_info "Creating directory structure on Pi..."
    
    # Create directories on Pi
    ssh ${PI_USER}@${PI_HOST} "mkdir -p /home/${PI_USER}/${PROJECT_NAME}/{configs,data,models}" || {
        log_error "Failed to create directories on Pi"
        exit 1
    }
    
    # Copy configs (if they exist locally)
    if [ -d "configs" ]; then
        log_info "Copying configuration files..."
        scp -r configs ${PI_USER}@${PI_HOST}:/home/${PI_USER}/${PROJECT_NAME}/
    fi
    
    log_success "Directory structure created"
}

download_embedding_model() {
    log_info "Downloading embedding model (nomic-embed-text-v1.5 Q4_K_M)..."
    
    # Skip model download due to fish shell compatibility issues
    log_warning "Skipping model download due to fish shell compatibility issues"
    log_info "Please manually download the model on the Pi or ensure it's already present"
}

deploy_stack() {
    # Create .env file for Pi
    cat > /tmp/.env.pi << EOF
# Pi-RAG Environment Variables
MODEL_PATH=/home/${PI_USER}/${PROJECT_NAME}/models
DATA_PATH=/home/${PI_USER}/${PROJECT_NAME}/data
CONFIG_PATH=/home/${PI_USER}/${PROJECT_NAME}/configs
LOG_LEVEL=INFO
EOF

    # Copy .env file to Pi
    scp /tmp/.env.pi ${PI_USER}@${PI_HOST}:/home/${PI_USER}/${PROJECT_NAME}/.env
    
    # Build and start containers on Pi
    log_info "Building Docker image (this may take a while)..."
    docker compose -f ${COMPOSE_FILE} --context ${DOCKER_CONTEXT} build
    
    log_info "Starting containers..."
    docker compose -f ${COMPOSE_FILE} --context ${DOCKER_CONTEXT} up -d
    
    log_success "Stack deployed successfully!"
}

wait_for_startup() {
    log_info "Waiting for pi-rag to start..."
    
    # Wait for container to be healthy
    max_attempts=30
    attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        status=$(ssh ${PI_USER}@${PI_HOST} "docker inspect -f '{{.State.Health.Status}}' pi-rag 2>/dev/null || echo 'starting'")
        
        case $status in
            "healthy")
                log_success "Container is healthy!"
                return 0
                ;;
            "starting"|"unhealthy")
                echo -n "."
                sleep 5
                ;;
            *)
                log_error "Container status: $status"
                return 1
                ;;
        esac
        
        attempt=$((attempt + 1))
    done
    
    log_error "Timeout waiting for container to become healthy"
    return 1
}

test_deployment() {
    log_info "Testing deployment..."
    
    # Get Pi IP
    PI_IP=$(ssh ${PI_USER}@${PI_HOST} "hostname -I | awk '{print \$1}'")
    
    # Test health endpoint
    log_info "Testing health endpoint..."
    curl -f http://${PI_IP}:8001/health || {
        log_error "Health check failed"
        return 1
    }
    
    log_success "Deployment test passed!"
}

show_info() {
    PI_IP=$(ssh ${PI_USER}@${PI_HOST} "hostname -I | awk '{print \$1}'")
    
    echo ""
    log_success "Deployment Complete!"
    echo ""
    echo "┌─────────────────────────────────────────────────────────┐"
    echo "│                    Pi-RAG Deployment                    │"
    echo "├─────────────────────────────────────────────────────────┤"
    echo "│                                                         │"
    echo "│ API Endpoint:  http://${PI_IP}:8001                      │"
    echo "│                                                         │"
    echo "│ Health Check:  curl http://${PI_IP}:8001/health         │"
    echo "│ List Models:   curl http://${PI_IP}:8001/v1/models       │"
    echo "│ Stats:         curl http://${PI_IP}:8001/v1/stats        │"
    echo "│                                                         │"
    echo "│ Docker Commands:                                        │"
    echo "│   View logs:   docker logs -f pi-rag                   │"
    echo "│   Stop:        docker stop pi-rag                      │"
    echo "│   Start:       docker start pi-rag                     │"
    echo "│                                                         │"
    echo "├─────────────────────────────────────────────────────────┤"
    echo "│ Next Steps:                                             │"
    echo "│ 1. Ingest documents:                                    │"
    echo "│    docker exec pi-rag python -m rag.bulk_ingest /app/data │"
    echo "│                                                         │"
    echo "│ 2. Test RAG query:                                      │"
    echo "│    curl -X POST http://${PI_IP}:8001/v1/chat/completions \\\│"
    echo "│      -H 'Content-Type: application/json' \\\│"
    echo "│      -d '{\"messages\": [{\"role\":\"user\",\"content\":\"Hello\"}]}' │"
    echo "│                                                         │"
    echo "└─────────────────────────────────────────────────────────┘"
    echo ""
}

show_logs() {
    log_info "Viewing logs (Ctrl+C to exit)..."
    ssh ${PI_USER}@${PI_HOST} "docker logs -f pi-rag"
}

# Main execution
main() {
    log_info "Starting Pi-RAG deployment to ${PI_HOST}..."
    log_info "Docker context: ${DOCKER_CONTEXT}"
    echo ""
    
    # Run deployment steps
    check_prerequisites
    create_directories
    download_embedding_model
    deploy_stack
    wait_for_startup
    test_deployment
    show_info
    
    # Optionally show logs
    read -t 5 -p "View logs now? (y/n, auto-no in 5s): " view_logs
    if [ "$view_logs" = "y" ]; then
        show_logs
    fi
}

# Handle script arguments
if [ $# -gt 0 ]; then
    # Check if first argument is a valid command
    case "$1" in
        "deploy"|"logs"|"test"|"stop"|"restart"|"update"|"shell")
            COMMAND="$1"
            PI_HOST="${PI_HOST:-piworm.local}"
            ;;
        *)
            # First argument is the host
            PI_HOST="$1"
            COMMAND="deploy"
            ;;
    esac
else
    COMMAND="deploy"
    PI_HOST="${PI_HOST:-piworm.local}"
fi

case "$COMMAND" in
    "deploy")
        main
        ;;
    "logs")
        show_logs
        ;;
    "test")
        docker context use ${DOCKER_CONTEXT}
        test_deployment
        ;;
    "stop")
        docker context use ${DOCKER_CONTEXT}
        docker compose -f ${COMPOSE_FILE} down
        ;;
    "restart")
        docker context use ${DOCKER_CONTEXT}
        docker compose -f ${COMPOSE_FILE} restart pi-rag
        ;;
    "update")
        docker context use ${DOCKER_CONTEXT}
        docker compose -f ${COMPOSE_FILE} build --no-cache
        docker compose -f ${COMPOSE_FILE} up -d --no-deps pi-rag
        ;;
    "shell")
        docker context use ${DOCKER_CONTEXT}
        docker exec -it pi-rag /bin/bash
        ;;
    *)
        echo "Usage: $0 {deploy|logs|test|stop|restart|update|shell} [pi-host]"
        echo ""
        echo "Commands:"
        echo "  deploy  - Full deployment (default)"
        echo "  logs    - View container logs"
        echo "  test    - Test deployment"
        echo "  stop    - Stop containers"
        echo "  restart - Restart containers"
        echo "  update  - Update to latest version"
        echo "  shell   - Open shell in container"
        exit 1
        ;;
esac