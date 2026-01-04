/**
 * Standard interface for hook-based auto-learning.
 *
 * All agent adapters must implement these methods.
 *
 * Design Principles:
 * - Language-agnostic (Python, TypeScript, Bash, REST)
 * - Graceful degradation (never crash agents)
 * - Async-ready (supports both sync and async)
 * - Zero agent lock-in (hooks only, no agent code modification)
 */

export interface UniversalHookInterface {
  /**
   * Called before tool execution.
   *
   * @param params - Hook parameters
   * @returns Promise resolving to undefined (allow execution) or dict with:
   *   - block: boolean (if true, block tool execution)
   *   - message: string (reason for blocking)
   *   - analyzeNow: boolean (trigger immediate analysis)
   */
  preToolUse?(params: {
    toolName: string;
    arguments: any;
    userMessage: string;
    agentResponse?: string;
  }): Promise<{
    block?: boolean;
    message?: string;
    analyzeNow?: boolean;
  } | undefined>;

  /**
   * Called after tool execution.
   *
   * @param params - Hook parameters
   * @returns Promise resolving to dict with:
   *   - analyze: boolean (should analyze conversation)
   *   - context: any (additional context for analysis)
   */
  postToolUse?(params: {
    toolName: string;
    result: any;
    userMessage: string;
    agentResponse: string;
  }): Promise<{
    analyze?: boolean;
    context?: any;
  }>;

  /**
   * Called when session starts.
   *
   * @returns Promise resolving to dict with initialization config
   */
  sessionStart?(): Promise<any>;

  /**
   * Called when session ends.
   *
   * @returns Promise resolving to dict with final actions (batch analysis, cleanup, etc.)
   */
  sessionEnd?(): Promise<any>;

  /**
   * Called when user submits prompt.
   *
   * @param prompt - User's submitted prompt
   * @returns Promise resolving to dict with context injection or modifications
   */
  userPromptSubmit?(prompt: string): Promise<any>;
}

export default UniversalHookInterface;
