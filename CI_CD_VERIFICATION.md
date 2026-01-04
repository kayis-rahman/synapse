# Multi-Platform CI/CD Testing Guide

This guide explains how to verify multi-platform Docker builds work correctly for SYNAPSE.

## Overview

SYNAPSE uses GitHub Actions to build and publish multi-platform Docker images to Docker Hub.

**Supported Platforms:**
- `linux/amd64` - Standard x86_64 architecture (Intel/AMD)
- `linux/arm64` - ARM 64-bit architecture (Apple Silicon, Raspberry Pi, etc.)

---

## CI/CD Workflow

### GitHub Actions Workflow: `.github/workflows/publish-docker.yml`

**Triggers:**
- Git tags matching `v*` pattern (e.g., `v1.0.0`)
- Pushes to `main` branch
- Manual workflow dispatch

**Key Features:**
- Uses `docker/setup-buildx-action@v3` for multi-platform builds
- Builds both `linux/amd64` and `linux/arm64` in parallel
- Pushes multi-arch manifest to Docker Hub
- Caches layers for faster builds

**Workflow Steps:**
1. Checkout code
2. Set up Docker Buildx
3. Login to Docker Hub (uses secrets)
4. Extract metadata (tags, labels)
5. Build and push multi-platform images
6. Create manifest for both platforms

---

## Verification Steps

### Step 1: Check Workflow Status

**URL:** https://github.com/kayis-rahman/synapse/actions

**Look for:**
- Workflow run for tag `v1.0.0`
- Green checkmark (success) or red X (failure)
- Job name: `build-and-push`

**What to verify:**
- [ ] Workflow completed successfully
- [ ] Both platforms built
- [ ] No errors in logs
- [ ] Images pushed to Docker Hub

---

### Step 2: Verify Multi-Platform Images on Docker Hub

**URL:** https://hub.docker.com/repository/docker/kayisrahman/synapse/tags

**What to look for:**
- Multiple tags with platform identifiers (e.g., `v1.0.0-amd64`, `v1.0.0-arm64`)
- OR single tag with multi-arch manifest
- Manifest info showing both platforms

**Example of correct state:**
```
TAG         SIZE      LAST UPDATED  MANIFESTS
v1.0.0      523MB     2 hours ago   linux/amd64, linux/arm64
```

---

### Step 3: Test Local Pull on Each Platform

#### Test AMD64 Platform

```bash
# Pull AMD64 image explicitly
docker pull --platform linux/amd64 kayisrahman/synapse:v1.0.0

# Verify platform
docker inspect kayisrahman/synapse:v1.0.0 | grep Architecture
# Should show: "Architecture": "amd64"
```

#### Test ARM64 Platform

```bash
# Pull ARM64 image explicitly
docker pull --platform linux/arm64 kayisrahman/synapse:v1.0.0

# Verify platform
docker inspect kayisrahman/synapse:v1.0.0 | grep Architecture
# Should show: "Architecture": "arm64"
```

#### Test Automatic Platform Selection

```bash
# Pull without platform (Docker should auto-select)
docker pull kayisrahman/synapse:v1.0.0

# Verify it's a multi-arch manifest
docker manifest inspect kayisrahman/synapse:v1.0.0

# Should show:
# {
#   "schemaVersion": 2,
#   "mediaType": "application/vnd.docker.distribution.manifest.list.v2+json",
#   "manifests": [
#     {
#       "platform": {"architecture": "amd64", "os": "linux"},
#       ...
#     },
#     {
#       "platform": {"architecture": "arm64", "os": "linux"},
#       ...
#     }
#   ]
# }
```

---

### Step 4: Test Deployment on Each Platform

#### Deploy on AMD64 (Standard PC/Server)

```bash
# Use docker-compose with correct image
docker compose -f docker-compose.synapse.yml up -d

# Check container logs
docker compose -f docker-compose.synapse.yml logs -f

# Verify health check
curl http://localhost:8002/health

# Expected response:
# {
#   "status": "ok",
#   "data_directory": "/opt/synapse/data"
# }
```

