# Upgrading from pi-rag to SYNAPSE v1.0.0

## Overview

This guide helps you upgrade from old **pi-rag** naming to new **SYNAPSE v1.0.0** branding.

## Breaking Changes

### Project ID Change

- **Old**: `project_id="pi-rag"`
- **New**: `project_id="synapse"`
- **Impact**: All MCP tool calls must use new project ID

### Directory Path Change

- **Old**: `/opt/pi-rag/data`
- **New**: `/opt/synapse/data`
- **Impact**: Config files and scripts reference new path
- **Compatibility**: Symlink `/opt/synapse` → `/opt/pi-rag` ensures both paths work

### Container Changes

- **Image**: `synapse:v2.0.0` (new tag, same image ID as v1.0.0)
- **Container Name**: `synapse-mcp` (same, will replace v1)
- **Hostname**: `synapse` (changed from `pi-rag`)

---

## Steps to Upgrade

### 1. Backup Data (Optional but Recommended)

```bash
# Backup existing databases
sudo tar -czf synapse-backup-$(date +%Y%m%d).tar.gz /opt/pi-rag/data/
```

### 2. Stop Old Container

```bash
# Stop v1 container
docker stop synapse-mcp

# Verify stopped
docker ps | grep synapse-mcp
# Should show nothing (container in Exited state)
```

### 3. Update Your Code

If you have custom code or configurations that reference `pi-rag`:

- Update `project_id` from `"pi-rag"` to `"synapse"`
- Update paths from `/opt/pi-rag/data` to `/opt/synapse/data`
- Update documentation to reference new naming

### 4. Start New Container

```bash
cd /home/dietpi/synapse

# Start v2 container
docker compose -f docker-compose.synapse.yml up -d

# Wait for health check
sleep 5

# Verify
docker ps | grep synapse-mcp
curl -s http://localhost:8002/health
```

### 5. Update opencode Configuration

File: `~/.opencode/system_prompt.md`

Your system prompt already uses `"synapse"` project IDs and `/opt/synapse/data` paths.

No changes needed.

### 6. Test MCP Tools

```bash
# Test with new project_id
curl -X POST http://localhost:8002/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "rag.get_context",
      "arguments": {
        "project_id": "synapse",
        "context_type": "all",
        "query": "test",
        "max_results": 5
      }
    }
  }'
```

### 7. Update Databases

The v2 container will initialize fresh databases. If you need to migrate data:

**Option A: Manual Export/Import**
```bash
# Export from v1 container (if still accessible)
docker exec synapse-mcp python3 << 'EOF'
import sqlite3

conn = sqlite3.connect('/app/data/episodic.db')
cursor = conn.cursor()

# Export episodes
cursor.execute("SELECT * FROM episodic_memory WHERE project_id='pi-rag'")
episodes = cursor.fetchall()

conn.close()

# Save to file
import json
with open('episodes_backup.json', 'w') as f:
    json.dump(episodes, f, indent=2)

print("Exported", len(episodes), "episodes")
EOF
```

**Option B: Re-learn**
Let the system relearn from interactions using the new `"synapse"` project ID.

---

## Rollback Procedure

If you encounter issues after upgrade:

### 1. Stop New Container

```bash
docker compose -f docker-compose.synapse.yml down

# Or
docker stop synapse-mcp
```

### 2. Start Old Container

```bash
docker start <old_container_id>

# Or start v1 image with different tag
docker run -d --name synapse-mcp-v1 \
  -v synapse-data:/app/data \
  -v synapse-models:/app/models \
  -v /home/dietpi/synapse/configs:/app/configs:ro \
  -p 8002:8002 \
  synapse:v1.0.0-pi-rag
```

### 3. Reset Code (Git)

```bash
cd /home/dietpi/synapse

# Reset to v1 tag
git reset --hard v1.0.0-pi-rag

# Or reset to commit before changes
git reset --hard <commit_hash_before_upgrade>
```

### 4. Revert Configuration

If you updated any config files manually:
```bash
# Remove new config
rm /home/dietpi/synapse/configs/rag_config_synapse.json

# Restore from backup if you made one
# cp backup/rag_config.json /home/dietpi/synapse/configs/
```

---

## Verification

After upgrade, verify:

- [ ] Health check passing: `curl -s http://localhost:8002/health`
- [ ] Container hostname is `synapse`: `docker inspect synapse-mcp | grep Hostname`
- [ ] MCP tools working with `project_id="synapse"`
- [ ] Data directory `/opt/synapse/data` is accessible via symlink
- [ ] Logs show no errors: `docker logs synapse-mcp | grep -i error`

---

## Support

If you encounter issues:

1. **Check Logs**: `docker logs synapse-mcp`
2. **Review Changes**: Compare with v1 behavior
3. **Consult Documentation**: See `CHANGELOG.md` for all changes
4. **Open Issue**: Report bugs at https://github.com/kayis-rahman/synapse/issues

---

## Migration Checklist

Before considering upgrade complete, verify:

- [ ] All MCP tools tested with `project_id="synapse"`
- [ ] No errors in container logs
- [ ] Health endpoint returns status "ok"
- [ ] opencode interactions work correctly
- [ ] Backups tested and verified
- [ ] Rollback procedure documented and tested
