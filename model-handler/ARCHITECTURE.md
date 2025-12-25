# Final Architecture Solution

After reviewing the requirements carefully, here's the correct approach:

## Problem Analysis
You provided two llama-server commands both using `--port 6006`, which means they cannot run simultaneously. This creates a fundamental conflict.

## Solution Approach
Since you want to expose on port 6006 (the "expose" requirement) and need to switch models, I recommend:

1. **FastAPI Server**: Runs on port 6006 (as required for exposure)
2. **Model Switching**: Only one model runs at a time (using different internal ports)
3. **Model Management**: The server manages starting/stopping model processes

## Key Design Decision
Since both models can't use port 6006 simultaneously, I've implemented:
- FastAPI server on port 6006 (for external exposure)
- Internal llama-server processes on different ports (6007 and 6008)
- The FastAPI server acts as an API gateway that routes to the active model

## Current Implementation
The model_switcher.py now properly uses different internal ports for each model:
- Qwen model: runs on internal port 6007
- DeepSeek model: runs on internal port 6008

This allows the FastAPI server to run on port 6006 while properly managing the model processes.

The service configuration has been updated to reflect this correct architecture.