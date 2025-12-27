# Ingest documents
ingest_docs() {
    log_info "Ingesting documents from $1..."
    docker exec pi-rag python -m rag.bulk_ingest "$1" "$@"
}

# Download model
download_model() {
    log_info "Downloading model to Pi..."
    ssh ${PI_USER}@${PI_HOST} "cd /home/${PI_USER}/pi-rag-models && wget -q --show-progress $1"
}

# Cleanup Docker resources
cleanup() {
    log_info "Cleaning up Docker resources..."
    docker context use ${DOCKER_CONTEXT}
    docker system prune -f
    docker volume rm $(docker volume ls -q -f dangling=true) 2>/dev/null || true
}

# Show all info
info() {
    docker context use ${DOCKER_CONTEXT}
    echo "=== SERVICE STATUS ==="
    docker compose -f ${COMPOSE_FILE} ps
    echo ""
    echo "=== CONTAINER STATUS ==="
    docker stats --no-stream pi-rag
    echo ""
    echo "=== LOGS (last 20 lines) ==="
    docker logs --tail 20 pi-rag
}

# Interactive selection
interactive() {
    while true; do
        echo ""
        echo "=========================================="
        echo "   Pi-RAG Management Menu"
        echo "=========================================="
        echo "1. Deploy/update pi-rag"
        echo "2. View logs"
        echo "3. Test API"
        echo "4. Ingest documents"
        echo "5. Open shell"
        echo "6. Restart service"
        echo "7. Stop service"
        echo "8. Cleanup Docker"
        echo "9. Show info"
        echo "10. Download model"
        echo "0. Exit"
        echo "=========================================="
        read -p "Select option: " option
        
        case $option in
            1) main ;;
            2) show_logs ;;
            3) test_deployment ;;
            4) 
                read -p "Enter document path on Pi: " doc_path
                ingest_docs "$doc_path"
                ;;
            5) docker exec -it pi-rag /bin/bash ;;
            6) docker compose -f ${COMPOSE_FILE} restart pi-rag ;;
            7) docker compose -f ${COMPOSE_FILE} down ;;
            8) cleanup ;;
            9) info ;;
            10)
                read -p "Enter model URL: " model_url
                download_model "$model_url"
                ;;
            0) exit 0 ;;
            *) echo "Invalid option" ;;
        esac
        
        read -p "Press Enter to continue..."
    done
}

# Show usage
usage() {
    echo "Pi-RAG Docker Management Script"
    echo ""
    echo "Usage: $0 [command] [options]"
    echo ""
    echo "Commands:"
    echo "  deploy [pi-host]     - Deploy pi-rag to Pi (default)"
    echo "  logs                 - View logs"
    echo "  test                 - Test deployment"
    echo "  stop                 - Stop containers"
    echo "  restart              - Restart containers"
    echo "  update               - Update to latest version"
    echo "  shell                - Open shell in container"
    echo "  interactive          - Interactive menu"
    echo "  help                 - Show this help"
    echo ""
    echo "Environment variables:"
    echo "  PI_USER              - Pi user (default: pi)"
    echo "  PI_HOST              - Pi hostname/IP"
    echo "  DOCKER_CONTEXT       - Docker context (default: pi)"
    echo "  EXTERNAL_CHAT_API_URL - External LLM API URL"
    echo "  EXTERNAL_CHAT_API_KEY   - External LLM API key"
}

# Execute command
if [ $# -gt 0 ]; then
    case "$1" in
        "deploy") main $@ ;;
        "logs") show_logs ;;
        "test") test_deployment ;;
        "stop") docker compose -f ${COMPOSE_FILE} --context ${DOCKER_CONTEXT} down ;;
        "restart") docker compose -f ${COMPOSE_FILE} --context ${DOCKER_CONTEXT} restart pi-rag ;;
        "update") update_service ;;
        "shell") docker exec -it pi-rag /bin/bash ;;
        "interactive") interactive ;;
        "help"|"--help"|"-h") usage ;;
        *) 
            echo "Unknown command: $1"
            usage
            exit 1
            ;;
    esac
else
    # Default to deploy if no arguments provided
    main
fi
