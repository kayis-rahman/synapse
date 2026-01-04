# Docker Hub Setup Guide for SYNAPSE

This guide walks you through setting up Docker Hub for SYNAPSE v1.0.0.

## Overview

SYNAPSE uses GitHub Actions to automatically build and publish Docker images to Docker Hub when:
- You push a tag matching `v*` (e.g., `v1.0.0`, `v1.1.0`)
- You push to the `main` branch

Image: `docker.io/kayisrahman/synapse`
Platforms: `linux/amd64`, `linux/arm64`

---

## Prerequisites

Before starting, ensure you have:
- [ ] Docker Hub account (free)
- [ ] GitHub account (you have this)
- [ ] Docker Hub access token
- [ ] GitHub repository access (you have this)

---

## Step 1: Create Docker Hub Account

1. Go to https://hub.docker.com/
2. Click **"Sign Up"** (top right)
3. Choose **"Docker ID"** (this will be your username, e.g., `kayisrahman`)
4. Enter email and password
5. Verify email address
6. Log in to Docker Hub

**Your Docker Hub username**: This will be `kayisrahman` for the image `docker.io/kayisrahman/synapse`

---

## Step 2: Create Access Token

Access tokens are more secure than using your Docker Hub password.

### 2.1 Navigate to Access Tokens

1. Log in to Docker Hub: https://hub.docker.com/
2. Click your username (top right) → **"Account Settings"**
3. On left sidebar, click **"Security"**
4. Under "Access Tokens", click **"New Access Token"**

### 2.2 Create Token

1. **Access Token Description**: Enter a descriptive name
   - Example: `github-actions`
   - This helps you identify where the token is used

2. **Access Permissions**: Choose appropriate permissions
   - **Read & Write** (recommended for CI/CD)
   - This allows GitHub Actions to pull and push images

3. Click **"Generate"**

4. **Copy the access token** immediately
   - Format: `dckr_pat_<long-string>`
   - ⚠️ **IMPORTANT**: You won't see this token again!

5. Store the token securely (password manager, env file, etc.)

**Example token**: `dckr_pat_aBcDeFgHiJkLmNoPqRsTuVwXyZ-1234567890abcdef`

---

## Step 3: Add Secrets to GitHub

Now add your Docker Hub credentials to GitHub Actions.

### 3.1 Navigate to GitHub Repository Settings

1. Go to your repository: https://github.com/kayis-rahman/synapse
2. Click **"Settings"** tab (top)
3. On left sidebar, click **"Secrets and variables"** → **"Actions"**

### 3.2 Add Docker Hub Username Secret

1. Click **"New repository secret"**
2. **Name**: Enter `DOCKER_USERNAME`
   - This must match the workflow: `${{ secrets.DOCKER_USERNAME }}`
3. **Value**: Enter your Docker Hub username
   - Example: `kayisrahman`
4. Click **"Add secret"**

### 3.3 Add Docker Hub Password Secret

1. Click **"New repository secret"**
2. **Name**: Enter `DOCKER_PASSWORD`
   - This must match the workflow: `${{ secrets.DOCKER_PASSWORD }}`
3. **Value**: Enter your Docker Hub access token (from Step 2)
   - Example: `dckr_pat_aBcDeFgHiJkLmNoPqRsTuVwXyZ-1234567890abcdef`
4. Click **"Add secret"**

**Your secrets should now be**:
- `DOCKER_USERNAME`: `kayisrahman`
- `DOCKER_PASSWORD`: `dckr_pat_...` (your access token)

### 3.4 Verify Secrets

After adding, you should see both secrets listed:
```
DOCKER_USERNAME    Updated 2 minutes ago
DOCKER_PASSWORD    Updated 2 minutes ago
```

---

## Step 4: Create Docker Hub Repository

The GitHub Actions workflow will create the repository on first push, but you can create it manually.

### 4.1 Create Repository (Optional)

