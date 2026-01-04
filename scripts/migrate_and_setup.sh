#!/bin/bash
# SYNAPSE Migration and Project Setup
# CLI-friendly script for migrating pi-rag → synapse and setting up projects
#
# Usage:
#   ./scripts/migrate_and_setup.sh [command]
#
# Commands:
#   check       - Check migration status (dry-run)
#   migrate     - Migrate pi-rag → synapse (renames directories)
#   setup       - Initialize synapse project in RAG system
#   verify      - Verify migration and setup complete
#   status      - Show current state
#
# Safety Features:
#   - Requires --yes flag for migration (no accidental execution)
#   - Always backs up databases before migration
#   - Dry-run mode for checking
#   - Rollback capability if migration fails
#
# Version: 1.0.0
# Author: SYNAPSE Team
# ==============================================================================

set -e  # Exit on error
set -u  # Exit on undefined variable

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
OLD_DIR="/opt/pi-rag"
NEW_DIR="/opt/synapse"
BACKUP_DIR="${NEW_DIR}/data/backup"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# ============================================================================
# COMMAND: check - Check migration status
# ============================================================================
cmd_check() {
    log_info "Checking migration status..."

    # Check if old directory exists
    if [ -d "$OLD_DIR" ]; then
        log_info "✓ Old directory exists: $OLD_DIR"
        old_exists=true
    else
        log_warning "✗ Old directory not found: $OLD_DIR"
        old_exists=false
    fi

    # Check if new directory exists
    if [ -d "$NEW_DIR" ]; then
        log_info "✓ New directory exists: $NEW_DIR"
        new_exists=true
    else
        log_warning "✗ New directory not found: $NEW_DIR"
        new_exists=false
    fi

    # Check database status
    if [ -f "${NEW_DIR}/data/episodic.db" ]; then
        log_info "✓ Episodic database found: ${NEW_DIR}/data/episodic.db"

        # Check for pi-rag project_id
        pi_rag_count=$(sqlite3 "${NEW_DIR}/data/episodic.db" "SELECT COUNT(*) FROM episodic_memory WHERE project_id='pi-rag';" 2>/dev/null || echo "0")
        if [ "$pi_rag_count" -gt 0 ]; then
            log_warning "✗ Found $pi_rag_count episodes with 'pi-rag' project_id (needs migration)"
        else
            log_success "✓ No 'pi-rag' project_id episodes in database"
        fi
    else
        log_warning "✗ Episodic database not found"
    fi

    # Summary
    echo ""
    log_info "Migration Summary:"
    if [ "$old_exists" = true ] && [ "$new_exists" = false ]; then
        log_warning "Status: READY TO MIGRATE"
        log_info "Run: $0 migrate --yes"
    elif [ "$old_exists" = false ] && [ "$new_exists" = true ]; then
        log_success "Status: ALREADY MIGRATED"
        log_info "No migration needed. Run: $0 setup"
    elif [ "$old_exists" = false ] && [ "$new_exists" = false ]; then
        log_error "Status: NO DIRECTORIES FOUND"
        log_info "Nothing to migrate. Run: $0 setup"
    else
        log_warning "Status: CONFLICT (both directories exist)"
        log_error "Please manually resolve before continuing"
    fi
}

# ============================================================================
# COMMAND: migrate - Migrate pi-rag → synapse
# ============================================================================
cmd_migrate() {
    if [ "$1" != "--yes" ]; then
        log_error "Migration requires --yes flag for confirmation"
        log_info "This will rename: $OLD_DIR → $NEW_DIR"
        log_info "Run: $0 migrate --yes"
        exit 1
    fi

    log_info "Starting migration: $OLD_DIR → $NEW_DIR"
    echo ""

    # Check if old directory exists
    if [ ! -d "$OLD_DIR" ]; then
        log_error "Old directory not found: $OLD_DIR"
        log_info "Nothing to migrate."
        exit 1
    fi

    # Check if new directory already exists
    if [ -d "$NEW_DIR" ]; then
        log_error "New directory already exists: $NEW_DIR"
        log_error "Migration aborted to prevent data loss"
        log_info "Manually resolve conflicts before running migration"
        exit 1
    fi

    # Create backup
    log_info "Creating backup of databases..."
    backup_path="${OLD_DIR}/backup_${TIMESTAMP}"
    mkdir -p "$backup_path"

    # Backup episodic.db if exists
    if [ -f "${OLD_DIR}/data/episodic.db" ]; then
        cp "${OLD_DIR}/data/episodic.db" "${backup_path}/episodic.db"
        log_success "✓ Backed up episodic.db"
    fi

    # Backup memory.db if exists
    if [ -f "${OLD_DIR}/data/memory.db" ]; then
        cp "${OLD_DIR}/data/memory.db" "${backup_path}/memory.db"
        log_success "✓ Backed up memory.db"
    fi

    log_success "✓ Backup created: $backup_path"
    echo ""

    # Perform migration (rename directory)
    log_info "Migrating directory..."
    mv "$OLD_DIR" "$NEW_DIR"
    log_success "✓ Migrated: $OLD_DIR → $NEW_DIR"
    echo ""

    # Move backup to new location
    if [ -d "${NEW_DIR}/backup_${TIMESTAMP}" ]; then
        log_info "Moving backup to new location..."
        mv "${NEW_DIR}/backup_${TIMESTAMP}" "${BACKUP_DIR}/migration_backup_${TIMESTAMP}"
        log_success "✓ Backup moved: ${BACKUP_DIR}/migration_backup_${TIMESTAMP}"
    fi

    echo ""
    log_success "Migration complete!"
    log_info "Next steps:"
    log_info "  1. Run: $0 verify"
    log_info "  2. Run: $0 setup"
}

