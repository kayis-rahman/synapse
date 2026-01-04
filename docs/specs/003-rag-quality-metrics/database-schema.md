# Metrics Database Schema

**Feature ID**: 003-rag-quality-metrics
**Status**: Phase 1 - Task 1.2
**Created**: January 4, 2026

---

## Overview

This document defines the time-series database schema for RAG quality metrics dashboard.

## Design Decision

**Database Choice**: SQLite (Simpler, no additional dependencies)

**Rationale**:
- Simpler deployment (no InfluxDB service to manage)
- Lower resource usage (important for Raspberry Pi 5)
- Sufficient for 1-second intervals, 90-day retention (~7.7M data points)
- Easy backup and export
- Familiar to Synapse team

**Trade-offs**:
- Less efficient than InfluxDB for very long time ranges
- No built-in compression (will implement manual)
- No built-in downsampling

**Mitigation**:
- Implement proper indexing
- Aggregation strategy (store raw 24h, aggregated thereafter)
- Automatic cleanup of old data

---

## Tables

### 1. metrics_raw

Stores raw metric data points at 1-second intervals.

```sql
CREATE TABLE IF NOT EXISTS metrics_raw (
    metric_id TEXT PRIMARY KEY,
    metric_type TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    value REAL NOT NULL,
    tags TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

**Columns:**
- `metric_id`: Unique identifier (UUID)
- `metric_type`: Type of metric (retrieval_quality, tool_performance, memory_usage, auto_learning, system_resources)
- `timestamp`: ISO8601 format timestamp
- `value`: Metric value (score, percentage, ms, bytes, etc.)
- `tags`: JSON string with additional metadata (memory_type, tool_name, etc.)
- `created_at`: When metric was recorded

**Indexes:**
```sql
CREATE INDEX IF NOT EXISTS idx_raw_metric_type ON metrics_raw(metric_type, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_raw_timestamp ON metrics_raw(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_raw_tags ON metrics_raw(tags);
```

**Data Types:**

**retrieval_quality** (value: 0.0-1.0):
```json
{
  "memory_type": "symbolic" | "episodic" | "semantic",
  "score": 0.85,
  "query_count": 10,
  "avg_latency_ms": 45.2
}
```

**tool_performance** (value: avg_latency_ms, error_rate):
```json
{
  "tool_name": "rag.search",
  "operation_count": 1,
  "error_count": 0,
  "avg_latency_ms": 45.2,
  "p50_latency_ms": 35.1,
  "p95_latency_ms": 78.3,
  "p99_latency_ms": 120.5
}
```

**memory_usage** (value: storage_mb):
```json
{
  "memory_type": "symbolic" | "episodic" | "semantic",
  "storage_mb": 125.5,
  "document_count": 1523,
  "chunk_count": 12547
}
```

**auto_learning** (value: episodes_created, facts_created, avg_confidence):
```json
{
  "episodes_created": 5,
  "facts_created": 12,
  "avg_confidence": 0.75
}
```

**system_resources** (value: cpu_percent, memory_percent, disk_usage_mb):
```json
{
  "cpu_percent": 23.5,
  "memory_percent": 67.2,
  "disk_usage_mb": 1024.5
}
```

### 2. metrics_aggregated

Stores pre-aggregated metrics for faster dashboard queries.

```sql
CREATE TABLE IF NOT EXISTS metrics_aggregated (
    aggregation_id TEXT PRIMARY KEY,
    metric_type TEXT NOT NULL,
    interval TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    avg_value REAL,
    min_value REAL,
    max_value REAL,
    p50_value REAL,
    p95_value REAL,
    p99_value REAL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

**Columns:**
- `aggregation_id`: Unique identifier (UUID)
- `metric_type`: Type of metric (same as metrics_raw)
- `interval`: Aggregation window ("1m", "5m", "1h", "24h")
- `timestamp`: Start of aggregation window (ISO8601)
- `avg_value`: Average value in window
- `min_value`: Minimum value in window
- `max_value`: Maximum value in window
- `p50_value`: 50th percentile
- `p95_value`: 95th percentile
- `p99_value`: 99th percentile

**Indexes:**
```sql
CREATE INDEX IF NOT EXISTS idx_agg_metric_type ON metrics_aggregated(metric_type, interval, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_agg_timestamp ON metrics_aggregated(timestamp DESC);
```

**Intervals:**
- `1m`: 1-minute averages
- `5m`: 5-minute averages
- `1h`: 1-hour averages
- `24h`: 24-hour averages

### 3. alerts

Stores alert configuration and status.

```sql
CREATE TABLE IF NOT EXISTS alerts (
    alert_id TEXT PRIMARY KEY,
    metric_type TEXT NOT NULL,
    threshold REAL NOT NULL,
    comparison TEXT NOT NULL,
    channels TEXT NOT NULL,
    last_triggered_at TEXT,
    is_enabled BOOLEAN DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

**Columns:**
- `alert_id`: Unique identifier (UUID)
- `metric_type`: Type of metric to monitor (retrieval_quality, tool_latency, etc.)
- `threshold`: Alert threshold value (e.g., 0.7 for retrieval quality, 500ms for latency)
- `comparison`: How to compare ("greater_than", "less_than", "outside_range")
- `channels`: JSON array of notification channels (["email"], ["webhook"], ["email", "webhook"])
- `last_triggered_at`: Last time alert was triggered (ISO8601)
- `is_enabled`: Whether alert is active
- `created_at`: When alert was created

**Comparison Examples:**
```json
{
  "comparison": "greater_than",
  "threshold": 0.7,
  "description": "Alert if value > 0.7"
}

{
  "comparison": "outside_range",
  "threshold": 0.5,
  "range_low": 0.7,
  "range_high": 0.95,
  "description": "Alert if value outside [0.7, 0.95]"
}
```

### 4. alert_history

Stores history of alert triggers and acknowledgments.

```sql
CREATE TABLE IF NOT EXISTS alert_history (
    history_id TEXT PRIMARY KEY,
    alert_id TEXT NOT NULL,
    triggered_at TEXT NOT NULL,
    value REAL NOT NULL,
    acknowledged_at TEXT,
    metadata TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (alert_id) REFERENCES alerts(alert_id) ON DELETE CASCADE
);
```

**Columns:**
- `history_id`: Unique identifier (UUID)
- `alert_id`: Reference to alert configuration
- `triggered_at`: When alert was triggered (ISO8601)
- `value`: Metric value that triggered the alert
- `acknowledged_at`: When alert was acknowledged (NULL if not acknowledged)
- `metadata`: Additional context (JSON)
- `created_at`: When history entry was created

**Indexes:**
```sql
CREATE INDEX IF NOT EXISTS idx_history_alert ON alert_history(alert_id, triggered_at DESC);
CREATE INDEX IF NOT EXISTS idx_history_timestamp ON alert_history(triggered_at DESC);
```

---

## Query Optimization

### Efficient Range Queries

```sql
-- Fast query for last 24 hours of retrieval quality
SELECT metric_type, timestamp, value, tags
FROM metrics_raw
WHERE metric_type = 'retrieval_quality'
  AND timestamp >= datetime('now', '-24 hours')
ORDER BY timestamp DESC;
```

### Aggregation Query Pattern

```sql
-- Calculate 1-hour averages
SELECT
    metric_type,
    '1h' as interval,
    datetime(timestamp, 'start of hour') as timestamp,
    AVG(value) as avg_value,
    MIN(value) as min_value,
    MAX(value) as max_value
FROM metrics_raw
WHERE timestamp >= datetime('now', '-1 hour')
GROUP BY
    metric_type,
    strftime('%Y-%m-%d %H', timestamp)
ORDER BY timestamp DESC;
```

### Cleanup Query

```sql
-- Delete metrics older than retention period
DELETE FROM metrics_raw
WHERE created_at < datetime('now', '-90 days');

DELETE FROM metrics_aggregated
WHERE created_at < datetime('now', '-90 days');

DELETE FROM alert_history
WHERE created_at < datetime('now', '-90 days');
```

---

## Data Volume Estimates

### Storage Calculations

**1-second intervals, 90-day retention:**
- Total seconds: 90 × 24 × 3600 = 7,776,000
- Metric types: 5 (retrieval_quality, tool_performance, memory_usage, auto_learning, system_resources)
- Total data points: 7,776,000 × 5 = 38,880,000 rows

**Row Size Estimate (with indexes):**
- Average row size: ~150 bytes
- Total storage: 38,880,000 × 150 bytes ≈ 5.5 GB

**Optimization (with 24h raw retention + aggregation):**
- Raw data: 24h × 3600 = 86,400 points per type × 5 = 432,000 points
- Raw storage: 432,000 × 150 bytes ≈ 60 MB
- Aggregated data: 86 hours × 4 intervals = 344 points × 5 = 1,720 points
- Aggregated storage: 1,720 × 250 bytes ≈ 0.4 MB
- Total: ~60.4 MB

**Optimization Strategy:**
- Store raw metrics for 24 hours
- Create 1m, 5m, 1h, 24h aggregated metrics
- Delete raw after 24 hours
- Keep aggregated for 90 days

**Result**: ~99% storage reduction (5.5 GB → 60 MB)

---

## Performance Considerations

### Write Performance
- All INSERTs use prepared statements
- Batch inserts for multiple metrics
- WAL mode enabled for concurrent access

### Query Performance
- Proper indexes on frequently queried columns
- Use EXPLAIN QUERY PLAN before production
- Pagination for large result sets

### Maintenance
- VACUUM weekly to reclaim space
- ANALYZE after bulk deletes
- Rebuild indexes if performance degrades

---

## Migration Strategy

### Versioning

Database version stored in `meta` table:

```sql
CREATE TABLE IF NOT EXISTS meta (
    key TEXT PRIMARY KEY,
    value TEXT
);

INSERT INTO meta (key, value) VALUES ('db_version', '1.0.0');
```

### Migration Scripts

Named migration files: `migrations/001_initial_schema.sql`, `migrations/002_add_indexes.sql`, etc.

### Rollback Plan

- Keep migration scripts in version control
- Document rollback procedure
- Backup database before migrations

---

**Last Updated**: January 4, 2026
