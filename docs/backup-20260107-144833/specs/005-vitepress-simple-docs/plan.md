# VitePress Simple Documentation - Technical Plan

**Feature ID**: 005-vitepress-simple-docs
**Status**: [In Progress]
**Created**: January 7, 2026
**Last Updated**: January 7, 2026

---

## Executive Summary

This plan details the technical implementation for restructuring SYNAPSE documentation from a mixed Fumadocs/VitePress system to a clean, single VitePress-based system.

**Goal**: Clean 3-directory structure (`app/`, `specs/`, `md/`) with 16+ documentation pages.

**Approach**: Incremental migration with validation at each phase.

---

## Technical Architecture

### Current State (Before)

```
docs/
├── .gitignore                          ❌ DELETE
├── FUMADOCS_IMPLEMENTATION_SUMMARY.md    ❌ DELETE
├── next-env.d.ts                       ❌ DELETE
├── next.config.mjs                     ❌ DELETE
├── package.json                        ❌ DELETE (Fumadocs)
├── package-lock.json                   ❌ DELETE (Fumadocs)
├── README.md                          ❌ DELETE
├── source.config.ts                    ❌ DELETE
├── tsconfig.json                      ❌ DELETE
├── troubleshooting-auto-learning.md     ❌ DELETE
├── archive/                           ❌ DELETE (124K)
├── api/                              ❌ DELETE (empty)
├── getting-started/                    ❌ DELETE (empty)
├── specs/                            ✅ KEEP (424K)
├── app/
│   ├── .vitepress/                   ✅ KEEP (VitePress)
│   ├── [lang]/                       ❌ DELETE (Next.js i18n)
│   ├── globals.css                    ❌ DELETE (Next.js)
│   ├── layout.tsx                    ❌ DELETE (Next.js)
│   ├── page.tsx                      ❌ DELETE (Next.js)
│   ├── package.json                   ✅ KEEP (VitePress)
│   ├── package-lock.json              ✅ KEEP (VitePress)
│   └── node_modules/                ✅ KEEP (VitePress)
├── content/
│   └── docs/                        ⚠️ MIGRATE (16 MDX files)
│       ├── getting-started/           → md/getting-started/
│       ├── architecture/              → md/architecture/
│       ├── usage/                    → md/usage/
│       ├── api-reference/             → md/api-reference/
│       └── development/              → md/development/
└── docs/
    └── docs/                        ⚠️ MIGRATE (4 MD files)
        └── api/
            └── cli-commands/         → md/api/cli-commands/
```

### Target State (After)

```
docs/
├── app/                             # VitePress engine only
│   ├── .vitepress/
│   │   ├── config.mts               [UPDATED]
│   │   └── cache/
│   ├── package.json
│   ├── package-lock.json
│   └── node_modules/
│
├── specs/                           # SDD specifications
│   ├── index.md
│   ├── 001-comprehensive-test-suite/
│   ├── 002-auto-learning/
│   ├── 003-rag-quality-metrics/
│   ├── 004-universal-hook-auto-learning/
│   └── 005-vitepress-simple-docs/
│       ├── requirements.md
│       ├── plan.md
│       └── tasks.md
│
└── md/                              # All documentation content
    ├── index.md                      [NEW] Home page
    ├── .vitepress/
    │   └── public/                   [NEW] Static assets
    ├── getting-started/
    │   ├── introduction.md            [CONVERTED]
    │   ├── installation.md            [CONVERTED]
    │   ├── quick-start.md            [CONVERTED]
    │   └── configuration.md          [CONVERTED]
    ├── architecture/
    │   ├── overview.md               [CONVERTED]
    │   ├── memory-system.md          [CONVERTED]
    │   └── mcp-protocol.md          [CONVERTED]
    ├── usage/
    │   ├── mcp-tools.md             [CONVERTED]
    │   ├── ingestion.md             [CONVERTED]
    │   └── querying.md             [CONVERTED]
    ├── api-reference/
    │   ├── memory-tools.md          [CONVERTED]
    │   ├── server-api.md            [CONVERTED]
    │   └── cli-commands.md         [CONVERTED]
    └── development/
        ├── contributing.md           [CONVERTED]
        ├── testing.md              [CONVERTED]
        └── deployment.md           [CONVERTED]
```

---

## Technology Stack

### Documentation Framework
- **VitePress 1.6.4**: Static site generator
- **Vue 3.4.0**: Framework
- **TypeScript 5.3.0**: Configuration language

