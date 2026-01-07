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

   // Only log initialization in debug mode to reduce noise
   console.debug(
     `[Synapse] Plugin initialized`, {
       mode: config.extraction_mode,
       enabled: config.enabled,
       project_id: config.rag_project_id,
       priority: config.priority,
       analyze_after_tools: config.analyze_after_tools,
       analyze_after_tools_count: config.analyze_after_tools.length,
       min_message_length: config.min_message_length,
       skip_patterns: config.skip_patterns,
       skip_patterns_count: config.skip_patterns.length,
       async_processing: config.async_processing
     }
   );

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

         // Get user message if available from SDK
         const userMessage = (input as any).userMessage || (input as any).message || "";
         const lastAgentResponse = (input as any).lastAgentResponse || (input as any).agentResponse || "";

         // Apply min_message_length filter
         if (userMessage.length > 0 && userMessage.length < config.min_message_length) {
           console.debug(
             `[Synapse] Skipping message (too short: ${userMessage.length} < ${config.min_message_length})`
           );
           return;
         }

         console.debug(`[Synapse] Processing message (${userMessage.length} chars)`);

         // Apply skip_patterns filter
         for (const pattern of config.skip_patterns) {
           try {
             const regex = new RegExp(pattern, 'i');
              if (regex.test(userMessage)) {
                console.debug(
                  `[Synapse] Skipping message (matched skip pattern: "${pattern}")`
                );
                return;
              }
           } catch (error) {
             console.error(
               `[Synapse] Invalid skip pattern: "${pattern}" - ${error}`
             );
             // Continue with next pattern instead of failing
           }
         }

         console.debug(`[Synapse] tool.execute.before: tool=${input.tool}, session=${input.sessionID}`);

         // Try to call RAG tool if we have context
         try {
           if (userMessage.length > 0 || lastAgentResponse.length > 0) {
             const result = await ctx.tools.call("rag.analyze_conversation", {
               project_id: config.rag_project_id,
               user_message: userMessage,
               agent_response: lastAgentResponse,
               context: {
                 tool_name: input.tool,
                 tool_arguments: input.arguments,
                 timestamp: new Date().toISOString()
               },
               auto_store: true,
               extraction_mode: config.extraction_mode,
               return_only: false
             });

              console.debug(
                `[Synapse] Analyzed conversation: ` +
                `${result.facts_stored} facts, ${result.episodes_stored} episodes`
              );
            } else {
              console.debug(`[Synapse] No conversation context available for analysis`);
            }
         } catch (ragError: any) {
           const ragDuration = Date.now() - startTime;
           console.error(
             `[Synapse] RAG tool call failed: ${ragError.message || ragError} (${ragDuration}ms)`
           );
            console.debug("[Synapse] Continuing without analysis (graceful degradation)");
           // Don't rethrow - allow tool to proceed
         }

         const duration = Date.now() - startTime;
         if (duration > 50) {
           console.warn(
             `[Synapse] Slow hook execution: ${duration}ms (threshold: 50ms)`
           );
         } else {
           console.debug(`[Synapse] Hook execution time: ${duration}ms`);
         }

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

         console.debug(
           `[Synapse] tool.execute.after:`, {
             tool: input.tool,
             session_id: input.sessionID,
             result_title: output.title,
             result_status: output.status
           }
         );

         const duration = Date.now() - startTime;
         console.debug(`[Synapse] tool.execute.after execution time: ${duration}ms`);

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
