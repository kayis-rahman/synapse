# Synapse Auto-Learning Plugin for OpenCode

## Overview

Automatically extracts facts and episodes from agent conversations and stores them in RAG memory.

## Configuration

Configure via `configs/rag_config.json`:

```json
{
  "universal_hooks": {
    "adapters": {
      "opencode": {
        "enabled": true,
        "priority": 1,
        "analyze_after_tools": ["rag.add_fact", "rag.add_episode"],
        "min_message_length": 10,
        "skip_patterns": ["^test$", "^hello$"],
        "extraction_mode": "heuristic"
      }
    },
    "conversation_analyzer": {
      "extraction_mode": "heuristic",
      "min_fact_confidence": 0.7,
      "min_episode_confidence": 0.6,
      "deduplication_mode": "per_day",
      "deduplication_window_days": 7
    }
  }
}
```

## Extraction Mode

- **heuristic**: Fast regex patterns (no LLM, <10ms)
- **llm**: Prompt-based extraction (not yet implemented)
- **hybrid**: Heuristics + LLM (not yet implemented)

## Hooks

- `tool.execute.before`: Analyzes conversation after configured tools
- `tool.execute.after`: Logs tool execution for debugging

## Requirements

- OpenCode CLI
- RAG MCP server running
- Configured `rag_config.json`

## Troubleshooting

**Plugin not loading**: Check `.opencode/plugins/` directory exists
**Analysis not working**: Check RAG MCP server is running
**Too many false positives**: Increase `min_fact_confidence` and `min_episode_confidence`

## Testing

1. Start RAG MCP server: `python -m mcp_server.rag_server`
2. Start OpenCode with plugins enabled
3. Run RAG tools (rag.add_fact, rag.add_episode, etc.)
4. Check console for `[Synapse]` log messages