### Content Format
- **Markdown**: Standard markdown (no MDX)
- **Frontmatter**: YAML metadata for page configuration
- **Code Blocks**: Syntax highlighting (Python, bash, JSON, TypeScript)

### Build System
- **Vite 5**: Build tool
- **Static Generation**: All pages pre-rendered
- **Zero JavaScript Runtime**: No build-time dependencies

---

## Implementation Phases

### Phase 1: Preparation & Backup (30 minutes)

**Objective**: Safe backup and preparation for restructuring.

**Tasks:**
1. Create backup of entire `/docs/` directory
2. Verify backup integrity
3. Create new directory structure skeleton
4. Identify all files to be deleted

**Risk Mitigation:**
- Backup stored at `/docs/backup-[timestamp]/`
- No deletions until backup verified

**Validation:**
- Backup exists and is complete
- Skeleton directories created

---

### Phase 2: Content Migration (2 hours)

**Objective**: Convert and migrate 16 MDX files to markdown format.

**Tasks:**

#### 2.1 Convert MDX Files (1.5 hours)
For each MDX file:
1. Read source file from `/docs/content/docs/`
2. Remove MDX-specific syntax:
   - Remove import statements
   - Remove component usage (e.g., `<Callout>`, `<TabGroup>`)
   - Convert custom components to standard markdown
   - Remove JSX/TSX syntax
3. Convert `.mdx` extension to `.md`
4. Write to `/docs/md/` target directory
5. Verify markdown syntax

**Conversion Rules:**

| MDX Element | Markdown Equivalent |
|-------------|-------------------|
| `<Callout type="info">` | `> **Info:**` |
| `<Callout type="warning">` | `> ⚠️ **Warning:**` |
| `<Callout type="error">` | `> ❌ **Error:**` |
| `<TabGroup>` | Subsection headers |
| `<Tab>` | Subsection content |
| `<CodeBlock>` | Standard code block with language |
| `<Link to="/path">` | Standard markdown link `[text](/path)` |
| `import { Component } from 'lib'` | Delete (no imports) |
| `export default function Page()` | Delete (no components) |

**Files to Convert:**

**Getting Started (4 files):**
- `introduction.mdx` → `getting-started/introduction.md`
- `installation.mdx` → `getting-started/installation.md`
- `quick-start.mdx` → `getting-started/quick-start.md`
- `configuration.mdx` → `getting-started/configuration.md`

**Architecture (3 files):**
- `overview.mdx` → `architecture/overview.md`
- `memory-system.mdx` → `architecture/memory-system.md`
- `mcp-protocol.mdx` → `architecture/mcp-protocol.md`

**Usage (3 files):**
- `mcp-tools.mdx` → `usage/mcp-tools.md`
- `ingestion.mdx` → `usage/ingestion.md`
- `querying.mdx` → `usage/querying.md`

**API Reference (3 files):**
- `memory-tools.mdx` → `api-reference/memory-tools.md`
- `server-api.mdx` → `api-reference/server-api.md`
- `cli-commands.mdx` → `api-reference/cli-commands.md`

**Development (3 files):**
- `contributing.mdx` → `development/contributing.md`
- `testing.mdx` → `development/testing.md`
- `deployment.mdx` → `development/deployment.md`

#### 2.2 Migrate CLI Documentation (30 minutes)
1. Read 4 MD files from `/docs/docs/docs/api/cli-commands/`
2. Merge into single `api-reference/cli-commands.md`
3. Update internal links to new paths
4. Delete source files

**Files to Migrate:**
- `complete-reference.md`
- `mcp-server.md`
- `query.md`
- `index.md`

**Validation:**
- All 16 files converted
- Markdown syntax valid
- No MDX-specific syntax remaining

---

### Phase 3: VitePress Configuration (45 minutes)

**Objective**: Configure VitePress for new structure.

**Tasks:**

#### 3.1 Update Config File
Edit `/docs/app/.vitepress/config.mts`:

