"""Main PromptManager class implementation."""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from langchain.prompts import PromptTemplate

from .managers.filesystem import FileSystemManager
from .managers.configuration import ConfigurationManager  
from .managers.template import TemplateManager
from .exceptions import (
    PromptConfigurationError,
    AgentNotFoundError,
    AgentAlreadyExistsError,
    FileSystemError
)
from .utils import validate_agent_name, create_error_context


class PromptManager:
    """
    Centralized manager for AI Agent prompt templates with dynamic loading
    and configuration-driven variable injection.
    """
    
    def __init__(self, store_path: str = "./prompt_store"):
        """
        Initialize PromptManager with automatic agent loading.
        
        Args:
            store_path: Path to prompt storage directory
            
        Raises:
            PromptConfigurationError: If initialization fails
        """
        try:
            # Initialize instance variables
            self.store_path = Path(store_path).resolve()
            self.prompts = {}  # Dict[str, Dict[str, PromptTemplate]]
            
            # Initialize manager components
            self.fs_manager = FileSystemManager(str(self.store_path))
            self.config_manager = ConfigurationManager()
            self.template_manager = TemplateManager()
            
            # Validate and prepare storage directory
            self._prepare_storage_directory()
            
            # Discover and load all agents
            self._discover_and_load_agents()
            
        except Exception as e:
            context = create_error_context("initialization", store_path=self.store_path)
            raise PromptConfigurationError(f"Failed to initialize PromptManager: {e}", context)
    
    def get_prompts(self, agent_name: str) -> Dict[str, PromptTemplate]:
        """
        Retrieve system and user prompt templates for an agent.
        
        Args:
            agent_name: Name of the agent
            
        Returns:
            Dictionary with 'system' and 'user' PromptTemplate instances
            
        Raises:
            AgentNotFoundError: If agent doesn't exist
        """
        if agent_name not in self.prompts:
            context = create_error_context("get_prompts", agent_name=agent_name)
            raise AgentNotFoundError(f"Agent '{agent_name}' not found", context)
        
        return self.prompts[agent_name].copy()  # Return copy to prevent modification
    
    def register_new_agent(self, agent_name: str, system_message: str, 
                          user_message: str = "", **kwargs) -> None:
        """
        Register a new agent with prompt templates and variables.
        
        Args:
            agent_name: Name for the new agent
            system_message: System message template content
            user_message: User message template content (optional)
            **kwargs: Variable name to content mappings
            
        Raises:
            AgentAlreadyExistsError: If agent already exists
            PromptConfigurationError: If registration fails
        """
        try:
            # Validate inputs (let ValueError propagate directly)
            self._validate_registration_inputs(agent_name, system_message, user_message, kwargs)

            # Check agent doesn't already exist
            if agent_name in self.prompts:
                context = create_error_context("register_new_agent", agent_name=agent_name)
                raise AgentAlreadyExistsError(f"Agent '{agent_name}' already exists", context)

            agent_dir = self.store_path / agent_name
            if self.fs_manager.directory_exists(agent_dir):
                context = create_error_context("register_new_agent", agent_name=agent_name, file_path=agent_dir)
                raise AgentAlreadyExistsError(f"Agent directory already exists: {agent_dir}", context)

            # Prepare all files and configuration
            files_to_create = self._prepare_agent_files(agent_name, system_message, user_message, kwargs)

            # Create agent files atomically
            self._create_agent_files_atomic(agent_dir, files_to_create)

            # Load agent into memory
            self._load_agent(agent_name)

        except (ValueError, AgentAlreadyExistsError, PromptConfigurationError):
            raise  # Re-raise validation and custom exceptions directly
        except Exception as e:
            context = create_error_context("register_new_agent", agent_name=agent_name)
            raise PromptConfigurationError(f"Failed to register agent '{agent_name}': {e}", context)
    
    def delete_agent(self, agent_name: str) -> None:
        """
        Delete an agent and all its associated files.
        
        Args:
            agent_name: Name of agent to delete
            
        Raises:
            AgentNotFoundError: If agent doesn't exist
        """
        try:
            # Validate agent exists
            if agent_name not in self.prompts:
                context = create_error_context("delete_agent", agent_name=agent_name)
                raise AgentNotFoundError(f"Agent '{agent_name}' not found", context)
            
            agent_dir = self.store_path / agent_name
            
            # Remove from memory first (fail fast if invalid)
            agent_prompts = self.prompts.pop(agent_name)
            
            # Delete directory and files
            try:
                self.fs_manager.delete_directory(agent_dir)
            except FileSystemError as e:
                # Restore in-memory state on file system failure
                self.prompts[agent_name] = agent_prompts
                context = create_error_context("delete_agent", agent_name=agent_name, file_path=agent_dir)
                raise PromptConfigurationError(f"Failed to delete agent '{agent_name}': {e}", context)
                
        except (AgentNotFoundError, PromptConfigurationError):
            raise  # Re-raise our custom exceptions
        except Exception as e:
            context = create_error_context("delete_agent", agent_name=agent_name)
            raise PromptConfigurationError(f"Unexpected error deleting agent '{agent_name}': {e}", context)
    
    def list_agents(self) -> List[str]:
        """
        List all registered agent names.
        
        Returns:
            List of agent names
        """
        return sorted(self.prompts.keys())
    
    def reload_agent(self, agent_name: str) -> None:
        """
        Reload a specific agent's configuration and templates.
        
        Args:
            agent_name: Name of agent to reload
            
        Raises:
            AgentNotFoundError: If agent doesn't exist
            PromptConfigurationError: If reload fails
        """
        try:
            # Validate agent exists
            if agent_name not in self.prompts:
                context = create_error_context("reload_agent", agent_name=agent_name)
                raise AgentNotFoundError(f"Agent '{agent_name}' not found", context)
            
            # Store current state for rollback
            old_prompts = self.prompts[agent_name].copy()
            
            # Remove from memory
            del self.prompts[agent_name]
            
            # Reload from disk
            try:
                self._load_agent(agent_name)
            except Exception as e:
                # Rollback on failure
                self.prompts[agent_name] = old_prompts
                context = create_error_context("reload_agent", agent_name=agent_name)
                raise PromptConfigurationError(f"Failed to reload agent '{agent_name}': {e}", context)
                
        except (AgentNotFoundError, PromptConfigurationError):
            raise  # Re-raise our custom exceptions
        except Exception as e:
            context = create_error_context("reload_agent", agent_name=agent_name)
            raise PromptConfigurationError(f"Unexpected error reloading agent '{agent_name}': {e}", context)
    
    def agent_exists(self, agent_name: str) -> bool:
        """
        Check if agent exists.
        
        Args:
            agent_name: Name of agent to check
            
        Returns:
            True if agent exists, False otherwise
        """
        return agent_name in self.prompts
    
    def get_agent_info(self, agent_name: str) -> Dict[str, Any]:
        """
        Get detailed information about an agent.
        
        Args:
            agent_name: Name of agent
            
        Returns:
            Dictionary with agent information
            
        Raises:
            AgentNotFoundError: If agent doesn't exist
        """
        if agent_name not in self.prompts:
            context = create_error_context("get_agent_info", agent_name=agent_name)
            raise AgentNotFoundError(f"Agent '{agent_name}' not found", context)
        
        try:
            agent_dir = self.store_path / agent_name
            config_path = agent_dir / "config.json"
            
            # Load configuration
            config = self.config_manager.load_config(config_path)
            
            # Get file stats
            system_path = agent_dir / "system_message.md"
            user_path = agent_dir / "user_message.md"
            
            return {
                "name": agent_name,
                "directory": str(agent_dir),
                "variables": list(config.keys()),
                "system_template_size": system_path.stat().st_size if system_path.exists() else 0,
                "user_template_size": user_path.stat().st_size if user_path.exists() else 0,
                "config_file": str(config_path),
                "last_modified": max(
                    system_path.stat().st_mtime if system_path.exists() else 0,
                    user_path.stat().st_mtime if user_path.exists() else 0,
                    config_path.stat().st_mtime if config_path.exists() else 0
                )
            }
            
        except Exception as e:
            context = create_error_context("get_agent_info", agent_name=agent_name)
            raise PromptConfigurationError(f"Failed to get info for agent '{agent_name}': {e}", context)

    def _prepare_storage_directory(self) -> None:
        """Prepare the prompt storage directory."""
        try:
            # Check if store directory exists
            if not self.store_path.exists():
                # Create empty store directory
                self._initialize_empty_store()
                return

            # Validate existing directory
            if not self.store_path.is_dir():
                raise PromptConfigurationError(
                    f"Store path exists but is not a directory: {self.store_path}"
                )

            # Check directory permissions
            if not os.access(self.store_path, os.R_OK | os.W_OK):
                raise PromptConfigurationError(
                    f"Insufficient permissions for store directory: {self.store_path}"
                )

        except PromptConfigurationError:
            raise  # Re-raise our custom exceptions
        except Exception as e:
            context = create_error_context("prepare_storage_directory", file_path=self.store_path)
            raise PromptConfigurationError(f"Failed to prepare storage directory: {e}", context)

    def _discover_and_load_agents(self) -> None:
        """Discover and load all agents in the store directory."""
        try:
            # Get list of subdirectories (potential agents)
            subdirs = self.fs_manager.list_subdirectories(self.store_path)

            # Load each agent
            loaded_count = 0
            failed_agents = []

            for agent_name in subdirs:
                try:
                    # Validate agent name
                    if not validate_agent_name(agent_name):
                        failed_agents.append((agent_name, "Invalid agent name format"))
                        continue

                    # Load agent
                    self._load_agent(agent_name)
                    loaded_count += 1

                except PromptConfigurationError as e:
                    # Log error but continue with other agents
                    failed_agents.append((agent_name, str(e)))
                    continue

            # Report results
            if failed_agents:
                error_msg = f"Failed to load {len(failed_agents)} agents: "
                error_details = [f"{name}: {error}" for name, error in failed_agents]
                # Log warning but don't fail initialization
                print(f"Warning: {error_msg}{'; '.join(error_details)}")

            print(f"PromptManager initialized with {loaded_count} agents")

        except FileSystemError as e:
            context = create_error_context("discover_and_load_agents", file_path=self.store_path)
            raise PromptConfigurationError(f"Failed to scan store directory: {e}", context)
        except Exception as e:
            context = create_error_context("discover_and_load_agents", file_path=self.store_path)
            raise PromptConfigurationError(f"Unexpected error during agent discovery: {e}", context)

    def _load_agent(self, agent_name: str) -> None:
        """Load a single agent's configuration and templates."""
        try:
            agent_dir = self.store_path / agent_name

            # Validate agent directory structure
            self._validate_agent_directory(agent_dir)

            # Load and validate configuration
            config_path = agent_dir / "config.json"
            config = self.config_manager.load_config(config_path)
            self.config_manager.validate_config(config, agent_dir)

            # Load variable files
            partial_vars = self.template_manager.load_variable_files(config, agent_dir)

            # Load template files
            system_template_path = agent_dir / "system_message.md"
            user_template_path = agent_dir / "user_message.md"

            system_content = self.template_manager.load_template_file(system_template_path)
            user_content = self.template_manager.load_template_file(user_template_path)

            # Create PromptTemplate instances
            system_template = self.template_manager.create_template(system_content, partial_vars)
            user_template = self.template_manager.create_template(user_content, partial_vars)

            # Store in memory
            self.prompts[agent_name] = {
                "system": system_template,
                "user": user_template
            }

        except Exception as e:
            context = create_error_context("load_agent", agent_name=agent_name, file_path=agent_dir)
            raise PromptConfigurationError(f"Failed to load agent '{agent_name}': {e}", context)

    def _validate_agent_directory(self, agent_dir: Path) -> None:
        """Validate agent directory has all required files."""
        required_files = [
            "config.json",
            "system_message.md",
            "user_message.md"
        ]

        # Check directory exists
        if not agent_dir.exists():
            raise PromptConfigurationError(f"Agent directory not found: {agent_dir}")

        if not agent_dir.is_dir():
            raise PromptConfigurationError(f"Agent path is not a directory: {agent_dir}")

        # Check required files exist
        missing_files = []
        for filename in required_files:
            file_path = agent_dir / filename
            if not self.fs_manager.file_exists(file_path):
                missing_files.append(filename)

        if missing_files:
            raise PromptConfigurationError(
                f"Agent {agent_dir.name} missing required files: {', '.join(missing_files)}"
            )

    def _initialize_empty_store(self) -> None:
        """Initialize empty prompt store directory."""
        try:
            # Create store directory
            self.fs_manager.ensure_directory(self.store_path)

            # Create .gitkeep file to preserve directory in git
            gitkeep_path = self.store_path / ".gitkeep"
            self.fs_manager.write_file(gitkeep_path, "")

            print(f"Initialized empty prompt store at: {self.store_path}")

        except FileSystemError as e:
            context = create_error_context("initialize_empty_store", file_path=self.store_path)
            raise PromptConfigurationError(f"Failed to initialize empty store: {e}", context)

    def _validate_registration_inputs(self, agent_name: str, system_message: str,
                                     user_message: str, kwargs: Dict[str, Any]) -> None:
        """Validate all inputs for agent registration."""
        # Validate agent name
        if not agent_name or not isinstance(agent_name, str):
            raise ValueError("Agent name must be a non-empty string")

        if not validate_agent_name(agent_name):
            raise ValueError(f"Invalid agent name format: {agent_name}")

        # Validate system message
        if not system_message or not isinstance(system_message, str):
            raise ValueError("System message must be a non-empty string")

        if len(system_message.strip()) == 0:
            raise ValueError("System message cannot be empty or whitespace only")

        # Validate user message
        if not isinstance(user_message, str):
            raise ValueError("User message must be a string")

        # Validate variable arguments
        for var_name, var_content in kwargs.items():
            if not isinstance(var_name, str) or not var_name:
                raise ValueError(f"Variable name must be non-empty string: {var_name}")

            if not isinstance(var_content, str):
                raise ValueError(f"Variable content must be string for '{var_name}'")

            # Validate variable name format
            from .utils import validate_variable_name
            if not validate_variable_name(var_name):
                raise ValueError(f"Invalid variable name format: {var_name}")

    def _prepare_agent_files(self, agent_name: str, system_message: str,
                            user_message: str, kwargs: Dict[str, str]) -> Dict[str, str]:
        """Prepare all files and configuration for agent creation."""
        files_to_create = {}
        config_data = {}

        # Prepare template files
        files_to_create["system_message.md"] = system_message
        files_to_create["user_message.md"] = user_message

        # Prepare variable files
        for var_name, var_content in kwargs.items():
            filename = f"{var_name}.md"
            files_to_create[filename] = var_content
            config_data[var_name] = filename

        # Prepare configuration file
        files_to_create["config.json"] = json.dumps(config_data, indent=2, ensure_ascii=False)

        return files_to_create

    def _create_agent_files_atomic(self, agent_dir: Path, files_to_create: Dict[str, str]) -> None:
        """Create all agent files atomically."""
        # Create agent directory
        self.fs_manager.ensure_directory(agent_dir)

        created_files = []
        try:
            # Create all files
            for filename, content in files_to_create.items():
                file_path = agent_dir / filename
                self.fs_manager.write_file(file_path, content)
                created_files.append(file_path)

        except Exception as e:
            # Cleanup created files on failure
            for file_path in created_files:
                try:
                    if file_path.exists():
                        file_path.unlink()
                except:
                    pass  # Best effort cleanup

            # Remove directory if empty
            try:
                if agent_dir.exists():
                    agent_dir.rmdir()
            except:
                pass  # Best effort cleanup

            raise e