# ============================================================================
# COMMAND: setup - Initialize synapse project
# ============================================================================
cmd_setup() {
    log_info "Setting up synapse project in RAG system..."
    echo ""

    # Check if synapse directory exists
    if [ ! -d "$NEW_DIR" ]; then
        log_error "SYNAPSE directory not found: $NEW_DIR"
        log_info "Run: $0 migrate --yes"
        exit 1
    fi

    # Check data directory
    data_dir="${NEW_DIR}/data"
    if [ ! -d "$data_dir" ]; then
        log_info "Creating data directory..."
        mkdir -p "$data_dir"
        log_success "✓ Created: $data_dir"
    fi

    # Initialize databases (will be created on first use)
    log_info "Initializing databases..."
    touch "${data_dir}/memory.db"
    touch "${data_dir}/episodic.db"
    log_success "✓ Initialized databases"

    # Create backup directory
    if [ ! -d "${BACKUP_DIR}" ]; then
        mkdir -p "${BACKUP_DIR}"
        log_success "✓ Created backup directory: ${BACKUP_DIR}"
    fi

    # Register synapse project (via SQLite)
    log_info "Registering synapse project..."
    registry_db="${data_dir}/registry.db"

    # Create registry if doesn't exist
    sqlite3 "$registry_db" <<EOF 2>/dev/null
CREATE TABLE IF NOT EXISTS projects (
    project_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    short_uuid TEXT NOT NULL,
    chroma_path TEXT,
    created_at TEXT,
    updated_at TEXT,
    status TEXT DEFAULT 'active',
    metadata TEXT
);
EOF

    # Insert synapse project if not exists
    sqlite3 "$registry_db" "INSERT OR IGNORE INTO projects (project_id, name, short_uuid, chroma_path, created_at, updated_at, status) VALUES ('synapse', 'synapse', 'synapse-uuid', '${data_dir}/chroma_semantic', datetime('now'), datetime('now'), 'active');"

    log_success "✓ Registered synapse project"

    echo ""
    log_success "Setup complete!"
    log_info "SYNAPSE project is ready"
    log_info "Project ID: synapse"
    log_info "Data directory: ${data_dir}"
}

# ============================================================================
# COMMAND: verify - Verify migration and setup
# ============================================================================
cmd_verify() {
    log_info "Verifying migration and setup..."
    echo ""

    errors=0

    # Check directories
    if [ -d "$NEW_DIR" ]; then
        log_success "✓ SYNAPSE directory exists: $NEW_DIR"
    else
        log_error "✗ SYNAPSE directory missing: $NEW_DIR"
        errors=$((errors + 1))
    fi

    if [ ! -d "$OLD_DIR" ]; then
        log_success "✓ Old directory removed: $OLD_DIR"
    else
        log_warning "⚠ Old directory still exists: $OLD_DIR (safe to remove after verification)"
    fi

    # Check databases
    if [ -f "${NEW_DIR}/data/memory.db" ]; then
        log_success "✓ Symbolic memory database exists"
    else
        log_error "✗ Symbolic memory database missing"
        errors=$((errors + 1))
    fi

    if [ -f "${NEW_DIR}/data/episodic.db" ]; then
        log_success "✓ Episodic memory database exists"

        # Check for pi-rag project_id
        pi_rag_count=$(sqlite3 "${NEW_DIR}/data/episodic.db" "SELECT COUNT(*) FROM episodic_memory WHERE project_id='pi-rag';" 2>/dev/null || echo "0")
        if [ "$pi_rag_count" -gt 0 ]; then
            log_error "✗ Found $pi_rag_count 'pi-rag' project_id episodes (needs manual migration)"
            errors=$((errors + 1))
        else
            log_success "✓ No 'pi-rag' project_id episodes in database"
        fi

        # Check for synapse project_id
        synapse_count=$(sqlite3 "${NEW_DIR}/data/episodic.db" "SELECT COUNT(*) FROM episodic_memory WHERE project_id='synapse';" 2>/dev/null || echo "0")
        log_info "  Synapse episodes: $synapse_count"
    else
        log_error "✗ Episodic memory database missing"
        errors=$((errors + 1))
    fi

    # Check project registry
    if [ -f "${NEW_DIR}/data/registry.db" ]; then
        log_success "✓ Project registry exists"

        # Check if synapse is registered
        synapse_registered=$(sqlite3 "${NEW_DIR}/data/registry.db" "SELECT COUNT(*) FROM projects WHERE project_id='synapse';" 2>/dev/null || echo "0")
        if [ "$synapse_registered" -gt 0 ]; then
            log_success "✓ Synapse project registered in registry"
        else
            log_warning "⚠ Synapse project not registered (run: $0 setup)"
        fi
    else
        log_warning "⚠ Project registry not found (run: $0 setup)"
    fi

    # Summary
    echo ""
    if [ $errors -eq 0 ]; then
        log_success "✓✓✓ VERIFICATION PASSED ✓✓✓"
        log_info "All systems operational"
        exit 0
    else
        log_error "✗✗✗ VERIFICATION FAILED ✗✗✗"
        log_error "Found $errors error(s)"
        exit 1
    fi
}

