/**
 * Synapse Auto-Learning Plugin for OpenCode
 *
 * Hooks: tool.execute.before, tool.execute.after
 * Purpose: Automatically extract facts and episodes from agent conversations
 * Mode: Heuristic extraction only (no LLM)
 *
 * Usage: Configure via rag_config.json -> universal_hooks -> adapters -> opencode
 */

import type { PluginInput, Hooks } from "@opencode-ai/plugin";

/**
 * Synapse Plugin Configuration
 */
interface SynapseConfig {
  enabled: boolean;
  priority: number;
  analyze_after_tools: string[];
  min_message_length: number;
  skip_patterns: string[];
  rag_project_id: string;
  async_processing: boolean;
  extraction_mode: string;
}

/**
 * Synapse Auto-Learning Plugin
 */
const SynapseAutoLearningPlugin = async (ctx: PluginInput): Promise<Hooks> => {
  // Load configuration
  const config: SynapseConfig = {
    enabled: true,
    priority: 1,
    analyze_after_tools: ["rag.add_fact", "rag.add_episode", "rag.search", "rag.get_context", "rag.ingest_file"],
    min_message_length: 10,
    skip_patterns: ["^test$", "^hello$", "^help$"],
    rag_project_id: "synapse",
    async_processing: true,
    extraction_mode: "heuristic"
  };

  console.log(`[Synapse] Plugin initialized (mode=${config.extraction_mode}, enabled=${config.enabled})`);

  // Return hooks object
  return {
    /**
     * Hook called before tool execution
     * Analyzes conversation after configured tools execute
     */
    "tool.execute.before": async (input, output) => {
      const startTime = Date.now();

      try {
        // Check if plugin is enabled
        if (!config.enabled) {
          return;
        }

        // Check if this tool should trigger analysis
        if (!config.analyze_after_tools.includes(input.tool)) {
          return;
        }

        console.debug(`[Synapse] tool.execute.before: tool=${input.tool}, session=${input.sessionID}`);

        // Note: We don't have direct access to user_message and agent_response here
        // The OpenCode SDK provides tool execution context, but not full conversation
        // For now, we'll log and skip analysis (can be enhanced later)

        console.log(`[Synapse] Tool ${input.tool} matched analysis list, but conversation context not yet available`);

        return;

      } catch (error) {
        const duration = Date.now() - startTime;
        console.error(`[Synapse] Error in tool.execute.before: ${error} (${duration}ms)`);
        // Never throw - allow tool to proceed
        return;
      }
    },

    /**
     * Hook called after tool execution
     * Tracks tool execution for debugging
     */
    "tool.execute.after": async (input, output) => {
      const startTime = Date.now();

      try {
        if (!config.enabled) {
          return;
        }

        console.debug(`[Synapse] tool.execute.after: tool=${input.tool}, session=${input.sessionID}`);
        console.debug(`[Synapse] Tool result: ${output.title}`);

        // For future enhancement: Could trigger analysis based on tool results
        // Currently just logging for debugging

        return;

      } catch (error) {
        const duration = Date.now() - startTime;
        console.error(`[Synapse] Error in tool.execute.after: ${error} (${duration}ms)`);
        // Never throw - allow agent to continue
        return;
      }
    }
  };
};

/**
 * Helper function to call RAG tool
 * Note: This requires access to ctx.client which is provided by OpenCode
 */
async function callRAGTool(client: any, toolName: string, args: any): Promise<any> {
  try {
    const result = await client.tools.call(toolName, args);
    return result;
  } catch (error) {
    console.error(`[Synapse] Failed to call RAG tool ${toolName}: ${error}`);
    throw error;
  }
}

/**
 * Helper function to check if message matches skip patterns
 */
function shouldSkipMessage(message: string, skipPatterns: string[]): boolean {
  for (const pattern of skipPatterns) {
    const regex = new RegExp(pattern, 'i');
    if (regex.test(message)) {
      return true;
    }
  }
  return false;
}

export default SynapseAutoLearningPlugin;