#### Deploy on ARM64 (Raspberry Pi, Apple Silicon)

```bash
# Same command - Docker should auto-select ARM64 image
docker compose -f docker-compose.synapse.yml up -d

# Check that container started on ARM64
docker ps

# Verify health check
curl http://localhost:8002/health
```

---

## Troubleshooting

### Issue: Workflow Failed

**Check GitHub Actions logs:**
1. Go to: https://github.com/kayis-rahman/synapse/actions
2. Click on the failed workflow run
3. Expand each step to see error messages
4. Common issues:
   - Docker Hub authentication (check secrets)
   - Build errors (check Dockerfile syntax)
   - Timeout (increase workflow timeout if needed)

**Fix Docker Hub secrets:**
1. Go to: https://github.com/kayis-rahman/synapse/settings/secrets/actions
2. Add secrets:
   - `DOCKER_USERNAME`: Your Docker Hub username
   - `DOCKER_PASSWORD`: Your Docker Hub password/access token

---

### Issue: Only One Platform Built

**Symptoms:**
- Only `linux/amd64` or `linux/arm64` in Docker Hub
- Missing multi-arch manifest

**Fix:**
1. Check workflow `.github/workflows/publish-docker.yml`
2. Verify `platforms: linux/amd64,linux/arm64` is present
3. Check `push: true` is set in `docker/build-push-action`
4. Re-run workflow manually from GitHub Actions UI

---

### Issue: Image Pull Fails

**Error:** `no matching manifest for linux/arm64`

**Fix:**
1. Wait a few minutes after workflow completes
2. Docker Hub may be updating manifests
3. Try again after 5-10 minutes

---

## Expected Results

### Successful CI/CD Pipeline

**GitHub Actions:**
- ✅ Workflow triggered on tag push
- ✅ Build job completed successfully
- ✅ Both platforms built in parallel
- ✅ Images pushed to Docker Hub
- ✅ Multi-arch manifest created

**Docker Hub:**
- ✅ Tag `v1.0.0` exists
- ✅ Supports `linux/amd64` and `linux/arm64`
- ✅ Manifest includes both platforms

**Local Testing:**
- ✅ `docker pull` works without platform specification
- ✅ `docker pull --platform linux/amd64` pulls correct image
- ✅ `docker pull --platform linux/arm64` pulls correct image
- ✅ `docker compose up -d` starts container successfully
- ✅ Health check endpoint returns OK

---

## Quick Validation Checklist

- [ ] GitHub Actions workflow completed successfully
- [ ] Both platforms (amd64, arm64) built
- [ ] Images pushed to Docker Hub
- [ ] Docker Hub shows multi-arch manifest
- [ ] Can pull AMD64 image: `docker pull --platform linux/amd64`
- [ ] Can pull ARM64 image: `docker pull --platform linux/arm64`
- [ ] Can pull auto-platform: `docker pull kayisrahman/synapse:v1.0.0`
- [ ] Container starts successfully on both platforms
- [ ] Health check passes on both platforms

---

## Next Steps After Verification

### All Tests Pass:

1. **Close task**: `bd close synapse-xsd`
2. **Move to next task**: synapse-7bm (Update installation documentation)
3. **Update DOCKERHUB_SETUP.md** with verification results

### Tests Fail:

1. **Review GitHub Actions logs** for errors
2. **Fix issues** in workflow or Dockerfile
3. **Re-run workflow** manually
4. **Re-verify** all steps above

---

## Related Files

- `.github/workflows/publish-docker.yml` - CI/CD workflow
- `docker-compose.synapse.yml` - Local deployment configuration
- `scripts/test_docker_build.sh` - Local testing script
- `DOCKERHUB_SETUP.md` - Docker Hub setup guide

---

**Last Updated:** 2025-01-04
**Version:** 1.0.0
**Status:** Ready for verification
