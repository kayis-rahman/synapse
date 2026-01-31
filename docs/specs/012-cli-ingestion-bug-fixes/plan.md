# Feature 012 - CLI & Ingestion Bug Fixes: Technical Plan

**Feature ID**: 012-cli-ingestion-bug-fixes  
**Status**: [In Progress]  
**Created**: January 31, 2026  
**Objective**: Fix 7 bugs from Feature 010 validation

---

## 🎯 Technical Approach

### Strategy Overview

Fix bugs in priority order:
1. **Phase 1-2**: Quick wins (CLI config/models - 2-5 hours)
2. **Phase 3-4**: Core features (CLI ingest/query - 6-8 hours)  
3. **Phase 5**: Critical fix (BUG-INGEST-01 - 4-5 hours)
4. **Phase 6**: Testing and validation (2-3 hours)

**Total**: 16-19 hours across 54 tasks

---

## 🐛 Bug Fix Approaches

### BUG-004: Config JSON Output

**Problem**: `--json` flag not implemented  
**Approach**: Add JSON formatting to config command

**Implementation**:
```python
# In synapse/cli/commands/config.py

@app.command()
def config(
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output as JSON"
    ),
    verbose: bool = False
):
    config_data = get_config()
    
    if json_output:
        # Format as JSON
        import json
        typer.echo(json.dumps(config_data, indent=2))
    else:
        # Existing text output
        print_config_summary(config_data)
```

**Files Modified**:
- `synapse/cli/commands/config.py`

**Tests**:
- Test `--json` flag outputs valid JSON
- Test JSON contains all config sections
- Test error handling

---

### BUG-005: Config Output Formatting

**Problem**: Output formatting issues  
**Approach**: Improve print_config_summary function

**Implementation**:
- Add consistent spacing
- Add section headers
- Use typer styling for readability
- Add color coding for status

**Files Modified**:
- `synapse/cli/commands/config.py`
- `synapse/config/__init__.py`

---

### BUG-006: Models List Incomplete

**Problem**: Shows incomplete model list  
**Approach**: Fix model detection logic

**Implementation**:
```python
# In synapse/cli/commands/models.py

def list_models():
    """List available and installed models."""
    models_dir = Path("~/.synapse/models").expanduser()
    required_models = {
        "embedding": "bge-m3-q8_0.gguf",
        "chat": "gemma-3-1b-it-UD-Q4_K_XL.gguf"
    }
    
    for model_type, filename in required_models.items():
        model_path = models_dir / filename
        if model_path.exists():
            size_mb = model_path.stat().st_size / (1024 * 1024)
            typer.echo(f"✓ {model_type}: {model_path} ({size_mb:.1f} MB)")
        else:
            typer.echo(f"✗ {model_type}: Not installed")
            typer.echo(f"  Download with: synapse models download {model_type}")
```

**Files Modified**:
- `synapse/cli/commands/models.py`

---

### BUG-007: Ingest Command Implementation

**Problem**: Not implemented (stub message)  
**Approach**: Implement full ingest using MCP tools