```typescript
import { defineConfig } from 'vitepress'

export default defineConfig({
  // Point to md/ directory
  srcDir: '../md',

  // Site metadata
  title: 'SYNAPSE',
  description: 'Your Data Meets Intelligence - Local-first RAG system',

  // Theme configuration
  themeConfig: {
    // Top navigation
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Getting Started', link: '/getting-started/introduction' },
      { text: 'Architecture', link: '/architecture/overview' },
      { text: 'Usage', link: '/usage/mcp-tools' },
      { text: 'API Reference', link: '/api-reference/memory-tools' },
      { text: 'Development', link: '/development/contributing' }
    ],

    // Sidebar navigation
    sidebar: [
      {
        text: 'Getting Started',
        items: [
          { text: 'Introduction', link: '/getting-started/introduction' },
          { text: 'Installation', link: '/getting-started/installation' },
          { text: 'Quick Start', link: '/getting-started/quick-start' },
          { text: 'Configuration', link: '/getting-started/configuration' }
        ]
      },
      {
        text: 'Architecture',
        items: [
          { text: 'Overview', link: '/architecture/overview' },
          { text: 'Memory System', link: '/architecture/memory-system' },
          { text: 'MCP Protocol', link: '/architecture/mcp-protocol' }
        ]
      },
      {
        text: 'Usage',
        items: [
          { text: 'MCP Tools', link: '/usage/mcp-tools' },
          { text: 'Ingestion', link: '/usage/ingestion' },
          { text: 'Querying', link: '/usage/querying' }
        ]
      },
      {
        text: 'API Reference',
        items: [
          { text: 'Memory Tools', link: '/api-reference/memory-tools' },
          { text: 'Server API', link: '/api-reference/server-api' },
          { text: 'CLI Commands', link: '/api-reference/cli-commands' }
        ]
      },
      {
        text: 'Development',
        items: [
          { text: 'Contributing', link: '/development/contributing' },
          { text: 'Testing', link: '/development/testing' },
          { text: 'Deployment', link: '/development/deployment' }
        ]
      }
    ],

    // Social links
    socialLinks: [
      { icon: 'github', link: 'https://github.com/kayis-rahman/synapse' }
    ],

    // Footer
    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright © 2026 SYNAPSE'
    }
  }
})
```

#### 3.2 Create Home Page
Create `/docs/md/index.md`:

```markdown
---
layout: home
hero:
  name: SYNAPSE
  text: Your Data Meets Intelligence
  tagline: Local-first RAG system for intelligent knowledge management
  actions:
    - theme: brand
      text: Get Started
      link: /getting-started/introduction
    - theme: alt
      text: Quick Start
      link: /getting-started/quick-start

features:
  - title: Neural Storage
    details: Three-tier memory system (symbolic, episodic, semantic) with authority hierarchy
  - title: Synaptic Transmission
    details: MCP protocol for seamless integration with AI agents
  - title: Local-First
    details: All data stored locally with optional remote ingestion
  - title: Auto-Learning
    details: Automatic extraction and storage of knowledge from interactions
  - title: Flexible Querying
    details: Query expansion, memory selection, and context injection
  - title: Production Ready
    details: HTTP server, CLI tools, and comprehensive API
---

<script setup>
import { onMounted } from 'vue'

onMounted(() => {
  console.log('SYNAPSE Documentation Loaded')
})
</script>
```

#### 3.3 Update Package Scripts
Edit `/docs/app/package.json`:

```json
{
  "name": "synapse-docs",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "docs:dev": "vitepress dev",
    "docs:build": "vitepress build",
    "docs:preview": "vitepress preview"
  },
  "devDependencies": {
    "vitepress": "^1.6.4",
    "vue": "^3.4.0",
    "typescript": "^5.3.0"
  }
}
```

**Validation:**
- Config file updated
- Home page created
- Scripts updated

---

### Phase 4: Cleanup (1 hour)

**Objective**: Remove Fumadocs, Next.js, and debris files.

**Tasks:**

#### 4.1 Delete Root-Level Files
Delete from `/docs/`:
- `.gitignore`
- `FUMADOCS_IMPLEMENTATION_SUMMARY.md`
- `next-env.d.ts`
- `next.config.mjs`
- `package.json` (Fumadocs version)
- `package-lock.json` (Fumadocs version)
- `README.md`
- `source.config.ts`
- `tsconfig.json`
- `troubleshooting-auto-learning.md`

#### 4.2 Delete Empty/Unused Directories
Delete from `/docs/`:
- `archive/` (124K)
- `api/` (empty)
- `getting-started/` (empty)
- `docs/` (16K - after content migration)

#### 4.3 Clean `/docs/app/` Directory
Delete from `/docs/app/`:
- `[lang]/` (Next.js i18n)
- `layout.tsx` (Next.js)
- `page.tsx` (Next.js)
- `globals.css` (Next.js)

#### 4.4 Delete Fumadocs Content
Delete from `/docs/`:
- `content/` (68K - after content migration)

**Validation:**
- `/docs/` contains only `app/`, `specs/`, `md/`
- No root-level files or directories
- Backup verified before deletion

---

