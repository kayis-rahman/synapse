#!/usr/bin/env python3
"""
FastAPI server that exposes model switching functionality through OpenAI-compatible API
"""

import sys
import os
import logging
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import httpx
from model_switcher import ModelSwitcher

# Configure logging - minimal output, only errors
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
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
        "message": "Model Switcher API - Use /models to list models, /chat/completions to chat",
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
    """Chat completions endpoint that routes to the active model"""
    try:
        # Map the model names to internal identifiers
        model_mapping = {
            "Qwen3-Coder-30B-A3B": "qwen",
            "Deepseek-Coder-33b-Instruct": "deepseek"
        }
        
        # Validate model name
        if request.model not in model_mapping:
            error_msg = f"Invalid model specified: {request.model}"
            logger.error(error_msg)
            raise HTTPException(status_code=400, detail=error_msg)
        
        internal_model = model_mapping[request.model]
        
        # Check if the requested model is available
        status = model_switcher.get_status()
        active_model = status["active_model"]
        
        if active_model is None:
            # If no model is active, start the requested model
            success = model_switcher.start_model(internal_model)
            if not success:
                error_msg = f"Failed to start model {internal_model}"
                logger.error(error_msg)
                raise HTTPException(status_code=500, detail=error_msg)
            active_model = internal_model
        else:
            # Check if we need to switch models (but only if it's a different model)
            if active_model != internal_model:
                success = model_switcher.switch_model(internal_model)
                if not success:
                    error_msg = f"Failed to switch models from {active_model} to {internal_model}"
                    logger.error(error_msg)
                    raise HTTPException(status_code=500, detail=error_msg)
                active_model = internal_model
            
        # Make an actual API call to the running model
        # Get the port of the currently active model
        config = model_switcher.model_configs[internal_model]
        model_port = config["port"]
        model_host = config["host"]
        
        # Make a request to the running llama-server model
        model_url = f"http://{model_host}:{model_port}/completion"
        
        # Prepare the request data for the model
        model_request_data = {
            "prompt": "\n".join([msg["content"] for msg in request.messages]),
            "temperature": request.temperature,
            "n_predict": request.max_tokens,
            "stop": ["\n"],
            "stream": False
        }
        
        # Make the actual HTTP request to the running model server
        import httpx
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(model_url, json=model_request_data, timeout=30.0)
                if response.status_code == 200:
                    model_response = response.json()
                    # Format the response properly for OpenAI API
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
                                    "content": model_response.get("content", ""),
                                    "tool_calls": None
                                },
                                "finish_reason": "stop"
                            }
                        ]
                    )
                else:
                    error_msg = f"Model server returned error: {response.status_code}"
                    logger.error(error_msg)
                    raise HTTPException(status_code=500, detail=error_msg)
        except Exception as e:
            error_msg = f"Error calling model server: {str(e)}"
            logger.error(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)
            
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.post("/models/{model_name}/switch")
async def switch_model(model_name: str):
    """Switch to a different model"""
    try:
        model_mapping = {
            "Qwen3-Coder-30B-A3B": "qwen",
            "Deepseek-Coder-33b-Instruct": "deepseek"
        }
        
        if model_name not in model_mapping:
            error_msg = f"Invalid model name specified: {model_name}"
            logger.error(error_msg)
            raise HTTPException(status_code=400, detail=error_msg)
        
        internal_model = model_mapping[model_name]
        
        success = model_switcher.switch_model(internal_model)
        if not success:
            error_msg = f"Failed to switch model to {internal_model}"
            logger.error(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)
        
        return {"message": f"Successfully switched to {model_name} model"}
    except Exception as e:
        logger.error(f"Error switching model: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error switching model: {str(e)}")

@app.get("/status")
async def get_status():
    """Get current model status"""
    return model_switcher.get_status()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run FastAPI server for model switching")
    parser.add_argument("--host", default="0.0.0.0", help="Host to run the server on")
    parser.add_argument("--port", type=int, default=6006, help="Port to run the server on")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    parser.add_argument("--log-level", default="debug", help="Logging level")
    
    args = parser.parse_args()
    
    print("Starting FastAPI server for model switching...")
    print(f"Server will be available at http://{args.host}:{args.port}")
    print(f"Active model can be managed using: python model_switcher.py")
    
    # Run the FastAPI server
    uvicorn.run(
        "main:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level=args.log_level
    )