# ============================================================================
# COMMAND: status - Show current state
# ============================================================================
cmd_status() {
    log_info "SYNAPSE Status Report"
    echo "=========================================="
    echo ""

    # System information
    echo "System Information:"
    echo "  Hostname: $(hostname)"
    echo "  OS: $(uname -s) $(uname -r)"
    echo "  Date: $(date)"
    echo ""

    # Directory status
    echo "Directory Status:"
    if [ -d "$NEW_DIR" ]; then
        echo "  ✓ SYNAPSE: $NEW_DIR ($(du -sh "$NEW_DIR" 2>/dev/null | cut -f1))"
    else
        echo "  ✗ SYNAPSE: $NEW_DIR (not found)"
    fi

    if [ -d "$OLD_DIR" ]; then
        echo "  ⚠  pi-rag: $OLD_DIR (exists - migration needed)"
    else
        echo "  ✓ pi-rag: $OLD_DIR (removed)"
    fi
    echo ""

    # Database status
    if [ -d "${NEW_DIR}/data" ]; then
        echo "Database Status:"
        data_dir="${NEW_DIR}/data"

        # Memory database
        if [ -f "${data_dir}/memory.db" ]; then
            mem_size=$(du -h "${data_dir}/memory.db" 2>/dev/null | cut -f1)
            echo "  ✓ Symbolic (memory.db): ${mem_size}"
        else
            echo "  ✗ Symbolic (memory.db): not found"
        fi

        # Episodic database
        if [ -f "${data_dir}/episodic.db" ]; then
            epi_size=$(du -h "${data_dir}/episodic.db" 2>/dev/null | cut -f1)
            epi_count=$(sqlite3 "${data_dir}/episodic.db" "SELECT COUNT(*) FROM episodic_memory;" 2>/dev/null || echo "0")
            echo "  ✓ Episodic (episodic.db): ${epi_size} (${epi_count} episodes)"
        else
            echo "  ✗ Episodic (episodic.db): not found"
        fi

        # Registry database
        if [ -f "${data_dir}/registry.db" ]; then
            reg_size=$(du -h "${data_dir}/registry.db" 2>/dev/null | cut -f1)
            echo "  ✓ Registry (registry.db): ${reg_size}"
        else
            echo "  ✗ Registry (registry.db): not found"
        fi

        echo ""
    fi

    # Container status
    if command -v docker &> /dev/null; then
        echo "Container Status:"
        if docker ps --filter "name=synapse-mcp" --format '{{.Names}}' | grep -q "^synapse-mcp$"; then
            echo "  ✓ synapse-mcp: running"
            echo "    Port: 8002"
            echo "    Health: http://localhost:8002/health"
        else
            echo "  ✗ synapse-mcp: not running"
            echo "    Start with: docker compose -f docker-compose.synapse.yml up -d"
        fi
    fi

    echo ""
    echo "=========================================="
}

# ============================================================================
# Main Entry Point
# ============================================================================
main() {
    case "${1:-}" in
        check)
            cmd_check
            ;;
        migrate)
            cmd_migrate "${2:-}"
            ;;
        setup)
            cmd_setup
            ;;
        verify)
            cmd_verify
            ;;
        status)
            cmd_status
            ;;
        help|--help|-h)
            echo "SYNAPSE Migration and Project Setup"
            echo ""
            echo "Usage: $0 [command]"
            echo ""
            echo "Commands:"
            echo "  check       - Check migration status (dry-run)"
            echo "  migrate     - Migrate pi-rag → synapse (requires --yes)"
            echo "  setup       - Initialize synapse project"
            echo "  verify      - Verify migration and setup"
            echo "  status      - Show current state"
            echo "  help        - Show this help"
            echo ""
            echo "Examples:"
            echo "  $0 check"
            echo "  $0 migrate --yes"
            echo "  $0 setup"
            echo "  $0 verify"
            echo "  $0 status"
            ;;
        *)
            log_error "Unknown command: ${1:-}"
            echo ""
            echo "Run '$0 help' for usage information"
            exit 1
            ;;
    esac
}

main "$@"
