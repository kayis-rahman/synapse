# Tasks: RAG Quality Metrics Dashboard

**Feature ID**: 003-rag-quality-metrics
**Status**: Planning Phase
**Created**: January 4, 2026

---

## Phase 1: Metrics Collection Foundation (1-2 hours)

### 1.1 Setup & Configuration
- [ ] Create `configs/metrics_config.json` configuration file
- [ ] Add metrics section to main `rag_config.json`
- [ ] Define collection interval (default: 1 second)
- [ ] Define retention policy (default: 90 days)
- [ ] Configure database path (/opt/synapse/data/metrics.db)
- [ ] Add metrics port configuration (8003)

**Linked to**: Requirement FR-1, NFR-1

### 1.2 Database Schema Design
- [ ] Design `metrics_raw` table schema
- [ ] Design `metrics_aggregated` table schema
- [ ] Design `alerts` table schema
- [ ] Design `alert_history` table schema
- [ ] Define indexes for efficient querying
- [ ] Define retention policy queries
- [ ] Document schema in `docs/architecture/metrics-schema.md`

**Linked to**: Requirement DR-1, DR-2

### 1.3 MetricsCollector Class Skeleton
- [ ] Create `rag/metrics_collector.py` module
- [ ] Implement `__init__()` with configuration loading
- [ ] Implement `record_retrieval_quality()` method
- [ ] Implement `record_tool_performance()` method
- [ ] Implement `record_memory_usage()` method
- [ ] Implement `record_auto_learning()` method
- [ ] Implement `record_system_resources()` method
- [ ] Add logging for debugging

**Linked to**: Requirement FR-1

### 1.4 Background Collection Thread
- [ ] Implement APScheduler integration
- [ ] Create periodic task for resource monitoring (1s interval)
- [ ] Create periodic task for aggregation (1m interval)
- [ ] Implement graceful shutdown handling
- [ ] Add thread-safe metrics storage
- [ ] Implement retry logic for database errors

**Linked to**: Requirement FR-1, NFR-2

---

## Phase 2: Dashboard API (1-2 hours)

### 2.1 FastAPI Application Setup
- [ ] Create `api/metrics_api.py` module
- [ ] Initialize FastAPI application
- [ ] Add CORS middleware
- [ ] Add API key authentication middleware
- [ ] Configure Uvicorn server on port 8003
- [ ] Add health check endpoint

**Linked to**: Requirement FR-3, NFR-4

### 2.2 Metrics Endpoints
- [ ] Implement `GET /api/metrics/retrieval-quality`
- [ ] Implement `GET /api/metrics/tool-performance`
- [ ] Implement `GET /api/metrics/memory-usage`
- [ ] Implement `GET /api/metrics/auto-learning`
- [ ] Implement `GET /api/metrics/system-resources`
- [ ] Add time range query parameters
- [ ] Add memory type filtering
- [ ] Add pagination support

**Linked to**: Requirement US-1, US-2, US-3, US-4, US-5

### 2.3 Alert Management Endpoints
- [ ] Implement `GET /api/alerts` (list all alerts)
- [ ] Implement `POST /api/alerts` (create/update alert)
- [ ] Implement `DELETE /api/alerts/{id}` (delete alert)
- [ ] Implement `GET /api/alerts/history` (alert trigger history)
- [ ] Implement `POST /api/alerts/{id}/acknowledge` (acknowledge alert)
- [ ] Add alert threshold validation

**Linked to**: Requirement US-6, FR-4

### 2.4 Export Endpoints
- [ ] Implement `GET /api/export` (query params for filtering)
- [ ] Implement JSON export format
- [ ] Implement CSV export format
- [ ] Add time range parameter
- [ ] Add metric type filtering
- [ ] Add response compression (gzip)

**Linked to**: Requirement US-7, FR-5

---

## Phase 3: Web Dashboard UI (2-3 hours)

### 3.1 Dashboard Framework Setup
- [ ] Choose framework (React or Vue)
- [ ] Initialize project with build tool (Vite/CRA)
- [ ] Set up routing structure
- [ ] Configure HTTP client (Axios)
- [ ] Set up environment variables (API URL, API key)
- [ ] Add CSS framework (Tailwind or Bootstrap)

**Linked to**: Requirement FR-3, NFR-3

### 3.2 Core Layout Components
- [ ] Create main dashboard layout
- [ ] Create navigation sidebar
- [ ] Create header with status indicator
- [ ] Implement responsive design (mobile/tablet/desktop)
- [ ] Add dark/light mode toggle

**Linked to**: Requirement US-1, NFR-4

### 3.3 Health Status Component
- [ ] Create overall health score display
- [ ] Add color-coded status (green/yellow/red)
- [ ] Add last updated timestamp
- [ ] Implement drill-down on click
- [ ] Add auto-refresh (10s interval)

**Linked to**: Requirement US-1

### 3.4 Retrieval Quality Charts
- [ ] Create line chart for retrieval scores
- [ ] Add time range selector (1h/24h/7d/30d)
- [ ] Add memory type filter (symbolic/episodic/semantic)
- [ ] Add aggregate metrics (avg, min, max, p50, p95)
- [ ] Implement tooltip with detailed info

**Linked to**: Requirement US-2

### 3.5 Tool Performance Charts
- [ ] Create bar chart for tool latency
- [ ] Add error rate percentage display
- [ ] Sort by slowest tools
- [ ] Add time range selector
- [ ] Add click to view tool logs

**Linked to**: Requirement US-3

### 3.6 Memory Usage Charts
- [ ] Create pie chart for storage by memory type
- [ ] Create line chart for growth over time
- [ ] Add total storage vs. available
- [ ] Add file count per memory type
- [ ] Add largest documents/sources list

