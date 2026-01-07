# VitePress Simple Documentation - Tasks

**Feature ID**: 005-vitepress-simple-docs
**Status**: [In Progress]
**Last Updated**: January 7, 2026

---

## Progress Summary

### PENDING Phases

- [ ] **Phase 1**: Preparation & Backup
- [ ] **Phase 2**: Content Migration (MDX → Markdown)
- [ ] **Phase 3**: VitePress Configuration
- [ ] **Phase 4**: Cleanup
- [ ] **Phase 5**: Validation & Testing
- [ ] **Phase 6**: Documentation

---

## Phase 1: Preparation & Backup

- [ ] Create backup of entire `/docs/` directory (Linked to FR-1)
- [ ] Verify backup integrity (Linked to Risk Mitigation)
- [ ] Create new directory structure skeleton (app/, specs/, md/) (Linked to FR-1)
- [ ] Identify all files to be deleted (Linked to Phase 4)

---

## Phase 2: Content Migration

### Convert MDX Files (16 files)

#### Getting Started Section
- [ ] Convert `introduction.mdx` → `md/getting-started/introduction.md` (Linked to US-3)
  - Remove MDX-specific syntax (imports, components)
  - Convert custom components to markdown
  - Verify markdown syntax
- [ ] Convert `installation.mdx` → `md/getting-started/installation.md` (Linked to US-3)
  - Remove MDX-specific syntax
  - Convert custom components to markdown
  - Verify markdown syntax
- [ ] Convert `quick-start.mdx` → `md/getting-started/quick-start.md` (Linked to US-3)
  - Remove MDX-specific syntax
  - Convert custom components to markdown
  - Verify markdown syntax
- [ ] Convert `configuration.mdx` → `md/getting-started/configuration.md` (Linked to US-3)
  - Remove MDX-specific syntax
  - Convert custom components to markdown
  - Verify markdown syntax

#### Architecture Section
- [ ] Convert `overview.mdx` → `md/architecture/overview.md` (Linked to US-3)
  - Remove MDX-specific syntax
  - Convert custom components to markdown
  - Verify markdown syntax
- [ ] Convert `memory-system.mdx` → `md/architecture/memory-system.md` (Linked to US-3)
  - Remove MDX-specific syntax
  - Convert custom components to markdown
  - Verify markdown syntax
- [ ] Convert `mcp-protocol.mdx` → `md/architecture/mcp-protocol.md` (Linked to US-3)
  - Remove MDX-specific syntax
  - Convert custom components to markdown
  - Verify markdown syntax

#### Usage Section
- [ ] Convert `mcp-tools.mdx` → `md/usage/mcp-tools.md` (Linked to US-3)
  - Remove MDX-specific syntax
  - Convert custom components to markdown
  - Verify markdown syntax
- [ ] Convert `ingestion.mdx` → `md/usage/ingestion.md` (Linked to US-3)
  - Remove MDX-specific syntax
  - Convert custom components to markdown
  - Verify markdown syntax
- [ ] Convert `querying.mdx` → `md/usage/querying.md` (Linked to US-3)
  - Remove MDX-specific syntax
  - Convert custom components to markdown
  - Verify markdown syntax

#### API Reference Section
- [ ] Convert `memory-tools.mdx` → `md/api-reference/memory-tools.md` (Linked to US-3)
  - Remove MDX-specific syntax
  - Convert custom components to markdown
  - Verify markdown syntax
- [ ] Convert `server-api.mdx` → `md/api-reference/server-api.md` (Linked to US-3)
  - Remove MDX-specific syntax
  - Convert custom components to markdown
  - Verify markdown syntax
- [ ] Convert `cli-commands.mdx` → `md/api-reference/cli-commands.md` (Linked to US-3)
  - Remove MDX-specific syntax
  - Convert custom components to markdown
  - Merge CLI documentation from `/docs/docs/docs/api/cli-commands/`
  - Verify markdown syntax

#### Development Section
- [ ] Convert `contributing.mdx` → `md/development/contributing.md` (Linked to US-3)
  - Remove MDX-specific syntax
  - Convert custom components to markdown
  - Verify markdown syntax
- [ ] Convert `testing.mdx` → `md/development/testing.md` (Linked to US-3)
  - Remove MDX-specific syntax
  - Convert custom components to markdown
  - Verify markdown syntax
- [ ] Convert `deployment.mdx` → `md/development/deployment.md` (Linked to US-3)
  - Remove MDX-specific syntax
  - Convert custom components to markdown
  - Verify markdown syntax

### Migration CLI Documentation
- [ ] Merge 4 CLI MD files into single `api-reference/cli-commands.md` (Linked to US-3)
  - Read from `/docs/docs/docs/api/cli-commands/`
  - Update internal links to new paths
  - Delete source files after merge

---

## Phase 3: VitePress Configuration

### Update Config File
- [ ] Edit `/docs/app/.vitepress/config.mts` (Linked to FR-2)
  - Update `srcDir` from `../` to `../md`
  - Configure top navigation (Home, Getting Started, Architecture, Usage, API Reference, Development)
  - Configure sidebar navigation with all sections
  - Add GitHub social links
  - Add footer configuration

