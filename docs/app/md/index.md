---
layout: home
---

# SYNAPSE

Your Data Meets Intelligence

A local-first RAG system that connects your knowledge to AI.

## Features

<div class="features">

### 🧠 Neural Storage
Three-tier memory system (symbolic, episodic, semantic) with authority hierarchy

### ⚡ Synaptic Transmission
MCP protocol for seamless integration with AI agents

### 🌐 Local-First
Your data never leaves your system with optional remote ingestion

### 🤖 Auto-Learning
Automatic extraction and storage of knowledge from interactions

### 🔍 Flexible Querying
Query expansion, memory selection, and context injection

### 🚀 Production Ready
HTTP server, CLI tools, and comprehensive API

</div>

---

## Quick Links

<a href="/getting-started/introduction" class="feature-link">
  <div class="feature-card">
    <div class="feature-icon">📚</div>
    <h3>Get Started</h3>
    <p>Install and configure SYNAPSE in minutes</p>
  </div>
</a>

<a href="/architecture/overview" class="feature-link">
  <div class="feature-card">
    <div class="feature-icon">🏗️</div>
    <h3>Architecture</h3>
    <p>Learn about SYNAPSE's design and components</p>
  </div>
</a>

<a href="/usage/mcp-tools" class="feature-link">
  <div class="feature-card">
    <div class="feature-icon">🔧</div>
    <h3>MCP Tools</h3>
    <p>Explore 7 MCP tools for AI integration</p>
  </div>
</a>

<a href="/development/contributing" class="feature-link">
  <div class="feature-card">
    <div class="feature-icon">🤝</div>
    <h3>Contributing</h3>
    <p>Join the community and help improve SYNAPSE</p>
  </div>
</a>

---

## Actions

<div class="actions">

<a href="/getting-started/quick-start" class="action-link">
  <div class="action-button primary">
    <h3>🚀 Get Started</h3>
    <p>Quick start guide for immediate results</p>
  </div>
</a>

<a href="/getting-started/installation" class="action-link">
  <div class="action-button secondary">
    <h3>📖 Install SYNAPSE</h3>
    <p>Pip install and setup instructions</p>
  </div>
</a>

<a href="https://github.com/kayis-rahman/synapse" target="_blank" class="action-link">
  <div class="action-button secondary">
    <div class="feature-icon">📦</div>
    <h3>View on GitHub</h3>
    <p>Source code, issues, and discussions</p>
  </div>
</a>

</div>

<style>
.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.feature-card {
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-border);
  border-radius: 8px;
  padding: 1.5rem;
  transition: transform 0.2s;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.feature-card h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
  color: var(--vp-c-text);
}

.feature-card p {
  font-size: 0.9rem;
  color: var(--vp-c-text-secondary);
  line-height: 1.5;
  margin: 0;
}

.actions {
  display: flex;
  gap: 1rem;
  margin: 3rem 0;
  flex-wrap: wrap;
  justify-content: center;
}

.action-link {
  text-decoration: none;
}

.action-button {
  display: inline-block;
  padding: 1rem 2rem;
  border-radius: 8px;
  font-weight: 600;
  text-decoration: none;
  transition: transform 0.2s, box-shadow 0.2s;
  background: var(--vp-c-brand);
  color: #fff;
}

.action-button h3 {
  font-size: 1.1rem;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.action-button p {
  font-size: 0.9rem;
  margin: 0;
}

.action-button.secondary {
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text);
  border: 1px solid var(--vp-c-border);
}

.action-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
}

@media (max-width: 768px) {
  .features {
    grid-template-columns: 1fr;
  }

  .actions {
    flex-direction: column;
    align-items: center;
  }
}
</style>