**Linked to**: Requirement US-4

### 3.7 Auto-Learning Analytics
- [ ] Create line chart for episodes per day
- [ ] Create line chart for facts per day
- [ ] Create histogram for confidence distribution
- [ ] Add deduplication hit rate display
- [ ] Add manual vs. auto-added ratio

**Linked to**: Requirement US-5

### 3.8 Alert Configuration UI
- [ ] Create alert list view
- [ ] Implement form to create/edit alerts
- [ ] Add threshold input with validation
- [ ] Add notification channel selection (email/webhook)
- [ ] Add alert history log

**Linked to**: Requirement US-6

### 3.9 Data Export Components
- [ ] Create export form with filters
- [ ] Implement JSON export download
- [ ] Implement CSV export download
- [ ] Add time range selection
- [ ] Add metric type selection
- [ ] Show export history

**Linked to**: Requirement US-7

---

## Phase 4: Instrumentation Integration (1-2 hours)

### 4.1 RAG Operations Instrumentation
- [ ] Modify `rag/orchestrator.py` to record metrics
- [ ] Modify `rag/retriever.py` to record retrieval quality
- [ ] Modify `rag/vectorstore.py` to record query metrics
- [ ] Add metrics recording to all search operations
- [ ] Add metrics recording to all ingest operations

**Linked to**: Requirement FR-1

### 4.2 MCP Tool Instrumentation
- [ ] Modify `mcp_server/rag_server.py` tool wrappers
- [ ] Add metrics recording to `list_projects()`
- [ ] Add metrics recording to `list_sources()`
- [ ] Add metrics recording to `get_context()`
- [ ] Add metrics recording to `search()`
- [ ] Add metrics recording to `ingest_file()`
- [ ] Add metrics recording to `add_fact()`
- [ ] Add metrics recording to `add_episode()`

**Linked to**: Requirement FR-1, NFR-2

### 4.3 Auto-Learning Metrics Integration
- [ ] Modify `rag/auto_learning_tracker.py` to emit metrics
- [ ] Record episode creation events
- [ ] Record fact extraction events
- [ ] Record confidence scores
- [ ] Record deduplication events

**Linked to**: Requirement US-5

### 4.4 System Resource Monitoring
- [ ] Create `rag/resource_monitor.py` module
- [ ] Implement CPU monitoring via psutil
- [ ] Implement memory monitoring via psutil
- [ ] Implement disk monitoring via psutil
- [ ] Implement network monitoring via psutil
- [ ] Add to MetricsCollector periodic tasks

**Linked to**: Requirement FR-1, NFR-2

---

## Phase 5: Testing (2-3 hours)

### 5.1 Unit Tests
- [ ] Create `tests/unit/rag/test_metrics_collector.py`
- [ ] Test all MetricsCollector methods
- [ ] Test thread-safe operations
- [ ] Test database schema operations
- [ ] Test aggregation logic
- [ ] Test alert threshold validation

**Linked to**: Requirement NFR-5

### 5.2 Integration Tests
- [ ] Create `tests/integration/test_metrics_api.py`
- [ ] Test all API endpoints
- [ ] Test alert creation and triggering
- [ ] Test export functionality
- [ ] Test authentication middleware
- [ ] Test concurrent API calls

**Linked to**: Requirement NFR-5

### 5.3 End-to-End Tests
- [ ] Test complete metrics collection flow
- [ ] Test dashboard UI with real metrics
- [ ] Test alert triggering and notifications
- [ ] Test export functionality
- [ ] Test performance under load

**Linked to**: Requirement NFR-5

### 5.4 Performance Tests
- [ ] Measure metrics collection overhead (<5% CPU, <100MB RAM)
- [ ] Measure API response times (<100ms p95)
- [ ] Test database query performance
- [ ] Test dashboard load time (<2s)
- [ ] Test concurrent dashboard viewers (100+)

**Linked to**: Requirement NFR-1

---

## Phase 6: Deployment (1 hour)

### 6.1 Docker Configuration
- [ ] Create `docker-compose.metrics.yml`
- [ ] Create `Dockerfile.metrics`
- [ ] Configure InfluxDB service (if using InfluxDB)
- [ ] Configure metrics API service
- [ ] Configure volume mounts
- [ ] Configure networking

**Linked to**: Requirement FR-3, NFR-4

### 6.2 Documentation
- [ ] Create `docs/metrics-setup.md`
- [ ] Document configuration options
- [ ] Document dashboard usage
- [ ] Document alert configuration
- [ ] Document export functionality
- [ ] Update README.md with metrics dashboard section

**Linked to**: Requirement NFR-5

### 6.3 Deployment & Verification
- [ ] Build Docker images
- [ ] Deploy to production (Raspberry Pi 5)
- [ ] Verify metrics collection is working
- [ ] Verify dashboard is accessible
- [ ] Test real-time updates
- [ ] Verify alerts can be triggered

**Linked to**: Requirement NFR-5

---

## Status Legend

- `[ ]` - Not started
- `[x]` - Completed
- `[~]` - In progress

---

## Notes

### Phase 1 Status
**Current**: Planning phase - awaiting approval to begin implementation
**Next**: Once Phase 1 is approved, will begin implementation tasks

### Dependencies
- All new modules depend on existing RAG components
- No breaking changes to existing APIs
- Metrics collection is non-invasive (wrappers only)

### Open Questions
1. Should we use InfluxDB or SQLite for time-series database?
2. Should dashboard be React or Vue?
3. Should we expose metrics via existing MCP protocol or separate API?

---

**Last Updated**: January 4, 2026
