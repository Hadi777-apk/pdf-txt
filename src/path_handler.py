"""文件路径处理器"""

import os
from pathlib import Path
from typing import Union

from .exceptions import PathError


class PathHandler:
    """文件路径处理器
    
    处理和验证文件路径，支持：
    - Windows 路径格式
    - 相对路径和绝对路径
    - 包含中文字符的路径
    - 包含空格的路径
    """
    
    @staticmethod
    def normalize_path(path: str) -> str:
        """规范化路径
        
        处理：
        - 反斜杠和正斜杠统一
        - 展开相对路径为绝对路径
        - 处理中文字符和空格
        - 解析 ~ 为用户目录
        
        参数:
            path: 原始路径字符串
            
        返回:
            规范化后的绝对路径
            
        异常:
            PathError: 路径格式不正确
        """
        if not path or not isinstance(path, str):
            raise PathError(str(path))
        
        try:
            # 使用 pathlib 处理跨平台路径
            # expanduser() 处理 ~ 符号
            # resolve() 将相对路径转换为绝对路径，并规范化路径
            normalized = Path(path).expanduser().resolve()
            return str(normalized)
        except (ValueError, OSError) as e:
            raise PathError(path) from e
    
    @staticmethod
    def validate_path(path: str) -> bool:
        """验证路径是否有效
        
        检查：
        - 路径格式是否正确
        - 路径是否存在
        - 是否为文件（而非目录）
        
        参数:
            path: 要验证的路径
            
        返回:
            True 如果路径有效，False 否则
        """
        if not path or not isinstance(path, str):
            return False
        
        try:
            # 先规范化路径
            normalized = PathHandler.normalize_path(path)
            path_obj = Path(normalized)
            
            # 检查路径是否存在且是文件
            return path_obj.exists() and path_obj.is_file()
        except (PathError, ValueError, OSError):
            return False
    
    @staticmethod
    def is_pdf_file(path: str) -> bool:
        """检查文件是否为 PDF
        
        通过文件扩展名判断（不区分大小写）
        
        参数:
            path: 文件路径
            
        返回:
            True 如果是 PDF 文件，False 否则
        """
        if not path or not isinstance(path, str):
            return False
        
        try:
            path_obj = Path(path)
            # 获取扩展名并转换为小写进行比较
            return path_obj.suffix.lower() == '.pdf'
        except (ValueError, OSError):
            return False
