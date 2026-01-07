import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  
  srcDir: "../",
  
  title: "SYNAPSE",
  description: "Your Data Meets Intelligence - Local-first RAG system",
  
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Getting Started', link: '/getting-started/installation' },
      { text: 'API Reference', link: '/api/' }
    ],

    sidebar: [
      {
        text: 'Getting Started',
        items: [
          { text: 'Installation', link: '/getting-started/installation' },
          { text: 'Quick Start', link: '/getting-started/quick-start' }
        ]
      },
      {
        text: 'API Reference',
        items: [
          { text: 'Overview', link: '/api/' },
          {
            text: 'MCP Protocol',
            collapsed: false,
            items: [
              { text: 'Overview', link: '/api/mcp-protocol/' },
              { text: 'Tools', link: '/api/mcp-protocol/tools/' },
              { text: 'Integration', link: '/api/mcp-protocol/integration' }
            ]
          },
          {
            text: 'Memory System',
            collapsed: false,
            items: [
              { text: 'Overview', link: '/api/memory-system/' },
              { text: 'Symbolic Memory', link: '/api/memory-system/symbolic-memory' },
              { text: 'Episodic Memory', link: '/api/memory-system/episodic-memory' },
              { text: 'Semantic Memory', link: '/api/memory-system/semantic-memory' }
            ]
          },
          {
            text: 'CLI Commands',
            collapsed: false,
            items: [
              { text: 'Overview', link: '/api/cli-commands/' },
              { text: 'mcp-server', link: '/api/cli-commands/mcp-server' },
              { text: 'query', link: '/api/cli-commands/query' },
              { text: 'Complete Reference', link: '/api/cli-commands/complete-reference' }
            ]
          }
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/your-repo/synapse' }
    ]
  }
})
