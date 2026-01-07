"""
SYNAPSE Configuration Module

Provides centralized configuration management with:
- Auto-detection of paths and environment
- Configuration layering (defaults < config files < env vars < CLI args)
- Validation and error handling
"""

from synapse.config.defaults import (
    DEFAULT_CONFIG,
    get_config,
    load_config_file,
    apply_environment_variables,
    validate_config,
    print_config_summary,
    detect_data_directory,
    detect_models_directory,
    detect_environment
)

__all__ = [
    "DEFAULT_CONFIG",
    "get_config",
    "load_config_file",
    "apply_environment_variables",
    "validate_config",
    "print_config_summary",
    "detect_data_directory",
    "detect_models_directory",
    "detect_environment"
]