### Phase 5: Validation & Testing (1 hour)

**Objective**: Verify everything works correctly.

**Tasks:**

#### 5.1 Install Dependencies
```bash
cd docs/app
npm install
```

#### 5.2 Run Dev Server
```bash
npm run docs:dev
```
**Verify:**
- Server starts on `http://localhost:5173`
- Home page loads correctly
- No console errors
- Navigation works

#### 5.3 Test Navigation
**Verify:**
- All 16 pages accessible via nav
- Sidebar navigation works
- Internal links work
- No 404 errors

#### 5.4 Test Search
**Verify:**
- Search bar visible
- ⌘K keyboard shortcut works
- Search returns results
- Results highlight terms

#### 5.5 Build Production
```bash
npm run docs:build
```
**Verify:**
- Build completes successfully
- Build time < 2 minutes
- Output in `.vitepress/dist/`
- No build errors or warnings

#### 5.6 Preview Production Build
```bash
npm run docs:preview
```
**Verify:**
- Preview works on localhost:4173
- All pages accessible
- Navigation works
- No console errors

#### 5.7 Link Validation
**Verify:**
- All internal links work
- No broken links
- Cross-references correct
- "See Also" sections link properly

**Validation:**
- Dev server works
- Build succeeds
- All pages accessible
- No broken links
- Performance targets met

---

### Phase 6: Documentation (30 minutes)

**Objective**: Update spec index and create completion summary.

**Tasks:**

#### 6.1 Update Spec Index
Edit `/docs/specs/index.md`:

Add entry:
```markdown
| 005-vitepress-simple-docs | VitePress Simple Documentation | [In Progress] | ⏳ Pending |
```

#### 6.2 Create Completion Summary
Create `/docs/specs/005-vitepress-simple-docs/COMPLETION-SUMMARY.md`:
- Document what was completed
- List all files created
- Document file deletions
- Summary of changes
- Known limitations
- Future work

#### 6.3 Create Tasks.md
Create `/docs/specs/005-vitepress-simple-docs/tasks.md`:
- Break down into atomic tasks
- Link tasks to requirements
- Mark completed tasks

**Validation:**
- Index updated
- Completion summary created
- Tasks.md created

---

## Data Schema

### File Structure Schema

```typescript
interface DocumentationFile {
  path: string;
  frontmatter: {
    title: string;
    description?: string;
    layout?: string;
  };
  content: string;
}
```

### Navigation Schema

```typescript
interface NavigationItem {
  text: string;
  link?: string;
  items?: NavigationItem[];
  collapsed?: boolean;
}
```

### Directory Structure Schema

```
docs/
├── app/           { type: "vitepress-engine" }
├── specs/         { type: "sdd-specifications" }
└── md/            { type: "documentation-content" }
    ├── index.md    { type: "home-page" }
    ├── getting-started/  { type: "section" }
    ├── architecture/      { type: "section" }
    ├── usage/            { type: "section" }
    ├── api-reference/     { type: "section" }
    └── development/      { type: "section" }
```

---

## Risk Mitigation

### Risk: Data Loss During Cleanup
**Mitigation Strategy:**
1. Create backup at `/docs/backup-[timestamp]/`
2. Verify backup integrity before deletions
3. Delete only after content verified in new location
4. Keep backup for 24 hours after completion

### Risk: Broken Internal Links
**Mitigation Strategy:**
1. Document all link patterns before conversion
2. Use search-and-replace for known patterns
3. Manually verify all internal links
4. Test navigation after each batch of conversions

### Risk: Build Configuration Issues
**Mitigation Strategy:**
1. Test build incrementally (10 files at a time)
2. Start with minimal config, add complexity gradually
3. Verify config with small subset first
4. Document all configuration changes

### Risk: MDX Conversion Issues
**Mitigation Strategy:**
1. Keep original MDX files until conversion verified
2. Manually review each converted file
3. Test markdown syntax validity
4. Preserve content structure and formatting

---

## Performance Optimization

### Build Performance Targets
- **Build time**: < 2 minutes
- **Bundle size**: < 500KB (gzipped)
- **Page load time**: < 2 seconds

### Optimization Techniques
1. **Static Generation**: All pages pre-rendered
2. **Lazy Loading**: Code splitting for navigation
3. **Image Optimization**: WebP format, responsive sizes (if images added)
4. **CSS Optimization**: Minified, critical CSS inline
5. **JavaScript Minimal**: No runtime dependencies

### Monitoring
- Measure build time
- Monitor bundle size
- Test page load times
- Validate with Lighthouse (optional)

