"""Configuration management for PromptManager."""

import json
from pathlib import Path
from typing import Dict, List
from ..exceptions import PromptConfigurationError
from ..utils import validate_variable_name


class ConfigurationManager:
    """Handles configuration file operations."""
    
    def load_config(self, config_path: Path) -> Dict[str, str]:
        """
        Load and parse configuration file.
        
        Args:
            config_path: Path to config.json file
            
        Returns:
            Dictionary of variable mappings
            
        Raises:
            PromptConfigurationError: If config loading or parsing fails
        """
        try:
            # Check if config file exists
            if not config_path.exists():
                raise PromptConfigurationError(f"Configuration file not found: {config_path}")
            
            if not config_path.is_file():
                raise PromptConfigurationError(f"Configuration path is not a file: {config_path}")
            
            # Read and parse JSON
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # Validate configuration structure
            self._validate_config_structure(config_data)
            
            return config_data
            
        except json.JSONDecodeError as e:
            raise PromptConfigurationError(f"Invalid JSON in config file {config_path}: {e}")
        except PromptConfigurationError:
            raise  # Re-raise our custom exceptions
        except Exception as e:
            raise PromptConfigurationError(f"Failed to load config from {config_path}: {e}")
    
    def validate_config(self, config: Dict[str, str], agent_dir: Path) -> None:
        """
        Validate configuration structure and referenced files.
        
        Args:
            config: Configuration dictionary to validate
            agent_dir: Agent directory path for file validation
            
        Raises:
            PromptConfigurationError: If validation fails
        """
        # Validate basic structure
        self._validate_config_structure(config)
        
        # Validate referenced files exist
        self._validate_referenced_files(config, agent_dir)
    
    def save_config(self, config_path: Path, config: Dict[str, str]) -> None:
        """
        Save configuration to file.
        
        Args:
            config_path: Path to save config.json
            config: Configuration dictionary to save
            
        Raises:
            PromptConfigurationError: If config saving fails
        """
        try:
            # Validate configuration before saving
            self._validate_config_structure(config)
            
            # Ensure parent directory exists
            config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write configuration to file
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
                
        except PromptConfigurationError:
            raise  # Re-raise our custom exceptions
        except Exception as e:
            raise PromptConfigurationError(f"Failed to save config to {config_path}: {e}")
    
    def _validate_config_structure(self, config: Dict) -> None:
        """
        Validate basic configuration structure.
        
        Args:
            config: Configuration to validate
            
        Raises:
            PromptConfigurationError: If structure is invalid
        """
        # Must be a dictionary
        if not isinstance(config, dict):
            raise PromptConfigurationError("Configuration must be a JSON object (dictionary)")
        
        # Validate each key-value pair
        for key, value in config.items():
            # Key must be a valid variable name
            if not isinstance(key, str) or not key:
                raise PromptConfigurationError(f"Configuration key must be non-empty string: {key}")
            
            if not validate_variable_name(key):
                raise PromptConfigurationError(f"Invalid variable name format: {key}")
            
            # Value must be a string (filename)
            if not isinstance(value, str) or not value:
                raise PromptConfigurationError(f"Configuration value must be non-empty string for key '{key}': {value}")
            
            # Value should be a valid filename (basic check)
            if '/' in value or '\\' in value:
                raise PromptConfigurationError(f"Configuration value should be filename only, not path for key '{key}': {value}")
    
    def _validate_referenced_files(self, config: Dict[str, str], agent_dir: Path) -> None:
        """
        Validate all files referenced in configuration exist.
        
        Args:
            config: Configuration with file references
            agent_dir: Agent directory to check files in
            
        Raises:
            PromptConfigurationError: If referenced files don't exist
        """
        missing_files = []
        
        for var_name, filename in config.items():
            file_path = agent_dir / filename
            
            if not file_path.exists():
                missing_files.append(f"Variable '{var_name}' references missing file: {filename}")
            elif not file_path.is_file():
                missing_files.append(f"Variable '{var_name}' references non-file path: {filename}")
        
        if missing_files:
            raise PromptConfigurationError(f"Configuration validation failed:\n" + "\n".join(missing_files))
    
    def create_default_config(self) -> Dict[str, str]:
        """
        Create a default empty configuration.
        
        Returns:
            Empty configuration dictionary
        """
        return {}
    
    def add_variable_mapping(self, config: Dict[str, str], var_name: str, filename: str) -> Dict[str, str]:
        """
        Add a variable mapping to configuration.
        
        Args:
            config: Existing configuration
            var_name: Variable name
            filename: File name for the variable
            
        Returns:
            Updated configuration
            
        Raises:
            PromptConfigurationError: If variable name or filename is invalid
        """
        # Validate variable name
        if not validate_variable_name(var_name):
            raise PromptConfigurationError(f"Invalid variable name: {var_name}")
        
        # Validate filename
        if not isinstance(filename, str) or not filename:
            raise PromptConfigurationError(f"Filename must be non-empty string: {filename}")
        
        if '/' in filename or '\\' in filename:
            raise PromptConfigurationError(f"Filename should not contain path separators: {filename}")
        
        # Create new configuration with added mapping
        new_config = config.copy()
        new_config[var_name] = filename
        
        return new_config
    
    def remove_variable_mapping(self, config: Dict[str, str], var_name: str) -> Dict[str, str]:
        """
        Remove a variable mapping from configuration.
        
        Args:
            config: Existing configuration
            var_name: Variable name to remove
            
        Returns:
            Updated configuration
        """
        new_config = config.copy()
        new_config.pop(var_name, None)  # Remove if exists, ignore if not
        return new_config
    
    def get_variable_filename(self, config: Dict[str, str], var_name: str) -> str:
        """
        Get filename for a variable from configuration.
        
        Args:
            config: Configuration dictionary
            var_name: Variable name to look up
            
        Returns:
            Filename for the variable
            
        Raises:
            PromptConfigurationError: If variable not found in configuration
        """
        if var_name not in config:
            raise PromptConfigurationError(f"Variable '{var_name}' not found in configuration")
        
        return config[var_name]
    
    def list_variables(self, config: Dict[str, str]) -> List[str]:
        """
        List all variable names in configuration.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            List of variable names
        """
        return sorted(config.keys())
