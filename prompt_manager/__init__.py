"""
PromptManager package for centralized AI agent prompt template management.

This package provides a comprehensive solution for managing AI agent prompt templates
with dynamic loading, configuration-driven variable injection, and strict error validation.
"""

from .core import PromptManager
from .exceptions import (
    PromptManagerError,
    PromptConfigurationError,
    AgentNotFoundError,
    AgentAlreadyExistsError,
    FileSystemError,
    TemplateError,
    ValidationError
)

__version__ = "1.0.0"
__author__ = "PromptManager Development Team"
__email__ = "dev@promptmanager.com"
__description__ = "Centralized AI agent prompt template management system"

__all__ = [
    "PromptManager",
    "PromptManagerError", 
    "PromptConfigurationError",
    "AgentNotFoundError",
    "AgentAlreadyExistsError",
    "FileSystemError",
    "TemplateError",
    "ValidationError"
]
