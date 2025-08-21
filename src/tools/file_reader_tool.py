#!/usr/bin/env python3
"""
文件读取工具
为 data_insight_agent 提供读取文件内容的能力
"""

import os
from typing import Optional, List, Dict, Any


def read_file_content(file_path: str) -> str:
    """
    读取指定文件的内容
    
    Args:
        file_path (str): 文件路径，相对于项目根目录
        
    Returns:
        str: 文件内容，如果文件不存在或读取失败则返回错误信息
        
    Example:
        content = read_file_content("prompt_store/keyword_agent/system_message.md")
    """
    try:
        # 确保路径是相对于项目根目录的
        if not os.path.isabs(file_path):
            # 获取项目根目录（假设工具在 src/tools/ 下）
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            full_path = os.path.join(project_root, file_path)
        else:
            full_path = file_path
            
        # 检查文件是否存在
        if not os.path.exists(full_path):
            return f"错误: 文件不存在 - {file_path}"
            
        # 读取文件内容
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        return content
        
    except PermissionError:
        return f"错误: 没有权限读取文件 - {file_path}"
    except UnicodeDecodeError:
        return f"错误: 文件编码问题，无法读取 - {file_path}"
    except Exception as e:
        return f"错误: 读取文件时发生异常 - {file_path}: {str(e)}"


def read_directory_structure(directory_path: str, max_depth: int = 3) -> str:
    """
    读取目录结构
    
    Args:
        directory_path (str): 目录路径
        max_depth (int): 最大递归深度
        
    Returns:
        str: 目录结构的文本表示
    """
    try:
        # 获取项目根目录
        if not os.path.isabs(directory_path):
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            full_path = os.path.join(project_root, directory_path)
        else:
            full_path = directory_path
            
        if not os.path.exists(full_path):
            return f"错误: 目录不存在 - {directory_path}"
            
        if not os.path.isdir(full_path):
            return f"错误: 路径不是目录 - {directory_path}"
            
        def _build_tree(path: str, prefix: str = "", depth: int = 0) -> List[str]:
            if depth > max_depth:
                return []
                
            items = []
            try:
                entries = sorted(os.listdir(path))
                # 过滤掉隐藏文件和缓存目录
                entries = [e for e in entries if not e.startswith('.') and e != '__pycache__']
                
                for i, entry in enumerate(entries):
                    entry_path = os.path.join(path, entry)
                    is_last = i == len(entries) - 1
                    
                    if os.path.isdir(entry_path):
                        items.append(f"{prefix}{'└── ' if is_last else '├── '}{entry}/")
                        if depth < max_depth:
                            extension = "    " if is_last else "│   "
                            items.extend(_build_tree(entry_path, prefix + extension, depth + 1))
                    else:
                        items.append(f"{prefix}{'└── ' if is_last else '├── '}{entry}")
                        
            except PermissionError:
                items.append(f"{prefix}└── [权限不足]")
                
            return items
            
        tree_lines = [f"{directory_path}/"]
        tree_lines.extend(_build_tree(full_path))
        return "\n".join(tree_lines)
        
    except Exception as e:
        return f"错误: 读取目录结构时发生异常 - {directory_path}: {str(e)}"


def read_multiple_files(file_paths: List[str]) -> Dict[str, str]:
    """
    批量读取多个文件
    
    Args:
        file_paths (List[str]): 文件路径列表
        
    Returns:
        Dict[str, str]: 文件路径到内容的映射
    """
    results = {}
    for file_path in file_paths:
        results[file_path] = read_file_content(file_path)
    return results



