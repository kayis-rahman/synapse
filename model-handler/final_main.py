#!/usr/bin/env python3
"""
Final Working FastAPI Server for Model Switching with Proper Initialization Handling
"""

import sys
import os
import logging
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import httpx
from model_switcher import ModelSwitcher

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the model switcher
model_switcher = ModelSwitcher()

app = FastAPI(title="Model Switcher API", version="1.0.0")

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[Dict[str, Any]]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 512
    top_p: Optional[float] = 1.0
    frequency_penalty: Optional[float] = 0.0
    presence_penalty: Optional[float] = 0.0

class ChatCompletionResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Dict[str, Any]]

class ModelListResponse(BaseModel):
    object: str
    data: List[Dict[str, Any]]

@app.get("/")
async def root():
    return {
        "message": "Model Switcher API - Server is running",
        "active_model": model_switcher.get_status()["active_model"]
    }

@app.get("/models", response_model=ModelListResponse)
async def list_models():
    """List available models"""
    return {
        "object": "list",
        "data": [
            {
                "id": "Qwen3-Coder-30B-A3B",
                "object": "model",
                "created": 1677610602,
                "owned_by": "system"
            },
            {
                "id": "Deepseek-Coder-33b-Instruct",
                "object": "model",
                "created": 1677610602,
                "owned_by": "system"
            }
        ]
    }

@app.post("/chat/completions", response_model=ChatCompletionResponse)
async def chat_completions(request: ChatCompletionRequest):
    """Chat completions endpoint that makes real calls to models with proper initialization handling"""
    try:
        # Validate model name
        valid_models = ["Qwen3-Coder-30B-A3B", "Deepseek-Coder-33b-Instruct"]
        if request.model not in valid_models:
            raise HTTPException(status_code=400, detail="Invalid model specified")
        
        logger.info(f"Processing request for model: {request.model}")
        
        # Check if the requested model is available
        status = model_switcher.get_status()
        active_model = status["active_model"]
        
        # If no model is active or different model is requested, switch models
        if active_model is None:
            # Start the requested model
            success = model_switcher.start_model(request.model.lower().replace("-coder-33b-instruct", "").replace("qwen3-coder-30b-a3b", "qwen"))
            if not success:
                raise HTTPException(status_code=500, detail=f"Failed to start model {request.model}")
            active_model = request.model
        elif active_model != request.model:
            # Switch to the requested model
            success = model_switcher.switch_model(request.model.lower().replace("-coder-33b-instruct", "").replace("qwen3-coder-30b-a3b", "qwen"))
            if not success:
                raise HTTPException(status_code=500, detail=f"Failed to switch to model {request.model}")
            active_model = request.model
            
        # Get the internal model identifier for configuration
        internal_model = request.model.lower().replace("-coder-33b-instruct", "").replace("qwen3-coder-30b-a3b", "qwen")
        
        # Get the port of the currently active model
        config = model_switcher.model_configs[internal_model]
        model_port = config["port"]
        model_host = config["host"]
        
        # Use the correct llama.cpp API endpoint
        model_url = f"http://{model_host}:{model_port}/completion"
        
        # Prepare the prompt from messages
        prompt = "\n".join([msg["content"] for msg in request.messages])
        
        # Prepare the request data for llama.cpp model
        model_request_data = {
            "prompt": prompt,
            "temperature": request.temperature,
            "n_predict": request.max_tokens,
            "stop": ["\n"],
            "stream": False
        }
        
        # Make the actual HTTP request to the running model server
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(model_url, json=model_request_data, timeout=60.0)
                if response.status_code == 200:
                    model_response = response.json()
                    
                    # Extract content from the model response
                    content = model_response.get("content", model_response.get("completion", "No content"))
                    
                    # Return properly formatted response
                    return ChatCompletionResponse(
                        id="chatcmpl-1234567890",
                        object="chat.completion",
                        created=1677610602,
                        model=request.model,
                        choices=[
                            {
                                "index": 0,
                                "message": {
                                    "role": "assistant",
                                    "content": content,
                                    "tool_calls": None
                                },
                                "finish_reason": "stop"
                            }
                        ]
                    )
                else:
                    error_msg = f"Model server returned error: {response.status_code} - {response.text}"
                    logger.error(error_msg)
                    raise HTTPException(status_code=500, detail=error_msg)
        except Exception as e:
            error_msg = f"Error calling model server: {str(e)}"
            logger.error(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)
            
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/status")
async def get_status():
    """Get current model status"""
    return model_switcher.get_status()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run FastAPI server for model switching")
    parser.add_argument("--host", default="0.0.0.0", help="Host to run the server on")
    parser.add_argument("--port", type=int, default=6006, help="Port to run the server on")
    
    args = parser.parse_args()
    
    print("Starting Final Working FastAPI Server for Model Switching...")
    print(f"Server will be available at http://{args.host}:{args.port}")
    print("This server provides clean API functionality with proper model management.")
    
    # Run the FastAPI server
    uvicorn.run(
        "final_main:app",
        host=args.host,
        port=args.port,
        log_level="info"
    )