"""Utility functions for PromptManager."""

import re
from typing import Optional, Dict, Any
from pathlib import Path
from datetime import datetime


def validate_agent_name(agent_name: str) -> bool:
    """
    Validate agent name contains only allowed characters.
    
    Agent names must:
    - Be non-empty strings
    - Contain only alphanumeric characters and underscores
    - Not start with underscore or number
    - Be between 1 and 50 characters long
    
    Args:
        agent_name: The agent name to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not agent_name or not isinstance(agent_name, str):
        return False
    
    # Check length
    if len(agent_name) < 1 or len(agent_name) > 50:
        return False
    
    # Check format: alphanumeric + underscores, must start with letter
    pattern = r'^[a-zA-Z][a-zA-Z0-9_]*$'
    return bool(re.match(pattern, agent_name))


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal attacks.
    
    Removes or replaces dangerous characters and patterns.
    
    Args:
        filename: The filename to sanitize
        
    Returns:
        Sanitized filename
    """
    if not filename or not isinstance(filename, str):
        return ""
    
    # Remove path separators and dangerous characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove path traversal patterns
    sanitized = re.sub(r'\.\.', '_', sanitized)
    
    # Remove leading/trailing dots and spaces
    sanitized = sanitized.strip('. ')
    
    # Ensure not empty after sanitization
    if not sanitized:
        sanitized = "unnamed_file"
    
    return sanitized


def ensure_md_extension(filename: str) -> str:
    """
    Ensure filename has .md extension.
    
    Args:
        filename: The filename to check
        
    Returns:
        Filename with .md extension
    """
    if not filename or not isinstance(filename, str):
        return "unnamed.md"
    
    # Sanitize first
    filename = sanitize_filename(filename)
    
    # Add .md extension if not present
    if not filename.lower().endswith('.md'):
        filename += '.md'
    
    return filename


def create_error_context(operation: str, agent_name: Optional[str] = None, 
                        file_path: Optional[Path] = None, **kwargs) -> Dict[str, Any]:
    """
    Create standardized error context for debugging.
    
    Args:
        operation: The operation being performed
        agent_name: Optional agent name involved
        file_path: Optional file path involved
        **kwargs: Additional context information
        
    Returns:
        Dictionary containing error context
    """
    import platform
    
    context = {
        "operation": operation,
        "timestamp": datetime.now().isoformat(),
        "system_info": {
            "platform": platform.system(),
            "python_version": platform.python_version()
        }
    }
    
    if agent_name:
        context["agent_name"] = agent_name
    
    if file_path:
        context["file_path"] = str(file_path)
        context["file_exists"] = file_path.exists() if file_path else False
    
    # Add any additional context
    context.update(kwargs)
    
    return context


def validate_variable_name(var_name: str) -> bool:
    """
    Validate variable name format for template variables.
    
    Variable names must:
    - Be non-empty strings
    - Start with a letter
    - Contain only alphanumeric characters and underscores
    - Be between 1 and 100 characters long
    
    Args:
        var_name: Variable name to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not var_name or not isinstance(var_name, str):
        return False
    
    # Check length
    if len(var_name) < 1 or len(var_name) > 100:
        return False
    
    # Check format: must start with letter, then alphanumeric + underscores
    pattern = r'^[a-zA-Z][a-zA-Z0-9_]*$'
    return bool(re.match(pattern, var_name))