---

## Deployment Strategy

### Local Deployment (Phase 5)
- Dev server: `npm run docs:dev` (localhost:5173)
- Build: `npm run docs:build`
- Preview: `npm run docs:preview` (localhost:4173)

### GitHub Pages Deployment (Future Work)
**Configuration:**
```yaml
# .github/workflows/deploy-docs.yml
name: Deploy VitePress Docs
on:
  push:
    branches: [main]
    paths:
      - 'docs/**'
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - name: Install Dependencies
        run: |
          cd docs/app
          npm install
      - name: Build Docs
        run: |
          cd docs/app
          npm run docs:build
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs/app/.vitepress/dist
```

**Base Path Configuration:**
```typescript
// docs/app/.vitepress/config.mts
export default defineConfig({
  base: '/synapse/docs/',
  // ... rest of config
})
```

---

## Testing Strategy

### Unit Tests
- Markdown syntax validation
- Frontmatter validation
- Link validation

### Integration Tests
- Build succeeds
- Dev server starts
- Navigation works
- All pages accessible

### Manual Tests
- Visual inspection of all pages
- Search functionality
- Theme toggle
- Responsive design (mobile, tablet, desktop)

### Performance Tests
- Build time measurement
- Page load time measurement
- Bundle size analysis

---

## Dependencies

### Internal Dependencies
- Fumadocs MDX content (16 files)
- Existing VitePress config
- CLI documentation (4 files)

### External Dependencies
- VitePress 1.6.4
- Vue 3.4.0
- TypeScript 5.3.0
- Node.js 20+

### System Dependencies
- npm or yarn (package manager)
- Bash shell (for scripts)

---

## Success Criteria

### Must Have
- [ ] Clean `/docs/` directory (only `app/`, `specs/`, `md/`)
- [ ] All 16 documentation pages converted and accessible
- [ ] Build succeeds with `npm run docs:build`
- [ ] Dev server runs on `localhost:5173`
- [ ] No broken internal links
- [ ] Build time < 2 minutes

### Should Have
- [ ] Search functionality works
- [ ] Dark/light theme toggle works
- [ ] Responsive design on mobile/tablet/desktop
- [ ] Home page with SYNAPSE branding

### Could Have
- [ ] GitHub Pages deployment configured
- [ ] Custom styling for authority levels
- [ ] Edit on GitHub links

---

## Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Preparation & Backup | 0.5h | 0.5h |
| Phase 2: Content Migration | 2h | 2.5h |
| Phase 3: VitePress Configuration | 0.75h | 3.25h |
| Phase 4: Cleanup | 1h | 4.25h |
| Phase 5: Validation & Testing | 1h | 5.25h |
| Phase 6: Documentation | 0.5h | 5.75h |
| **Total** | **5.75h** | **5.75h** |

---

## Rollback Plan

If any phase fails:

### Rollback Phase 4 (Cleanup)
- Restore from backup at `/docs/backup-[timestamp]/`
- Verify restoration
- Investigate failure cause
- Fix issue before retry

### Rollback Phase 2 (Content Migration)
- Keep converted files in `/docs/md/`
- Investigate conversion issues
- Fix MDX conversion logic
- Retry conversion

### Rollback Phase 3 (Configuration)
- Revert config.mts to previous version
- Verify dev server works
- Investigate config errors
- Fix configuration issues

### Rollback All Phases
- Delete `/docs/md/` (if created)
- Restore entire `/docs/` from backup
- Investigate root cause
- Plan alternative approach

---

## Open Questions

1. **GitHub Pages Configuration**: Should GitHub Pages be configured as part of this feature?
   - **Recommendation**: No, defer to separate feature or manual setup

2. **Custom Styling**: Should custom CSS be added for SYNAPSE branding?
   - **Recommendation**: No, use default VitePress theme for simplicity

3. **Additional Documentation**: Should more documentation be added beyond existing 16 pages?
   - **Recommendation**: No, migrate existing content first, expand later

4. **Backup Retention**: How long should backup be kept?
   - **Recommendation**: 24 hours after completion, then delete

---

## Next Steps

### Immediate Actions
1. Review and approve this plan
2. Create `tasks.md` with detailed task breakdown
3. Begin Phase 1: Preparation & Backup

### Post-Completion
1. Test documentation thoroughly
2. Gather user feedback
3. Plan additional features (GitHub Pages, custom styling, etc.)

---

**Document Status**: Ready for Implementation

**Next Phase**: Task Breakdown (`tasks.md`)
