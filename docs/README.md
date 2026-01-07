# SYNAPSE Documentation

This directory contains SYNAPSE documentation built with **VitePress 1.6.4**.

---

## Quick Start

### Prerequisites
- Node.js 18 or higher
- npm or package manager

### Setup

```bash
# Navigate to documentation directory
cd docs/app

# Install dependencies
npm install

# Start dev server (runs on http://localhost:5173)
npm run docs:dev
```

That's it! The documentation will be available at `http://localhost:5173`.

---

## Structure

```
docs/
├── app/                    # VitePress engine
│   ├── .vitepress/
│   │   ├── config.mts     # VitePress configuration
│   │   ├── cache/         # Build cache (gitignored)
│   │   └── dist/          # Build output (gitignored)
│   └── package.json       # VitePress dependencies
│
├── md/                     # Documentation content
│   ├── index.md           # Home page
│   ├── getting-started/    # 4 files
│   ├── architecture/       # 3 files
│   ├── usage/             # 3 files
│   ├── api-reference/      # 3 files
│   └── development/       # 3 files
│
├── specs/                 # SDD specifications
│   ├── index.md
│   └── [5 feature specs]
│
└── backup-20260107-144833/  # Historical backup (Fumadocs)
```

---

## Documentation Guide

| Document | Purpose |
|----------|---------|
| [Structure Guide](./STRUCTURE.md) | Directory layout and rationale for Option B |
| [Migration Summary](./MIGRATION.md) | Fumadocs → VitePress migration details |
| [Contributing Guide](./CONTRIBUTING-DOCS.md) | How to edit and contribute to docs |

---

## Available Scripts

From `docs/app/` directory:

```bash
npm run docs:dev       # Start dev server (localhost:5173)
npm run docs:build     # Build for production
npm run docs:preview   # Preview production build (localhost:4173)
```

---

## Key Concepts

### Option B Structure

We use **Option B** VitePress configuration:
- **Engine**: `app/` - VitePress config and build artifacts
- **Content**: `md/` - Documentation pages
- **Separation**: Clean separation of concerns

The `srcDir: "../md"` in `config.mts` tells VitePress to read content from the `md/` directory.

### Benefits

- ✅ Clean separation of engine and content
- ✅ Easier maintenance
- ✅ Better git history
- ✅ 92% smaller footprint (vs Fumadocs)
- ✅ 4x faster builds (30 seconds vs 2 minutes)

---

## Documentation Sections

| Section | Description | Pages |
|---------|-------------|-------|
| **Getting Started** | User onboarding | 4 pages |
| **Architecture** | System design | 3 pages |
| **Usage** | How to use SYNAPSE | 3 pages |
| **API Reference** | API documentation | 3 pages |
| **Development** | Contributing guide | 3 pages |

**Total**: 16 documentation pages

---

## View Online

Documentation will be deployed at:
```
https://kayisrahman.github.io/synapse/docs/
```

(Note: GitHub Pages deployment requires manual setup)

---

## Technology Stack

- **VitePress 1.6.4** - Static site generator
- **Vue 3.4.0** - Framework
- **TypeScript 5.3.0** - Configuration language
- **Markdown** - Content format

---

## Migration History

**Previous**: Fumadocs (Next.js 15.5.9)
- Complex configuration (5+ files)
- 50+ dependencies
- 992K total size
- ~2 minute builds

**Current**: VitePress (Option B)
- Simple configuration (1 file)
- 3 dependencies
- 72K total size
- ~30 second builds

**Benefits**: 92% size reduction, 4x faster builds, easier maintenance

See [Migration Summary](./MIGRATION.md) for details.

---

## Backup Reference

The `backup-20260107-144833/` directory contains the historical Fumadocs/Next.js structure before migration to VitePress.

**Purpose**: Reference only, can be deleted after documentation is finalized.

**Contents**:
- Next.js application code
- Fumadocs configuration
- MDX content files (17 files)
- Historical documentation

---

## Contributing

Want to help improve documentation?

1. Read the [Contributing Guide](./CONTRIBUTING-DOCS.md)
2. Make your changes
3. Test locally
4. Submit a pull request

All contributions are welcome! 🙌

---

## Troubleshooting

### Dev server won't start?

```bash
# Kill process on port 5173
npx kill-port 5173

# Or use different port
npm run docs:dev -- --port 5174
```

### Build fails?

```bash
# Clear cache and reinstall
rm -rf .vitepress/cache node_modules package-lock.json
npm install
npm run docs:build
```

### Changes not showing?

- Refresh browser (Cmd+R or F5)
- Check console for errors
- Restart dev server if needed

---

## Support

- 📖 [Documentation Guide](./STRUCTURE.md)
- 📝 [Contributing Guide](./CONTRIBUTING-DOCS.md)
- 🔄 [Migration Summary](./MIGRATION.md)
- 🐛 [Report Issues](https://github.com/kayis-rahman/synapse/issues)
- 💬 [Discussions](https://github.com/kayis-rahman/synapse/discussions)

---

## License

Documentation is released under the same license as SYNAPSE (MIT).

---

**Happy documenting!** 📚
