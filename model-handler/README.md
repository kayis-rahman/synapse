# Model Switcher for LLaMA Server

This tool allows you to switch between two different models (Qwen3-Coder and DeepSeek-Coder) with their specific configurations while using port 6006.

## Features
- Switch between Qwen3-Coder and DeepSeek-Coder models
- Each model uses its specific configuration parameters
- Consistent port 6006 usage (models are started/stopped to avoid conflicts)
- API-compatible interface for both models

## Usage

### Starting a model
```bash
python model_switcher.py start --model qwen
python model_switcher.py start --model deepseek
```

### Stopping the current model
```bash
python model_switcher.py stop
```

### Switching between models
```bash
python model_switcher.py switch --model qwen
python model_switcher.py switch --model deepseek
```

### Checking status
```bash
python model_switcher.py status
```

## Model Configurations

### Qwen3-Coder-30B-A3B-Instruct-Q5_K_M.gguf
- Model Path: models/Qwen3-Coder-30B-A3B-Instruct-Q5_K_M.gguf
- Port: 6006
- Context: 131072
- NGL: 24
- Flash Attention: on
- CTK: q8_0
- CTv: q8_0
- Batch Size: 512
- UB: 512
- MLock: enabled

### deepseek-coder-33b-instruct.Q5_K_M.gguf
- Model Path: models/deepseek-coder-33b-instruct.Q5_K_M.gguf
- Port: 6006
- Context: 32768
- NGL: 49
- Flash Attention: on
- CTK: q4_0
- CTv: q4_0
- Batch Size: 512
- UB: 512
- NP: 1
- MLock: enabled

## Important Notes

1. Only one model can be active at a time since both use port 6006
2. When switching models, the current model will be stopped before starting the new one
3. The script assumes that the llama-server binary is at ./build/bin/llama-server
4. Model files must be in the specified locations as configured in the script