### Create Home Page
- [ ] Create `/docs/md/index.md` (Linked to FR-4)
  - Add SYNAPSE hero section ("Your Data Meets Intelligence")
  - Add feature cards (6 cards)
  - Add action buttons (Get Started, Quick Start)
  - Use VitePress home layout

### Update Package Scripts
- [ ] Verify `/docs/app/package.json` has correct scripts (Linked to FR-2)
  - docs:dev: "vitepress dev"
  - docs:build: "vitepress build"
  - docs:preview: "vitepress preview"

---

## Phase 4: Cleanup

### Delete Root-Level Files
- [ ] Delete `.gitignore` from `/docs/` (Linked to FR-1)
- [ ] Delete `FUMADOCS_IMPLEMENTATION_SUMMARY.md` from `/docs/` (Linked to FR-1)
- [ ] Delete `next-env.d.ts` from `/docs/` (Linked to FR-1)
- [ ] Delete `next.config.mjs` from `/docs/` (Linked to FR-1)
- [ ] Delete `package.json` (Fumadocs version) from `/docs/` (Linked to FR-1)
- [ ] Delete `package-lock.json` (Fumadocs version) from `/docs/` (Linked to FR-1)
- [ ] Delete `README.md` from `/docs/` (Linked to FR-1)
- [ ] Delete `source.config.ts` from `/docs/` (Linked to FR-1)
- [ ] Delete `tsconfig.json` from `/docs/` (Linked to FR-1)
- [ ] Delete `troubleshooting-auto-learning.md` from `/docs/` (Linked to FR-1)

### Delete Empty/Unused Directories
- [ ] Delete `archive/` from `/docs/` (Linked to FR-1)
- [ ] Delete `api/` from `/docs/` (Linked to FR-1)
- [ ] Delete `getting-started/` from `/docs/` (Linked to FR-1)
- [ ] Delete `docs/` from `/docs/` (Linked to FR-1)

### Clean `/docs/app/` Directory
- [ ] Delete `[lang]/` from `/docs/app/` (Linked to FR-1)
- [ ] Delete `layout.tsx` from `/docs/app/` (Linked to FR-1)
- [ ] Delete `page.tsx` from `/docs/app/` (Linked to FR-1)
- [ ] Delete `globals.css` from `/docs/app/` (Linked to FR-1)

### Delete Fumadocs Content
- [ ] Delete `content/` from `/docs/` (Linked to FR-1)
  - Verify all files migrated to `/docs/md/` before deletion

---

## Phase 5: Validation & Testing

### Install Dependencies
- [ ] Run `npm install` in `/docs/app/` (Linked to NFR-1)
  - Verify no errors
  - Verify dependencies installed

### Run Dev Server
- [ ] Run `npm run docs:dev` in `/docs/app/` (Linked to NFR-1)
  - Verify server starts on `http://localhost:5173`
  - Verify no console errors
  - Verify home page loads

### Test Navigation
- [ ] Test top navigation (Linked to US-4)
  - Verify Home link works
  - Verify Getting Started link works
  - Verify Architecture link works
  - Verify Usage link works
  - Verify API Reference link works
  - Verify Development link works
- [ ] Test sidebar navigation (Linked to US-4)
  - Verify all sections expandable
  - Verify all pages accessible
  - Verify no 404 errors
- [ ] Test internal links (Linked to FR-6)
  - Verify "See Also" sections work
  - Verify cross-references work
  - Verify no broken links

### Test Search Functionality
- [ ] Verify search bar visible (Linked to US-5)
- [ ] Test ⌘K keyboard shortcut (Linked to US-5)
- [ ] Test search functionality (Linked to US-5)
  - Search for "MCP"
  - Search for "memory"
  - Search for "ingestion"
  - Verify results highlighted

### Test Theme Support
- [ ] Verify theme toggle button visible (Linked to US-6)
- [ ] Test dark mode (Linked to US-6)
  - Verify legible
  - Verify all pages work
- [ ] Test light mode (Linked to US-6)
  - Verify legible
  - Verify all pages work
- [ ] Verify theme preference persists (Linked to US-6)

### Build Production
- [ ] Run `npm run docs:build` (Linked to NFR-1)
  - Verify build completes successfully
  - Verify build time < 2 minutes
  - Verify output in `.vitepress/dist/`
  - Verify no build errors or warnings

### Preview Production Build
- [ ] Run `npm run docs:preview` (Linked to NFR-1)
  - Verify preview works on localhost:4173
  - Verify all pages accessible
  - Verify navigation works
  - Verify no console errors

### Link Validation
- [ ] Verify all internal links work (Linked to FR-6)
- [ ] Verify no broken links (Linked to FR-6)
- [ ] Verify cross-references correct (Linked to FR-6)

