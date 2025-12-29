-- Symbolic Memory Database Schema
-- Postgres-compatible SQLite schema for deterministic fact storage
-- Design Rules:
-- - No embeddings, no vector DB
-- - Explicit facts only (no guesses, no auto-persistence)
-- - Every memory entry has: scope, category, confidence, source
-- - Deterministic CRUD operations

-- Table: memory_facts
-- Stores explicit, durable facts with full audit trail
CREATE TABLE IF NOT EXISTS memory_facts (
    id TEXT PRIMARY KEY,              -- UUID for uniqueness
    scope TEXT NOT NULL,              -- user | project | org | session
    category TEXT NOT NULL,           -- preference | constraint | decision | fact
    key TEXT NOT NULL,                -- Unique identifier within scope
    value TEXT NOT NULL,              -- JSON string (flexible values)
    confidence REAL NOT NULL CHECK(confidence >= 0.0 AND confidence <= 1.0),
    source TEXT NOT NULL,             -- user | agent | tool
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    -- Ensure uniqueness of (scope, key) combination
    -- This prevents duplicate facts within the same scope
    CONSTRAINT unique_scope_key UNIQUE (scope, key)
);

-- Index: idx_scope_key
-- Fast lookups by scope and key (common pattern: "get user's X preference")
CREATE INDEX IF NOT EXISTS idx_scope_key ON memory_facts(scope, key);

-- Index: idx_category_scope
-- Fast filtering by category within scopes (e.g., "all user preferences")
CREATE INDEX IF NOT EXISTS idx_category_scope ON memory_facts(category, scope);

-- Index: idx_confidence
-- For conflict resolution (highest confidence wins)
CREATE INDEX IF NOT EXISTS idx_confidence ON memory_facts(confidence DESC);

-- Table: memory_audit_log
-- Full audit trail for compliance and debugging
-- Stores all write operations with timestamps and previous values
CREATE TABLE IF NOT EXISTS memory_audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fact_id TEXT NOT NULL,
    operation TEXT NOT NULL CHECK(operation IN ('INSERT', 'UPDATE', 'DELETE')),
    old_value TEXT,                   -- Previous value (for UPDATE/DELETE)
    new_value TEXT,                  -- New value (for INSERT/UPDATE), NULL for DELETE
    changed_by TEXT NOT NULL,         -- Who made the change
    changed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fact_id) REFERENCES memory_facts(id) ON DELETE CASCADE
);

-- Index: idx_audit_fact_id
-- Fast lookup of all changes for a specific fact
CREATE INDEX IF NOT EXISTS idx_audit_fact_id ON memory_audit_log(fact_id);

-- Trigger: update_timestamp
-- Automatically update the updated_at timestamp on row modifications
CREATE TRIGGER IF NOT EXISTS update_timestamp
AFTER UPDATE ON memory_facts
FOR EACH ROW
BEGIN
    UPDATE memory_facts
    SET updated_at = CURRENT_TIMESTAMP
    WHERE id = NEW.id;
END;

-- Trigger: audit_insert
-- Log all insert operations to audit trail
CREATE TRIGGER IF NOT EXISTS audit_insert
AFTER INSERT ON memory_facts
FOR EACH ROW
BEGIN
    INSERT INTO memory_audit_log (
        fact_id, operation, old_value, new_value, changed_by, changed_at
    ) VALUES (
        NEW.id,
        'INSERT',
        NULL,
        NEW.value,
        NEW.source,
        CURRENT_TIMESTAMP
    );
END;

-- Trigger: audit_update
-- Log all update operations to audit trail
CREATE TRIGGER IF NOT EXISTS audit_update
AFTER UPDATE ON memory_facts
FOR EACH ROW
BEGIN
    INSERT INTO memory_audit_log (
        fact_id, operation, old_value, new_value, changed_by, changed_at
    ) VALUES (
        NEW.id,
        'UPDATE',
        OLD.value,
        NEW.value,
        NEW.source,
        CURRENT_TIMESTAMP
    );
END;

-- Trigger: audit_delete
-- Log all delete operations to audit trail
CREATE TRIGGER IF NOT EXISTS audit_delete
AFTER DELETE ON memory_facts
FOR EACH ROW
WHEN OLD.source IS NOT NULL
BEGIN
    INSERT INTO memory_audit_log (
        fact_id, operation, old_value, changed_by, changed_at
    ) VALUES (
        OLD.id,
        'DELETE',
        OLD.value,
        OLD.source,
        CURRENT_TIMESTAMP
    );
END;

-- View: memory_summary
-- Aggregated view for quick stats and monitoring
CREATE VIEW IF NOT EXISTS memory_summary AS
SELECT
    scope,
    category,
    COUNT(*) as fact_count,
    AVG(confidence) as avg_confidence,
    MIN(created_at) as earliest_fact,
    MAX(updated_at) as latest_update
FROM memory_facts
GROUP BY scope, category;

-- View: high_confidence_facts
-- Only facts with confidence >= 0.8 (trustworthy facts)
CREATE VIEW IF NOT EXISTS high_confidence_facts AS
SELECT
    id,
    scope,
    category,
    key,
    value,
    confidence,
    source,
    created_at,
    updated_at
FROM memory_facts
WHERE confidence >= 0.8;
