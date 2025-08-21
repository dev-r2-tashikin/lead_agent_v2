"""Custom exception classes for PromptManager."""

from datetime import datetime
from typing import Optional, Dict, Any


class PromptManagerError(Exception):
    """Base exception for all PromptManager errors."""
    
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        """
        Initialize PromptManagerError with message and optional context.
        
        Args:
            message: Error message
            context: Optional context information for debugging
        """
        super().__init__(message)
        self.context = context or {}
        self.timestamp = datetime.now()
        
    def __str__(self) -> str:
        """Return string representation of the error."""
        base_msg = super().__str__()
        if self.context:
            context_str = ", ".join(f"{k}={v}" for k, v in self.context.items())
            return f"{base_msg} (Context: {context_str})"
        return base_msg


class PromptConfigurationError(PromptManagerError):
    """Raised when prompt configuration is invalid or incomplete."""
    pass


class AgentNotFoundError(PromptManagerError):
    """Raised when attempting to access a non-existent agent."""
    pass


class AgentAlreadyExistsError(PromptManagerError):
    """Raised when attempting to register an agent that already exists."""
    pass


class FileSystemError(PromptManagerError):
    """Raised when file system operations fail."""
    pass


class TemplateError(PromptManagerError):
    """Raised when template operations fail."""
    pass


class ValidationError(PromptManagerError):
    """Raised when validation operations fail."""
    pass