**Implementation**:
```python
# In synapse/cli/commands/ingest.py

@app.command()
def ingest(
    path: Path = typer.Argument(
        ...,
        help="Path to file or directory to ingest"
    ),
    project_id: str = typer.Option(
        "synapse",
        "--project-id", "-p",
        help="Project ID for ingestion"
    ),
    code_mode: bool = typer.Option(
        False,
        "--code-mode", "-c",
        help="Enable code indexing mode"
    ),
    chunk_size: int = typer.Option(
        500,
        "--chunk-size",
        help="Chunk size in characters"
    )
):
    """Ingest documents into SYNAPSE knowledge base."""
    
    if not path.exists():
        typer.echo(f"❌ Error: Path does not exist: {path}")
        raise typer.Exit(1)
    
    # Use MCP ingest_file tool
    import requests
    
    files = []
    if path.is_file():
        files.append(path)
    else:
        # Recursively find all files
        for ext in [".py", ".md", ".txt", ".json"]:
            files.extend(path.rglob(f"*{ext}"))
    
    typer.echo(f"📄 Found {len(files)} files to ingest")
    
    # Ingest each file via MCP
    success_count = 0
    error_count = 0
    
    for file_path in files:
        try:
            # Call MCP ingest_file tool
            response = requests.post(
                "http://localhost:8002/mcp",
                headers={
                    "Accept": "application/json, text/event-stream",
                    "Content-Type": "application/json"
                },
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/call",
                    "params": {
                        "name": "ingest_file",
                        "arguments": {
                            "file_path": str(file_path),
                            "project_id": project_id,
                            "chunk_size": chunk_size
                        }
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                success_count += 1
                typer.echo(f"✓ Ingested: {file_path.name}")
            else:
                error_count += 1
                typer.echo(f"✗ Failed: {file_path.name}")
                
        except Exception as e:
            error_count += 1
            typer.echo(f"✗ Error: {file_path.name} - {e}")
    
    typer.echo(f"\n✅ Ingestion complete: {success_count} success, {error_count} errors")
```

**Files Modified**:
- `synapse/cli/commands/ingest.py`

**Tests**:
- Test single file ingestion
- Test directory ingestion
- Test error handling
- Test MCP tool integration

---

### BUG-008: Query Command Implementation

**Problem**: Not implemented (stub message)  
**Approach**: Implement full query using MCP search tool

**Implementation**:
```python
# In synapse/cli/commands/query.py

@app.command()
def query(
    text: str = typer.Argument(
        ...,
        help="Query text to search knowledge base"
    ),
    top_k: int = typer.Option(
        3,
        "--top-k", "-k",
        help="Number of results to return"
    ),
    format: str = Option(
        "json",
        "--format", "-f",
        help="Output format: json or text"
    ),
    mode: str = Option(
        "default",
        "--mode", "-m",
        help="Query mode: default, code, structured"
    )
):
    """Query SYNAPSE knowledge base."""
    
    import requests
    import json
    
    # Call MCP search tool
    response = requests.post(
        "http://localhost:8002/mcp",
        headers={
            "Accept": "application/json, text/event-stream", 
            "Content-Type": "application/json"
        },
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "search",
                "arguments": {
                    "project_id": "synapse",
                    "query": text,
                    "top_k": top_k,
                    "mode": mode
                }
            }
        },
        timeout=30
    )
    
    if response.status_code != 200:
        typer.echo(f"❌ Query failed: {response.status_code}")
        raise typer.Exit(1)
    
    # Parse SSE response
    result_text = ""
    for line in response.text.split('\n'):
        if line.startswith('data: ') and line[6:].strip():
            try:
                data = json.loads(line[6:])
                if 'result' in data:
                    result_text = data['result']['content'][0]['text']
                    break
            except:
                pass
    
    if format == "json":
        # Output as JSON
        try:
            result_json = json.loads(result_text)
            typer.echo(json.dumps(result_json, indent=2))
        except:
            typer.echo(result_text)
    else:
        # Output as text
        typer.echo(result_text)
```

**Files Modified**:
- `synapse/cli/commands/query.py`

---

### BUG-009: Missing Config Flags

**Problem**: Various flags not implemented  
**Approach**: Add missing options to config command

**Implementation**:
- Add `--env` flag to show environment variables
- Add `--path` flag to show config file path
- Add `--validate` flag to validate configuration
- Add `--reset` flag to reset to defaults

---

### BUG-INGEST-01: Ingestion Persistence

**Problem**: Completes but data not persisted  
**Approach**: Fix bulk_ingest script storage commit

**Investigation Steps**:

1. **Check storage backend**:
   - Identify if using ChromaDB, FAISS, or custom
   - Find persist/commit calls
   - Verify they're being called

2. **Fix approach**:
   ```python
   # In scripts/bulk_ingest.py
   
   # Add explicit persist after ingestion
   if hasattr(self.collection, 'persist'):
       self.collection.persist()
   elif hasattr(self.vectorstore, 'persist'):
       self.vectorstore.persist()
   elif hasattr(self, 'save_index'):
       self.save_index()
   
   # Verify persistence
   verify_count = self.get_source_count()
   if verify_count == 0:
       raise Exception("Data not persisted successfully!")
   ```