1. Go to Docker Hub: https://hub.docker.com/
2. Click **"Create"** → **"Repository"** (top right)
3. Fill in details:
   - **Name**: `synapse`
   - **Visibility**: Public (recommended) or Private
   - **Description**: `SYNAPSE - Your Data Meets Intelligence`
4. Click **"Create"**

**Repository URL**: https://hub.docker.com/repository/docker/kayisrahman/synapse/general

### 4.2 Configure Repository

After creating or after first build:

1. Go to repository settings: https://hub.docker.com/repository/docker/kayisrahman/synapse/general
2. **General Settings**:
   - **Description**: `Your Data Meets Intelligence`
   - **Full Description**: Copy from DOCKERHUB_README.md
   - **Visibility**: Public (recommended)
   - **Dockerfile**: Link to Dockerfile
   - **Git Repository**: `https://github.com/kayis-rahman/synapse`

3. **Labels** (optional):
   - Add tags: `rag`, `mcp`, `local-ai`, `neural-network`

---

## Step 5: Configure GitHub Actions Workflow

The workflow file is already created at `.github/workflows/publish-docker.yml`.

### 5.1 Verify Workflow

1. Go to: https://github.com/kayis-rahman/synapse/blob/main/.github/workflows/publish-docker.yml
2. Verify the workflow contains:
   - Docker Hub login step (uses `DOCKER_USERNAME` and `DOCKER_PASSWORD`)
   - Build step with platforms `linux/amd64,linux/arm64`
   - Push step to `docker.io/kayisrahman/synapse`

### 5.2 Workflow Triggers

The workflow is triggered by:
- Push tags matching `v*` (e.g., `v1.0.0`, `v1.1.0`)
- Push to `main` branch
- Manual trigger (workflow_dispatch)

---

## Step 6: Trigger First Build

Now trigger the first build to verify everything works.

### Option A: Push a Tag (Recommended)

```bash
# Tag current commit as v1.0.0
git tag v1.0.0

# Push tag to GitHub
git push origin v1.0.0

# Or push all tags
git push --tags
```

This will trigger the GitHub Actions workflow to build and push the image.

### Option B: Push to Main Branch

```bash
# Push to main branch
git push origin main
```

This will also trigger the workflow.

### Option C: Manual Trigger

1. Go to: https://github.com/kayis-rahman/synapse/actions
2. Click **"Publish Docker Image"** workflow
3. Click **"Run workflow"**
4. Select branch: `main`
5. Click **"Run workflow"** button

---

## Step 7: Monitor Build

After triggering, monitor the build progress.

### 7.1 Check GitHub Actions

1. Go to: https://github.com/kayis-rahman/synapse/actions
2. Click the running workflow: **"Publish Docker Image"**
3. View logs in real-time

Expected steps:
- Checkout code
- Set up Docker Buildx
- Login to Docker Hub
- Extract metadata
- Build and push (multi-platform)
  - Build for linux/amd64
  - Build for linux/arm64
  - Push to Docker Hub

**Expected build time**: 10-20 minutes (multi-platform)

### 7.2 Check Docker Hub

After build completes (green checkmark in GitHub Actions):

1. Go to: https://hub.docker.com/repository/docker/kayisrahman/synapse/general
2. Check **"Tags"** tab
3. You should see:
   - `1.0.0`
   - `latest`

---

## Step 8: Verify Deployment

Test that the image is available and works.

### 8.1 Pull Image

```bash
# Pull specific version
docker pull docker.io/kayisrahman/synapse:1.0.0

# Pull latest
docker pull docker.io/kayisrahman/synapse:latest
```

### 8.2 Test Run

```bash
# Test run (quick start)
docker run --rm -p 8002:8002 \
  docker.io/kayisrahman/synapse:1.0.0 \
  python -c "from rag import MemoryStore; print('✅ SYNAPSE OK')"
```

