#!/usr/bin/env python3
"""
文件写入工具
为 data_insight_agent 提供安全的文件写入能力
"""

import os
import logging
import pathlib
import json
import tempfile
from datetime import datetime
from typing import Optional, Dict, Any


def write_file_content(file_path: str, content: str, backup: bool = True) -> str:
    """
    写入文件内容，支持自动备份
    
    Args:
        file_path (str): 文件路径，相对于项目根目录
        content (str): 要写入的内容
        backup (bool): 是否在写入前创建备份
        
    Returns:
        str: 操作结果信息
        
    Example:
        result = write_file_content("prompt_store/keyword_agent/system_message.md", new_content)
    """
    try:
        # 确保路径是相对于项目根目录的
        if not os.path.isabs(file_path):
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            full_path = os.path.join(project_root, file_path)
        else:
            full_path = file_path
            
        # 创建目录（如果不存在）
        directory = os.path.dirname(full_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            
        # 创建备份（如果文件存在且需要备份）
        backup_path = None
        if backup and os.path.exists(full_path):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{os.path.basename(full_path)}.backup_{timestamp}"
            backup_path = os.path.join(directory, backup_filename)
            
            # 复制原文件到备份
            with open(full_path, 'r', encoding='utf-8') as original:
                original_content = original.read()
            with open(backup_path, 'w', encoding='utf-8') as backup_file:
                backup_file.write(original_content)
                
        # 写入新内容
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        result = f"成功写入文件: {file_path}"
        if backup_path:
            result += f"\n备份文件: {os.path.basename(backup_path)}"
            
        return result
        
    except PermissionError:
        return f"错误: 没有权限写入文件 - {file_path}"
    except Exception as e:
        return f"错误: 写入文件时发生异常 - {file_path}: {str(e)}"


def append_to_file(file_path: str, content: str, separator: str = "\n") -> str:
    """
    追加内容到文件末尾
    
    Args:
        file_path (str): 文件路径
        content (str): 要追加的内容
        separator (str): 分隔符
        
    Returns:
        str: 操作结果信息
    """
    try:
        # 确保路径是相对于项目根目录的
        if not os.path.isabs(file_path):
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            full_path = os.path.join(project_root, file_path)
        else:
            full_path = file_path
            
        # 创建目录（如果不存在）
        directory = os.path.dirname(full_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            
        # 追加内容
        with open(full_path, 'a', encoding='utf-8') as f:
            if os.path.getsize(full_path) > 0:  # 文件不为空时添加分隔符
                f.write(separator)
            f.write(content)
            
        return f"成功追加内容到文件: {file_path}"
        
    except Exception as e:
        return f"错误: 追加文件时发生异常 - {file_path}: {str(e)}"




def backup_file(file_path: str, backup_dir: str = "backups") -> str:
    """
    创建文件备份
    
    Args:
        file_path (str): 要备份的文件路径
        backup_dir (str): 备份目录
        
    Returns:
        str: 备份结果信息
    """
    try:
        # 确保路径是相对于项目根目录的
        if not os.path.isabs(file_path):
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            full_path = os.path.join(project_root, file_path)
        else:
            full_path = file_path
            
        if not os.path.exists(full_path):
            return f"错误: 文件不存在 - {file_path}"
            
        # 创建备份目录
        if not os.path.isabs(backup_dir):
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            full_backup_dir = os.path.join(project_root, backup_dir)
        else:
            full_backup_dir = backup_dir
            
        os.makedirs(full_backup_dir, exist_ok=True)
        
        # 生成备份文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.basename(file_path)
        backup_filename = f"{filename}.backup_{timestamp}"
        backup_path = os.path.join(full_backup_dir, backup_filename)
        
        # 复制文件
        with open(full_path, 'r', encoding='utf-8') as original:
            content = original.read()
        with open(backup_path, 'w', encoding='utf-8') as backup_file:
            backup_file.write(content)
            
        return f"备份成功: {os.path.join(backup_dir, backup_filename)}"
        
    except Exception as e:
        return f"错误: 备份文件时发生异常 - {file_path}: {str(e)}"


# 配置日志，便于追踪LLM的调用行为
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def _atomic_write_to_file(path: pathlib.Path, final_content: str) -> bool:
    """[内部辅助函数] 使用原子操作安全地将内容写入文件。"""
    temp_path = None
    try:
        fd, temp_path_str = tempfile.mkstemp(suffix=".tmp", dir=path.parent, text=True)
        temp_path = pathlib.Path(temp_path_str)
        with os.fdopen(fd, 'w', encoding='utf-8') as temp_file:
            temp_file.write(final_content)
        os.replace(temp_path, path)
        temp_path = None
        return True
    except Exception as e:
        logging.error(f"原子写入文件 '{path}' 时失败: {e}")
        return False
    finally:
        if temp_path and temp_path.exists():
            temp_path.unlink()

def edit_file(
    file_path: str, 
    action: str,
    start_line: int,
    end_line: int = -1,
    new_code: str = ""
) -> str:
    """
    对文件执行指定的块级操作：替换、插入或删除。

    这是一个统一的文件编辑工具。通过 'action' 参数来决定具体行为。

    - **替换 (REPLACE)**: 删除 `start_line` 到 `end_line` 的内容，并用 `new_code` 替换。
      - `action="REPLACE"`, `start_line` 和 `end_line` 必须提供。
      - 示例: edit_file('a.txt', "REPLACE", 5, 10, "new content")

    - **插入 (INSERT)**: 在 `start_line` 处插入 `new_code`，原有内容下移。`end_line` 参数被忽略。
      - `action="INSERT"`, `start_line` 必须提供。
      - 示例: edit_file('a.txt', "INSERT", 5, new_code="new content")
      
    - **删除 (DELETE)**: 删除 `start_line` 到 `end_line` 的内容。`new_code` 参数被忽略。
      - `action="DELETE"`, `start_line` 和 `end_line` 必须提供。
      - 示例: edit_file('a.txt', "DELETE", 5, 10)

    Args:
        file_path (str): 要修改的文件的完整路径。
        action (str): 要执行的操作。必须是 "REPLACE", "INSERT", 或 "DELETE" 之一。
        start_line (int): 操作的起始行号（从1开始）。对于插入，这是新代码的插入位置。
        end_line (int, optional): 操作的结束行号（从1开始，包含此行）。对于插入操作，此参数被忽略。默认为-1。
        new_code (str, optional): 用于替换或插入的新代码。对于删除操作，此参数被忽略。默认为空字符串。

    Returns:
        str: 如果操作成功，返回 "操作成功完成。"；如果失败，则返回描述错误的字符串。
    """
    action = action.upper()
    valid_actions = ["REPLACE", "INSERT", "DELETE"]
    if action not in valid_actions:
        return f"错误：无效的操作 '{action}'。有效操作为: {', '.join(valid_actions)}。"

    path = pathlib.Path(file_path)
    if not path.is_file():
        return f"错误：文件未找到: {file_path}"

    lines = path.read_text('utf-8').splitlines()
    num_lines = len(lines)
    
    new_full_lines = []

    try:
        if action == "REPLACE":
            if not (1 <= start_line <= end_line <= num_lines):
                return f"错误 [REPLACE]：无效的行范围 {start_line}-{end_line}。文件总行数为 {num_lines}。"
            start_idx = start_line - 1
            lines_before = lines[:start_idx]
            lines_after = lines[end_line:]
            new_code_lines = new_code.splitlines()
            new_full_lines = lines_before + new_code_lines + lines_after
            log_msg = f"替换文件 '{path}' 的第 {start_line}-{end_line} 行。"

        elif action == "INSERT":
            if not (1 <= start_line <= num_lines + 1):
                return f"错误 [INSERT]：无效的插入行号 {start_line}。文件总行数为 {num_lines}。"
            insert_idx = start_line - 1
            lines_before = lines[:insert_idx]
            lines_after = lines[insert_idx:]
            new_code_lines = new_code.splitlines()
            new_full_lines = lines_before + new_code_lines + lines_after
            log_msg = f"在文件 '{path}' 的第 {start_line} 行插入新内容。"

        elif action == "DELETE":
            if not (1 <= start_line <= end_line <= num_lines):
                return f"错误 [DELETE]：无效的行范围 {start_line}-{end_line}。文件总行数为 {num_lines}。"
            start_idx = start_line - 1
            lines_before = lines[:start_idx]
            lines_after = lines[end_line:]
            new_full_lines = lines_before + lines_after
            log_msg = f"删除文件 '{path}' 的第 {start_line}-{end_line} 行。"
        
        final_content = "\n".join(new_full_lines)
        if _atomic_write_to_file(path, final_content):
            logging.info(f"成功: {log_msg}")
            return "操作成功完成。"
        else:
            return f"错误：写入文件 '{path}' 时发生未知错误。"
            
    except Exception as e:
        return f"处理文件时发生意外错误: {e}"

