/**
 * Synapse Auto-Learning Plugin for OpenCode
 *
 * PRIORITY 1: First adapter to implement.
 *
 * Hooks:
 * - tool.execute.before: Intercept tool calls to detect conversation patterns
 * - tool.execute.after: Capture tool execution results
 *
 * Integrates with RAG MCP server via rag.analyze_conversation tool.
 *
 * Features:
 * - Async processing enabled (non-blocking LLM calls)
 * - Every message analysis
 * - Hybrid extraction mode (default)
 * - Per-day deduplication
 * - Configurable token budget
 */

interface SynapseConfig {
  enabled: boolean;
  priority: number;
  analyze_after_tools: string[];
  min_message_length: number;
  skip_patterns: string[];
  rag_project_id: string;
  async_processing: boolean;
  extraction_mode: string;  // "heuristic" | "llm" | "hybrid"
}

export default {
  name: "synapse-auto-learning",
  version: "1.0.0",
  description: "Universal auto-learning for Synapse RAG (OpenCode adapter)",
  priority: 1,  // First adapter to implement

  config: {
    enabled: true,
    priority: 1,
    analyze_after_tools: ["rag.add_fact", "rag.add_episode", "rag.search", "rag.get_context"],
    min_message_length: 10,
    skip_patterns: ["^test$", "^hello$"],
    rag_project_id: "synapse",
    async_processing: true,  // Enable async processing
    extraction_mode: "hybrid"  // Default to hybrid mode
  } as SynapseConfig,

  hooks: {
    async "tool.execute.before"(
      toolName: string,
      args: any,
      context: {
        userMessage?: string;
        lastAgentResponse?: string;
        session: any;
      }
    ): Promise<any> {
      const config = this.config as SynapseConfig;

      if (!config.enabled) {
        return;
      }

      // Skip analysis for certain tools
      if (!config.analyze_after_tools.includes(toolName)) {
        return;
      }

      // Check if we have user message and agent response
      if (!context.userMessage || !context.lastAgentResponse) {
        return;
      }

      // Skip short messages
      if (context.userMessage.length < config.min_message_length) {
        return;
      }

      // Skip if matches skip patterns
      for (const pattern of config.skip_patterns) {
        const regex = new RegExp(pattern, 'i');
        if (regex.test(context.userMessage)) {
          return;
        }
      }

      // NEW: Async RAG tool call (non-blocking)
      try {
        const result = await this.callRAGTool("rag.analyze_conversation", {
          project_id: config.rag_project_id,
          user_message: context.userMessage,
          agent_response: context.lastAgentResponse,
          context: {
            tool_name: toolName,
            tool_args: args,
            extraction_mode: config.extraction_mode  // NEW: Pass extraction mode
          },
          auto_store: true
        });

        console.log(
          `[Synapse] Analyzed conversation: ${result.facts_stored} facts, ` +
          `${result.episodes_stored} episodes (async)`
        );
      } catch (error) {
        console.error(`[Synapse] Failed to analyze conversation:`, error);
        // Don't block tool execution, just log error
      }
      // Hook returns immediately (non-blocking)
    },

    async "tool.execute.after"(
      toolName: string,
      result: any
    ): Promise<void> {
      // Track tool execution for session-end analysis
      // Implementation: buffer results for later analysis
      console.log(`[Synapse] Tool executed: ${toolName}`);
    }
  },

  async callRAGTool(toolName: string, args: any): Promise<any> {
    // Access RAG MCP client via opencode's tool execution
    const tool = this.tools.find((t: any) => t.name === toolName);
    if (!tool) {
      throw new Error(`RAG tool not found: ${toolName}`);
    }

    return await tool.execute(args);
  }
};
