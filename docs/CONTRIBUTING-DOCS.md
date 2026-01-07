# Contributing to SYNAPSE Documentation

This guide helps you contribute to SYNAPSE documentation built with VitePress.

---

## Quick Start

### Prerequisites

- **Node.js** 18 or higher
- **npm** or package manager (pnpm, yarn, bun)
- **Text editor** (VSCode recommended with Vue extension)

### Setup

```bash
# Navigate to documentation directory
cd docs/app

# Install dependencies
npm install

# Start dev server (runs on http://localhost:5173)
npm run docs:dev
```

The dev server supports hot module replacement - changes reload automatically.

---

## Architecture Overview

### Directory Structure

```
docs/
├── app/                              # VitePress engine
│   ├── .vitepress/
│   │   ├── config.mts                # Main configuration
│   │   ├── cache/                    # Build cache (gitignored)
│   │   └── dist/                     # Build output (gitignored)
│   └── package.json                  # Dependencies
│
├── md/                               # Documentation content
│   ├── index.md                       # Home page
│   ├── getting-started/                # Getting Started section
│   ├── architecture/                   # Architecture section
│   ├── usage/                         # Usage section
│   ├── api-reference/                  # API Reference section
│   └── development/                   # Development section
│
└── specs/                            # SDD specifications
```

### Key Concepts