### Performance Validation
- [ ] Measure build time (target: < 2 minutes) (Linked to NFR-1)
- [ ] Test page load time (target: < 2 seconds) (Linked to NFR-1)
- [ ] Verify static generation works (Linked to NFR-1)

---

## Phase 6: Documentation

### Update Spec Index
- [ ] Update `/docs/specs/index.md` (Linked to SDD Protocol)
  - Add entry for 005-vitepress-simple-docs
  - Set status to [In Progress]
  - Add creation date

### Create Completion Summary
- [ ] Create `/docs/specs/005-vitepress-simple-docs/COMPLETION-SUMMARY.md` (Linked to SDD Protocol)
  - Document what was completed
  - List all files created
  - Document file deletions
  - Summary of changes
  - Known limitations
  - Future work

### Mark Tasks Complete
- [ ] Update this `tasks.md` file (Linked to SDD Protocol)
  - Mark completed tasks with [x]
  - Update progress summary

### Update Spec Index to Completed
- [ ] Update `/docs/specs/index.md` (Linked to SDD Protocol)
  - Change status to [Completed]
  - Add completion date
  - Add final commit hash

---

## Task Notes

### MDX Conversion Rules

When converting MDX files to markdown, apply these transformations:

1. **Remove Import Statements**
   ```mdx
   // DELETE
   import { Component } from 'fumadocs-ui'
   ```

2. **Convert Callout Components**
   ```mdx
   // FROM
   <Callout type="info">Text here</Callout>

   // TO
   > **Info:** Text here

   <Callout type="warning">Text here</Callout>

   // TO
   > ⚠️ **Warning:** Text here

   <Callout type="error">Text here</Callout>

   // TO
   > ❌ **Error:** Text here
   ```

3. **Convert Tab Components**
   ```mdx
   // FROM
   <TabGroup>
     <Tab label="Option 1">Content 1</Tab>
     <Tab label="Option 2">Content 2</Tab>
   </TabGroup>

   // TO
   ### Option 1
   Content 1

   ### Option 2
   Content 2
   ```

4. **Convert Code Block Components**
   ```mdx
   // FROM
   <CodeBlock language="python">code here</CodeBlock>

   // TO
   \```python
   code here
   \```
   ```

5. **Convert Link Components**
   ```mdx
   // FROM
   <Link to="/path/to/page">Text</Link>

   // TO
   [Text](/path/to/page)
   ```

6. **Remove JSX/TSX Syntax**
   - Replace `<Component />` with markdown equivalents
   - Remove JSX attributes
   - Use standard markdown syntax

### File Paths Reference

**Source Files (to be deleted):**
- `/docs/content/docs/getting-started/*.mdx` (4 files)
- `/docs/content/docs/architecture/*.mdx` (3 files)
- `/docs/content/docs/usage/*.mdx` (3 files)
- `/docs/content/docs/api-reference/*.mdx` (3 files)
- `/docs/content/docs/development/*.mdx` (3 files)
- `/docs/docs/docs/api/cli-commands/*.md` (4 files)

**Target Files (to be created):**
- `/docs/md/index.md` (home page)
- `/docs/md/getting-started/*.md` (4 files)
- `/docs/md/architecture/*.md` (3 files)
- `/docs/md/usage/*.md` (3 files)
- `/docs/md/api-reference/*.md` (3 files)
- `/docs/md/development/*.md` (3 files)

### Validation Checklist

After each phase, verify:

**Phase 1 (Preparation):**
- [ ] Backup created
- [ ] Backup verified
- [ ] Skeleton directories created

**Phase 2 (Migration):**
- [ ] All 16 MDX files converted
- [ ] Markdown syntax valid
- [ ] No MDX-specific syntax remaining

**Phase 3 (Configuration):**
- [ ] Config file updated
- [ ] Home page created
- [ ] Scripts verified

**Phase 4 (Cleanup):**
- [ ] `/docs/` contains only `app/`, `specs/`, `md/`
- [ ] No root-level files
- [ ] No empty directories

**Phase 5 (Validation):**
- [ ] Dev server works
- [ ] Build succeeds
- [ ] All pages accessible
- [ ] No broken links
- [ ] Performance targets met

**Phase 6 (Documentation):**
- [ ] Spec index updated
- [ ] Completion summary created
- [ ] Tasks marked complete

---

## Notes

### Priority Order

Based on plan.md, implementation order is:
1. **Preparation**: Backup and structure (safe start)
2. **Content Migration**: Convert MDX files (core content)
3. **Configuration**: VitePress config and home page (infrastructure)
4. **Cleanup**: Remove old systems (clean finish)
5. **Validation**: Test everything (quality assurance)
6. **Documentation**: Update specs (close the loop)

### Dependencies Between Phases

- Phase 1 must complete before Phase 2 (backup required)
- Phase 2 must complete before Phase 4 (content required before deletion)
- Phase 3 can proceed in parallel with Phase 2 (independent)
- Phase 5 depends on Phase 2, 3, 4 (all changes validated)
- Phase 6 depends on Phase 5 (documentation after validation)

---

**Next Step**: Begin Phase 1 - Preparation & Backup
