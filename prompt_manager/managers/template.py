"""Template management for PromptManager."""

from pathlib import Path
from typing import Dict, Optional, List
from langchain.prompts import PromptTemplate
from ..exceptions import PromptConfigurationError, TemplateError


class TemplateManager:
    """Handles PromptTemplate creation and management."""
    
    def load_template_file(self, template_path: Path) -> str:
        """
        Load template content from file.
        
        Args:
            template_path: Path to template file
            
        Returns:
            Template content as string
            
        Raises:
            PromptConfigurationError: If template loading fails
        """
        try:
            # Check if template file exists
            if not template_path.exists():
                raise PromptConfigurationError(f"Template file not found: {template_path}")
            
            if not template_path.is_file():
                raise PromptConfigurationError(f"Template path is not a file: {template_path}")
            
            # Read template content
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Validate template syntax
            self._validate_template_syntax(content)
            
            return content
            
        except PromptConfigurationError:
            raise  # Re-raise our custom exceptions
        except UnicodeDecodeError as e:
            raise PromptConfigurationError(f"Failed to decode template file {template_path}: {e}")
        except Exception as e:
            raise PromptConfigurationError(f"Failed to load template from {template_path}: {e}")
    
    def create_template(self, template_content: str, partial_vars: Optional[Dict[str, str]] = None) -> PromptTemplate:
        """
        Create PromptTemplate instance with partial variables.
        
        Args:
            template_content: Template content string
            partial_vars: Dictionary of partial variables
            
        Returns:
            Configured PromptTemplate instance
            
        Raises:
            TemplateError: If template creation fails
        """
        try:
            # Validate template content
            if not isinstance(template_content, str):
                raise TemplateError("Template content must be a string")
            
            # Create base template
            template = PromptTemplate.from_template(template_content)
            
            # Apply partial variables if provided
            if partial_vars:
                # Validate partial variables
                self._validate_partial_variables(partial_vars, template_content)
                
                # Create template with partial variables
                template = template.partial(**partial_vars)
            
            return template
            
        except Exception as e:
            # Wrap any langchain exceptions in our custom exception
            raise TemplateError(f"Failed to create template: {e}")
    
    def load_variable_files(self, config: Dict[str, str], agent_dir: Path) -> Dict[str, str]:
        """
        Load all variable files referenced in configuration.
        
        Args:
            config: Configuration with variable file mappings
            agent_dir: Agent directory containing variable files
            
        Returns:
            Dictionary of variable name to content mappings
            
        Raises:
            PromptConfigurationError: If variable file loading fails
        """
        partial_vars = {}
        
        for var_name, filename in config.items():
            try:
                file_path = agent_dir / filename
                
                # Check if file exists
                if not file_path.exists():
                    raise PromptConfigurationError(f"Variable file not found: {filename} for variable '{var_name}'")
                
                if not file_path.is_file():
                    raise PromptConfigurationError(f"Variable path is not a file: {filename} for variable '{var_name}'")
                
                # Read file content
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Store variable content
                partial_vars[var_name] = content
                
            except PromptConfigurationError:
                raise  # Re-raise our custom exceptions
            except UnicodeDecodeError as e:
                raise PromptConfigurationError(f"Failed to decode variable file {filename} for '{var_name}': {e}")
            except Exception as e:
                raise PromptConfigurationError(f"Failed to load variable file {filename} for '{var_name}': {e}")
        
        return partial_vars
    
    def _validate_template_syntax(self, template_content: str) -> None:
        """
        Validate template syntax for common issues.
        
        Args:
            template_content: Template content to validate
            
        Raises:
            PromptConfigurationError: If template syntax is invalid
        """
        try:
            # Try to create a basic template to check syntax
            PromptTemplate.from_template(template_content)
            
        except Exception as e:
            raise PromptConfigurationError(f"Invalid template syntax: {e}")
    
    def _validate_partial_variables(self, partial_vars: Dict[str, str], template_content: str) -> None:
        """
        Validate partial variables against template content.
        
        Args:
            partial_vars: Dictionary of partial variables
            template_content: Template content to check against
            
        Raises:
            TemplateError: If partial variables are invalid
        """
        # Check that all partial variables are strings
        for var_name, var_content in partial_vars.items():
            if not isinstance(var_name, str):
                raise TemplateError(f"Variable name must be string: {var_name}")
            
            if not isinstance(var_content, str):
                raise TemplateError(f"Variable content must be string for '{var_name}': {type(var_content)}")
    
    def extract_template_variables(self, template_content: str) -> List[str]:
        """
        Extract variable names from template content.
        
        Args:
            template_content: Template content to analyze
            
        Returns:
            List of variable names found in template
            
        Raises:
            TemplateError: If template analysis fails
        """
        try:
            # Create template to extract input variables
            template = PromptTemplate.from_template(template_content)
            return list(template.input_variables)
            
        except Exception as e:
            raise TemplateError(f"Failed to extract variables from template: {e}")
    
    def validate_template_variables(self, template_content: str, available_vars: Dict[str, str]) -> Dict[str, List[str]]:
        """
        Validate that template variables are satisfied by available variables.
        
        Args:
            template_content: Template content to validate
            available_vars: Available variables (partial + runtime)
            
        Returns:
            Dictionary with 'missing' and 'unused' variable lists
            
        Raises:
            TemplateError: If validation fails
        """
        try:
            # Extract required variables from template
            required_vars = set(self.extract_template_variables(template_content))
            available_var_names = set(available_vars.keys())
            
            # Find missing and unused variables
            missing_vars = list(required_vars - available_var_names)
            unused_vars = list(available_var_names - required_vars)
            
            return {
                'missing': missing_vars,
                'unused': unused_vars
            }
            
        except Exception as e:
            raise TemplateError(f"Failed to validate template variables: {e}")
    
    def format_template_preview(self, template: PromptTemplate, sample_vars: Optional[Dict[str, str]] = None) -> str:
        """
        Generate a preview of the template with sample variables.
        
        Args:
            template: PromptTemplate instance
            sample_vars: Sample variables for preview
            
        Returns:
            Formatted template preview
            
        Raises:
            TemplateError: If preview generation fails
        """
        try:
            # Use sample variables or placeholders
            if sample_vars is None:
                sample_vars = {}
            
            # Fill missing variables with placeholders
            for var in template.input_variables:
                if var not in sample_vars:
                    sample_vars[var] = f"[{var.upper()}_PLACEHOLDER]"
            
            # Format template
            return template.format(**sample_vars)
            
        except Exception as e:
            raise TemplateError(f"Failed to generate template preview: {e}")
    
    def create_template_from_parts(self, system_content: str, user_content: str, 
                                  partial_vars: Optional[Dict[str, str]] = None) -> Dict[str, PromptTemplate]:
        """
        Create both system and user templates from content.
        
        Args:
            system_content: System message template content
            user_content: User message template content
            partial_vars: Dictionary of partial variables
            
        Returns:
            Dictionary with 'system' and 'user' PromptTemplate instances
            
        Raises:
            TemplateError: If template creation fails
        """
        try:
            return {
                'system': self.create_template(system_content, partial_vars),
                'user': self.create_template(user_content, partial_vars)
            }
            
        except Exception as e:
            raise TemplateError(f"Failed to create templates from parts: {e}")