**Engine vs Content:**
- `app/` - VitePress configuration and build artifacts
- `md/` - Documentation content (what you'll edit)

**Configuration:**
- All navigation, theme, and site settings in `app/.vitepress/config.mts`
- `srcDir: "../md"` tells VitePress to read content from `md/` directory

---

## Editing Documentation

### Adding a New Page

#### Step 1: Create Markdown File

Navigate to appropriate section and create `.md` file:

```bash
# Example: Add new page to Getting Started
cd docs/md/getting-started
touch troubleshooting.md
```

#### Step 2: Add Frontmatter

```markdown
---
title: Troubleshooting
description: Common issues and solutions
---

# Troubleshooting

Your content here...
```

#### Step 3: Update Navigation

Edit `docs/app/.vitepress/config.mts`:

```typescript
sidebar: [
  {
    text: 'Getting Started',
    items: [
      { text: 'Introduction', link: '/getting-started/introduction' },
      { text: 'Installation', link: '/getting-started/installation' },
      { text: 'Quick Start', link: '/getting-started/quick-start' },
      { text: 'Configuration', link: '/getting-started/configuration' },
      // Add your new page here
      { text: 'Troubleshooting', link: '/getting-started/troubleshooting' }
    ]
  }
]
```

#### Step 4: Restart Dev Server

If dev server is running, it will reload automatically.

#### Step 5: Verify

Open `http://localhost:5173/getting-started/troubleshooting` in browser.

---

### Editing an Existing Page

#### Step 1: Locate File

Use the file location reference:

| Content | Location |
|---------|-----------|
| Home page | `md/index.md` |
| Getting Started | `md/getting-started/` |
| Architecture | `md/architecture/` |
| Usage | `md/usage/` |
| API Reference | `md/api-reference/` |
| Development | `md/development/` |

#### Step 2: Edit File

Edit markdown file in your text editor. Changes hot-reload automatically.

#### Step 3: Test Changes

- View in browser at `http://localhost:5173/[path]`
- Check formatting
- Test internal links
- Verify code blocks render correctly

#### Step 4: Commit Changes

```bash
git add docs/md/[filename].md
git commit -m "docs: update [filename]"
git push
```

---

## Markdown Guide

### Frontmatter

Required at top of every page:

```markdown
---
title: Page Title
description: Page description (shown in search results)
---
```

Optional frontmatter fields:
```markdown
---
title: Page Title
description: Page description
layout: home              # For home page only
outline: [2, 3]          # Table of contents depth
lastUpdated: true         # Show "Last Updated" timestamp
---
```

### Headings

```markdown
# H1 Heading
## H2 Heading
### H3 Heading
#### H4 Heading
```

**Note:** H1 should only appear once per page (title).

### Code Blocks

```markdown
\`\`\`python
def hello():
    print("Hello, World!")
\`\`\`

\`\`\`bash
pip install synapse
\`\`\`

\`\`\`json
{
  "name": "synapse",
  "version": "1.0.0"
}
\`\`\`
```

**Supported Languages:** python, bash, json, yaml, javascript, typescript, markdown, etc.

### Callouts (Alerts)

```markdown
> **Info:** This is an informational note.

> **Warning:** This is a warning.

> **Error:** This is an error message.

> **Tip:** This is a helpful tip.
```

### Links

**Internal Links:**
```markdown
[Link text](/path/to/page)
[Getting Started](/getting-started/introduction)
```

**External Links:**
```markdown
[SYNAPSE GitHub](https://github.com/kayis-rahman/synapse)
```

**Anchor Links:**
```markdown
[Jump to section](#section-heading)
```

### Lists

**Unordered:**
```markdown
- Item 1
- Item 2
  - Nested item
  - Another nested item
- Item 3
```

**Ordered:**
```markdown
1. Step 1
2. Step 2
3. Step 3
```

**Task Lists:**
```markdown
- [ ] Incomplete task
- [x] Completed task
```

### Tables

```markdown
| Column 1 | Column 2 | Column 3 |
|-----------|-----------|-----------|
| Row 1     | Data      | Data      |
| Row 2     | Data      | Data      |
```

### Images

```markdown
![Alt text](/path/to/image.png)
![SYNAPSE Logo](./images/logo.png)
```

**Note:** Images should be placed in `md/.vitepress/public/` or use external URLs.

### Horizontal Rule

```markdown
---
```

---

## VitePress Features

### Vue Components

You can use Vue components in markdown:

```markdown
<script setup>
import { ref } from 'vue'

const count = ref(0)
</script>

# Interactive Demo

Count: {{ count }}

<button @click="count++">Increment</button>
```

### Custom CSS

Add custom CSS to your page:

```markdown
<style>
.custom-class {
  color: #3B82F6;
  font-weight: bold;
}
</style>

This is <span class="custom-class">custom styled</span> text.
```

### Table of Contents

Automatically generated from headings. Configure depth in frontmatter:

```markdown
---
outline: [2, 3]  # Show H2 and H3 headings
---
```

Or in config.mts:
```typescript
export default defineConfig({
  themeConfig: {
    outline: {
      level: [2, 3]
    }
  }
})
```

### Last Updated

Show last updated timestamp:

```markdown
---
lastUpdated: true
---
```

Configure format in config.mts:
```typescript
export default defineConfig({
  themeConfig: {
    lastUpdated: {
      formatOptions: {
        dateStyle: 'full',
        timeStyle: 'short'
      }
    }
  }
})
```

### Prev/Next Navigation

Automatically generated based on sidebar order.

Disable for specific page:
```markdown
---
prev: false
next: false
---
```

---

## Configuration

### Navigation (Top Bar)

Edit `docs/app/.vitepress/config.mts`:

```typescript
themeConfig: {
  nav: [
    { text: 'Home', link: '/' },
    { text: 'Getting Started', link: '/getting-started/introduction' },
    { text: 'Architecture', link: '/architecture/overview' },
    { text: 'Usage', link: '/usage/mcp-tools' },
    { text: 'API Reference', link: '/api-reference/memory-tools' },
    { text: 'Development', link: '/development/contributing' }
  ]
}
```

### Sidebar (Left Menu)

Edit `docs/app/.vitepress/config.mts`:

```typescript
themeConfig: {
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
    }
    // ... more sections
  ]
}
```

### Site Metadata

Edit `docs/app/.vitepress/config.mts`:

```typescript
export default defineConfig({
  title: 'SYNAPSE',
  description: 'Your Data Meets Intelligence - Local-first RAG system',

  head: [
    ['link', { rel: 'icon', href: '/favicon.ico' }],
    ['meta', { name: 'theme-color', content: '#3c8772' }]
  ]
})
```

### Social Links

Edit `docs/app/.vitepress/config.mts`:

```typescript
themeConfig: {
  socialLinks: [
    { icon: 'github', link: 'https://github.com/kayis-rahman/synapse' }
  ]
}
```

### Footer

Edit `docs/app/.vitepress/config.mts`:

```typescript
themeConfig: {
  footer: {
    message: 'Released under the MIT License.',
    copyright: 'Copyright © 2026 SYNAPSE'
  }
}
```

---

## Building and Deploying

### Local Build

```bash
cd docs/app
npm run docs:build
```

Build output: `docs/app/.vitepress/dist/`

### Preview Production Build

```bash
npm run docs:preview
```

Runs on `http://localhost:4173`

### GitHub Pages Deployment

Create `.github/workflows/deploy-docs.yml`:

```yaml
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

Configure GitHub Pages:
1. Go to repo Settings → Pages
2. Set Source: GitHub Actions
3. Deploy on next push

---

## Best Practices

### Writing Style

1. **Be Clear and Concise**: Use simple language, avoid jargon
2. **Use Active Voice**: "Install SYNAPSE" not "SYNAPSE should be installed"
3. **Be Consistent**: Use same terminology throughout
4. **Provide Examples**: Show, don't just tell
5. **Include Screenshots**: Visual aids when helpful

### Code Examples

1. **Use Syntax Highlighting**: Always specify language
2. **Keep it Simple**: Avoid complex examples
3. **Add Comments**: Explain what code does
4. **Test Everything**: Verify code works

### Structure

1. **Start with Overview**: What is this about?
2. **Provide Prerequisites**: What do users need?
3. **Step-by-Step Instructions**: Clear, numbered steps
4. **Troubleshooting**: Common issues and solutions
5. **Next Steps**: What should users do next?

### Links

1. **Use Relative Paths**: `/getting-started/introduction` not `../introduction`
2. **Link to Related Content**: Cross-reference other docs
3. **Avoid Dead Links**: Test all links before committing
4. **Descriptive Link Text**: "Get Started" not "click here"

---

## Common Tasks

### Fixing Typos

1. Find and edit the file
2. Make changes
3. Test in dev server
4. Commit: `docs: fix typo in [filename]`

### Updating API Docs

1. Locate API doc in `md/api-reference/`
2. Update content
3. Test examples work
4. Commit: `docs: update [tool-name] API docs`

### Adding Code Example

1. Use fenced code block with language
2. Add comments explaining code
3. Test code runs successfully
4. Commit: `docs: add example for [feature]`

### Restructuring Section

1. Create new section directory in `md/`
2. Move relevant files
3. Update sidebar in `config.mts`
4. Test navigation
5. Commit: `docs: restructure [section-name]`

---

## Troubleshooting

### Dev Server Won't Start

**Problem**: Port 5173 already in use

**Solution**:
```bash
# Kill process on port 5173
npx kill-port 5173

# Or use different port
npx vitepress dev --port 5174
```

### Changes Not Reflecting

**Problem**: Edits not showing in browser

**Solution**:
1. Refresh browser (Cmd+R or F5)
2. Check console for errors
3. Restart dev server
4. Clear browser cache

### Build Fails

**Problem**: `npm run docs:build` fails

**Solutions**:
- Check markdown syntax (unclosed backticks, malformed links)
- Verify frontmatter is valid YAML
- Check for special characters in filenames
- Clear cache: `rm -rf .vitepress/cache`
- Reinstall dependencies: `rm -rf node_modules package-lock.json && npm install`

### Navigation Not Showing

**Problem**: New page not in sidebar

**Solution**:
1. Check `config.mts` sidebar configuration
2. Verify link path matches file path
3. Restart dev server
4. Check for syntax errors in config.mts

---

## Resources

### Official Documentation

- [VitePress Guide](https://vitepress.dev/guide/)
- [VitePress Config Reference](https://vitepress.dev/reference/site-config)
- [VitePress Markdown](https://vitepress.dev/guide/markdown)
- [VitePress Theming](https://vitepress.dev/guide/custom-theme)

### Markdown Resources

- [CommonMark Spec](https://spec.commonmark.org/)
- [GitHub Flavored Markdown](https://github.github.com/gfm/)

### SYNAPSE Resources

- [Structure Guide](../STRUCTURE.md) - Directory layout
- [Migration Summary](../MIGRATION.md) - How we got here
- [README](../README.md) - Quick start

---

## Getting Help

If you need help:

1. **Check existing docs**: Look for similar content
2. **Check official docs**: VitePress documentation is excellent
3. **Open an issue**: https://github.com/kayis-rahman/synapse/issues
4. **Ask in discussions**: https://github.com/kayis-rahman/synapse/discussions

---

## Contributing Workflow

1. **Fork repository**
2. **Create branch**: `git checkout -b docs/[your-change]`
3. **Edit content**
4. **Test locally**: `npm run docs:dev`
5. **Build production**: `npm run docs:build`
6. **Commit changes**: Clear, descriptive commit messages
7. **Push to fork**
8. **Create pull request**

---

## Code Review Guidelines

When reviewing documentation PRs:

1. **Accuracy**: Content is factually correct
2. **Clarity**: Easy to understand
3. **Formatting**: Proper markdown syntax
4. **Links**: All links work
5. **Examples**: Code examples work
6. **Spelling**: No typos
7. **Consistency**: Matches style guide

---

**Happy documenting!** 📝
