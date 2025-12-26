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
from model_switcher import ModelSwitcher

# Configure logging
logging.basicConfig(level=logging.DEBUG)
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
        logger.debug(f"Received request for model: {request.model}")
        logger.debug(f"Request data: {request.dict()}")
        
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
        logger.debug(f"Mapped to internal model: {internal_model}")
        
        # Check if the requested model is available
        status = model_switcher.get_status()
        active_model = status["active_model"]
        logger.debug(f"Current active model: {active_model}")
        
        if active_model is None:
            # If no model is active, start the requested model
            logger.debug(f"Starting model: {internal_model}")
            success = model_switcher.start_model(internal_model)
            if not success:
                error_msg = f"Failed to start model {internal_model}"
                logger.error(error_msg)
                raise HTTPException(status_code=500, detail=error_msg)
            active_model = internal_model
        else:
            # Check if we need to switch models
            if active_model != internal_model:
                logger.debug(f"Switching from {active_model} to {internal_model}")
                success = model_switcher.switch_model(internal_model)
                if not success:
                    error_msg = f"Failed to switch models from {active_model} to {internal_model}"
                    logger.error(error_msg)
                    raise HTTPException(status_code=500, detail=error_msg)
                active_model = internal_model
            
        logger.debug(f"Model {internal_model} is active, returning response")
        
        # For demonstration purposes, we'll return a mock response
        # In a real implementation, you would make an actual API call to the running model
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
                        "content": f"Response from {request.model} model. This is a demo response since the actual model calls require additional setup. The model is now active: {request.model}",
                        "tool_calls": None
                    },
                    "finish_reason": "stop"
                }
            ]
        )
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.post("/models/{model_name}/switch")
async def switch_model(model_name: str):
    """Switch to a different model"""
    try:
        logger.debug(f"Received switch request for model: {model_name}")
        
        model_mapping = {
            "Qwen3-Coder-30B-A3B": "qwen",
            "Deepseek-Coder-33b-Instruct": "deepseek"
        }
        
        if model_name not in model_mapping:
            error_msg = f"Invalid model name specified: {model_name}"
            logger.error(error_msg)
            raise HTTPException(status_code=400, detail=error_msg)
        
        internal_model = model_mapping[model_name]
        logger.debug(f"Mapped to internal model: {internal_model}")
        
        success = model_switcher.switch_model(internal_model)
        if not success:
            error_msg = f"Failed to switch model to {internal_model}"
            logger.error(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)
        
        logger.debug(f"Successfully switched to model: {internal_model}")
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