3. **Add verification**:
   ```python
   def verify_persistence(self):
       """Verify data was persisted."""
       count = self.get_source_count()
       if count == 0:
           logger.error("No sources found after ingestion!")
           return False
       logger.info(f"Verified {count} sources persisted")
       return True
   ```

**Files Modified**:
- `scripts/bulk_ingest.py`

**Tests**:
- Test data persists after bulk_ingest
- Test data survives server restart
- Test verification function

---

## 🧪 Testing Strategy

### Pytest Tests (80%+ coverage)

**New Test Files**:
- `tests/unit/test_cli_config.py` (8 tests)
- `tests/unit/test_cli_models.py` (6 tests)
- `tests/unit/test_cli_ingest.py` (10 tests)
- `tests/unit/test_cli_query.py` (10 tests)
- `tests/unit/test_bulk_ingest_persistence.py` (12 tests)

**Test Categories**:
- Unit tests for each CLI command
- Integration tests for MCP tool calls
- Persistence tests for bulk_ingest
- Error handling tests
- Performance tests (optional)

### Manual Testing

**Test Scenarios**:
- CLI command help text
- JSON output format
- Model list completeness
- File ingestion (single/directory)
- Query execution
- Ingestion persistence
- Error scenarios
- Performance benchmarks

---

## 📁 File Modifications Summary

| File | Changes | Phase |
|------|---------|-------|
| `synapse/cli/commands/config.py` | Add JSON output, fix formatting | 1 |
| `synapse/cli/commands/models.py` | Fix model detection | 2 |
| `synapse/cli/commands/ingest.py` | Implement full command | 3 |
| `synapse/cli/commands/query.py` | Implement full command | 4 |
| `scripts/bulk_ingest.py` | Fix persistence | 5 |
| `tests/unit/test_cli_config.py` | New test file | 6 |
| `tests/unit/test_cli_models.py` | New test file | 6 |
| `tests/unit/test_cli_ingest.py` | New test file | 6 |
| `tests/unit/test_cli_query.py` | New test file | 6 |
| `tests/unit/test_bulk_ingest_persistence.py` | New test file | 6 |

---

## ⚠️ Risks and Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| MCP server unavailable | HIGH | LOW | Add error handling, check server status |
| bulk_ingest complexity | MEDIUM | MEDIUM | Add logging, test incrementally |
| Performance degradation | LOW | LOW | Benchmark before/after |
| Test environment issues | MEDIUM | LOW | Use mocks for unit tests |

---

## 🔧 Configuration Changes

**No major configuration changes required**

- Existing config structure remains
- New CLI flags added with defaults
- Environment variable support maintained

---

## 📊 Success Criteria Verification

| Criterion | Method | Target |
|-----------|--------|--------|
| JSON output valid | Validate with jq | 100% |
| Models list complete | Manual count | All models |
| Ingest works | Manual test | 100% success |
| Query works | Manual test | Returns results |
| Persistence works | list_sources | > 50 sources |
| Pytest coverage | pytest --cov | 80%+ |
| Test pass rate | pytest | 100% |

---

## 🚀 Deployment Plan

1. **Create feature branch**: `feature/012-cli-ingestion-bug-fixes`
2. **Implement fixes**: One phase at a time
3. **Write tests**: After each fix
4. **Test thoroughly**: pytest + manual
5. **Create PR**: When all tests pass
6. **Merge**: After review

---

## 📝 References

- **Feature 010**: Fresh Installation Validation (bug reports)
- **Feature 011**: Validation Blocker Fixes (CLI framework)
- **AGENTS.md**: SDD protocol
- **Existing tests**: `tests/unit/test_cli_*.py`

---

**Created**: January 31, 2026  
**Status**: Ready for Implementation  
**Next**: Create tasks.md
