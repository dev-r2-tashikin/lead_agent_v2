"""File system operations manager."""

import os
import shutil
from pathlib import Path
from typing import List
from ..exceptions import FileSystemError


class FileSystemManager:
    """Handles all file system operations for PromptManager."""
    
    def __init__(self, base_path: str):
        """
        Initialize FileSystemManager.
        
        Args:
            base_path: Base directory path for prompt storage
        """
        self.base_path = Path(base_path).resolve()
    
    def ensure_directory(self, path: Path) -> None:
        """
        Ensure directory exists, create if necessary.
        
        Args:
            path: Directory path to ensure
            
        Raises:
            FileSystemError: If directory creation fails
        """
        try:
            # Resolve path to prevent directory traversal
            resolved_path = path.resolve()
            
            # Ensure path is within base_path for security
            if not str(resolved_path).startswith(str(self.base_path)):
                raise FileSystemError(f"Path outside base directory: {resolved_path}")
            
            # Create directory if it doesn't exist
            resolved_path.mkdir(parents=True, exist_ok=True)
            
        except OSError as e:
            raise FileSystemError(f"Failed to create directory {path}: {e}")
        except Exception as e:
            raise FileSystemError(f"Unexpected error creating directory {path}: {e}")
    
    def read_file(self, file_path: Path) -> str:
        """
        Read content from file.
        
        Args:
            file_path: Path to file to read
            
        Returns:
            File content as string
            
        Raises:
            FileSystemError: If file reading fails
        """
        try:
            # Resolve path to prevent directory traversal
            resolved_path = file_path.resolve()
            
            # Ensure path is within base_path for security
            if not str(resolved_path).startswith(str(self.base_path)):
                raise FileSystemError(f"Path outside base directory: {resolved_path}")
            
            # Check if file exists
            if not resolved_path.exists():
                raise FileSystemError(f"File not found: {file_path}")
            
            if not resolved_path.is_file():
                raise FileSystemError(f"Path is not a file: {file_path}")
            
            # Read file content
            with open(resolved_path, 'r', encoding='utf-8') as f:
                return f.read()
                
        except FileSystemError:
            raise  # Re-raise our custom exceptions
        except OSError as e:
            raise FileSystemError(f"Failed to read file {file_path}: {e}")
        except UnicodeDecodeError as e:
            raise FileSystemError(f"Failed to decode file {file_path}: {e}")
        except Exception as e:
            raise FileSystemError(f"Unexpected error reading file {file_path}: {e}")
    
    def write_file(self, file_path: Path, content: str) -> None:
        """
        Write content to file.
        
        Args:
            file_path: Path to file to write
            content: Content to write
            
        Raises:
            FileSystemError: If file writing fails
        """
        try:
            # Resolve path to prevent directory traversal
            resolved_path = file_path.resolve()
            
            # Ensure path is within base_path for security
            if not str(resolved_path).startswith(str(self.base_path)):
                raise FileSystemError(f"Path outside base directory: {resolved_path}")
            
            # Ensure parent directory exists
            resolved_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file content
            with open(resolved_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
        except FileSystemError:
            raise  # Re-raise our custom exceptions
        except OSError as e:
            raise FileSystemError(f"Failed to write file {file_path}: {e}")
        except Exception as e:
            raise FileSystemError(f"Unexpected error writing file {file_path}: {e}")
    
    def delete_directory(self, dir_path: Path) -> None:
        """
        Delete directory and all contents.
        
        Args:
            dir_path: Directory path to delete
            
        Raises:
            FileSystemError: If directory deletion fails
        """
        try:
            # Resolve path to prevent directory traversal
            resolved_path = dir_path.resolve()
            
            # Ensure path is within base_path for security
            if not str(resolved_path).startswith(str(self.base_path)):
                raise FileSystemError(f"Path outside base directory: {resolved_path}")
            
            # Check if directory exists
            if not resolved_path.exists():
                return  # Already deleted, nothing to do
            
            if not resolved_path.is_dir():
                raise FileSystemError(f"Path is not a directory: {dir_path}")
            
            # Delete directory and all contents
            shutil.rmtree(resolved_path)
            
        except FileSystemError:
            raise  # Re-raise our custom exceptions
        except OSError as e:
            raise FileSystemError(f"Failed to delete directory {dir_path}: {e}")
        except Exception as e:
            raise FileSystemError(f"Unexpected error deleting directory {dir_path}: {e}")
    
    def list_subdirectories(self, path: Path) -> List[str]:
        """
        List all subdirectories in given path.
        
        Args:
            path: Path to scan for subdirectories
            
        Returns:
            List of subdirectory names
            
        Raises:
            FileSystemError: If directory listing fails
        """
        try:
            # Resolve path to prevent directory traversal
            resolved_path = path.resolve()
            
            # Ensure path is within base_path for security
            if not str(resolved_path).startswith(str(self.base_path)):
                raise FileSystemError(f"Path outside base directory: {resolved_path}")
            
            # Check if directory exists
            if not resolved_path.exists():
                return []  # No directory, no subdirectories
            
            if not resolved_path.is_dir():
                raise FileSystemError(f"Path is not a directory: {path}")
            
            # List subdirectories
            subdirs = []
            for item in resolved_path.iterdir():
                if item.is_dir():
                    subdirs.append(item.name)
            
            return sorted(subdirs)
            
        except FileSystemError:
            raise  # Re-raise our custom exceptions
        except OSError as e:
            raise FileSystemError(f"Failed to list subdirectories in {path}: {e}")
        except Exception as e:
            raise FileSystemError(f"Unexpected error listing subdirectories in {path}: {e}")
    
    def file_exists(self, file_path: Path) -> bool:
        """
        Check if file exists.
        
        Args:
            file_path: Path to check
            
        Returns:
            True if file exists, False otherwise
        """
        try:
            # Resolve path to prevent directory traversal
            resolved_path = file_path.resolve()
            
            # Ensure path is within base_path for security
            if not str(resolved_path).startswith(str(self.base_path)):
                return False  # Outside base path, consider as non-existent
            
            return resolved_path.exists() and resolved_path.is_file()
            
        except Exception:
            # Any error means file doesn't exist or isn't accessible
            return False
    
    def directory_exists(self, dir_path: Path) -> bool:
        """
        Check if directory exists.
        
        Args:
            dir_path: Path to check
            
        Returns:
            True if directory exists, False otherwise
        """
        try:
            # Resolve path to prevent directory traversal
            resolved_path = dir_path.resolve()
            
            # Ensure path is within base_path for security
            if not str(resolved_path).startswith(str(self.base_path)):
                return False  # Outside base path, consider as non-existent
            
            return resolved_path.exists() and resolved_path.is_dir()
            
        except Exception:
            # Any error means directory doesn't exist or isn't accessible
            return False