Expected output:
```
✅ SYNAPSE OK
```

### 8.3 Full Deployment

```bash
# Full deployment with Docker Compose
docker compose -f docker-compose.mcp.yml up -d

# Or with docker run
docker run -d --name synapse-mcp \
  -p 8002:8002 \
  -v synapse-data:/app/data \
  -v synapse-models:/app/models \
  docker.io/kayisrahman/synapse:1.0.0
```

### 8.4 Verify Health

```bash
# Health check
curl http://localhost:8002/health

# Expected response
{"status": "ok", "service": "synapse"}
```

---

## Troubleshooting

### Workflow Fails with "Invalid Credentials"

**Error**: `Error: unauthorized: incorrect username or password`

**Solution**:
1. Verify `DOCKER_USERNAME` is correct (Docker Hub username, not email)
2. Verify `DOCKER_PASSWORD` is your access token, not your password
3. Regenerate access token if needed

### Workflow Fails with "Permission Denied"

**Error**: `Error: insufficient permissions`

**Solution**:
1. Ensure access token has "Read & Write" permissions
2. Ensure you're pushing to correct repository
3. Check repository visibility (public vs private)

### Build Fails on One Platform

**Error**: Build fails on `linux/arm64` or `linux/amd64`

**Solution**:
1. Check GitHub Actions logs for specific error
2. Verify Dockerfile is compatible with both platforms
3. Test locally: `docker buildx build --platform linux/arm64 .`

### Image Not Found After Build

**Issue**: Docker Hub shows image but can't pull

**Solution**:
1. Wait a few minutes for Docker Hub to propagate
2. Verify image name: `docker.io/kayisrahman/synapse`
3. Try pulling again: `docker pull docker.io/kayisrahman/synapse:1.0.0`

### Multi-Platform Not Working

**Issue**: Only one platform is built

**Solution**:
1. Verify workflow has `platforms: linux/amd64,linux/arm64`
2. Check Dockerfile doesn't have platform-specific code
3. Verify GitHub Actions runner supports multi-platform builds

---

## Security Best Practices

### Access Token Rotation

Rotate your access token regularly (every 90 days):

1. Go to Docker Hub → Security → Access Tokens
2. Click "..." on existing token → "Revoke"
3. Create new access token
4. Update GitHub secret `DOCKER_PASSWORD`
5. Test workflow

### Use Read-Only for Pull-Only Workflows

If you only need to pull images (not push), use read-only token:

1. Create access token with "Read only" permission
2. Use in other workflows or local Docker setup

### Restrict Workflow Permissions

The workflow file already has minimal permissions:
```yaml
permissions:
  contents: read
  packages: write
```

Don't add unnecessary permissions.

---

## Next Steps

After successful setup:

1. ✅ Docker Hub configured
2. ✅ GitHub Actions secrets added
3. ✅ First image pushed successfully
4. ✅ Verified deployment works

**Next steps**:
- 📖 Read [DOCKER_INSTALLATION.md](DOCKER_INSTALLATION.md) for usage guide
- 🚀 Deploy to production: `docker compose -f docker-compose.mcp.yml up -d`
- 🔧 Configure environment: Edit `.env.docker`
- 📝 Create documentation: [DOCKERHUB_README.md](DOCKERHUB_README.md)

---

## Reference

- **Docker Hub Repository**: https://hub.docker.com/repository/docker/kayisrahman/synapse/general
- **GitHub Actions**: https://github.com/kayis-rahman/synapse/actions
- **Docker Hub Documentation**: https://docs.docker.com/docker-hub/
- **GitHub Actions Documentation**: https://docs.github.com/en/actions

---

## Support

- **Issues**: [GitHub Issues](https://github.com/kayis-rahman/synapse/issues)
- **Discussions**: [GitHub Discussions](https://github.com/kayis-rahman/synapse/discussions)
- **Docker Hub Support**: https://www.docker.com/company/contact/
