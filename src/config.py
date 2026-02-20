"""配置管理模块

提供应用程序配置管理功能，支持从配置文件和环境变量读取配置。
"""

import os
import json
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class ExtractionConfig:
    """提取配置"""
    
    # 关键信息提取配置
    extract_key_info: bool = True
    max_keywords: int = 10
    summary_max_length: int = 200
    
    # 输出配置
    default_output_format: str = "text"
    output_encoding: str = "utf-8"
    
    # 性能配置
    show_progress_threshold: int = 5  # 页数超过此值时显示进度
    
    # 日志配置
    log_level: str = "WARNING"
    log_to_file: bool = False
    log_file_path: str = "pdf_extractor.log"


class ConfigManager:
    """配置管理器
    
    负责加载、保存和管理应用程序配置。
    支持从配置文件、环境变量和默认值读取配置。
    
    配置优先级（从高到低）：
    1. 环境变量
    2. 配置文件
    3. 默认值
    """
    
    DEFAULT_CONFIG_PATHS = [
        Path.home() / ".pdf_extractor" / "config.json",  # 用户配置
        Path.cwd() / "pdf_extractor_config.json",  # 当前目录配置
    ]
    
    def __init__(self, config_path: Optional[str] = None):
        """初始化配置管理器
        
        参数:
            config_path: 配置文件路径（可选）。如果不提供，将按默认顺序查找配置文件
        """
        self.config = ExtractionConfig()
        self.config_path = Path(config_path) if config_path else None
        
        # 加载配置
        self._load_config()
    
    def _load_config(self):
        """加载配置
        
        按优先级顺序加载配置：
        1. 从配置文件加载
        2. 从环境变量覆盖
        """
        # 1. 从配置文件加载
        config_file = self._find_config_file()
        if config_file:
            self._load_from_file(config_file)
        
        # 2. 从环境变量覆盖
        self._load_from_env()
    
    def _find_config_file(self) -> Optional[Path]:
        """查找配置文件
        
        返回:
            配置文件路径，如果未找到则返回 None
        """
        # 如果指定了配置文件路径，直接使用
        if self.config_path and self.config_path.exists():
            return self.config_path
        
        # 否则按默认顺序查找
        for path in self.DEFAULT_CONFIG_PATHS:
            if path.exists():
                return path
        
        return None
    
    def _load_from_file(self, config_file: Path):
        """从配置文件加载配置
        
        参数:
            config_file: 配置文件路径
        """
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # 更新配置对象
            for key, value in config_data.items():
                if hasattr(self.config, key):
                    setattr(self.config, key, value)
        
        except Exception as e:
            # 配置文件加载失败时使用默认配置
            import logging
            logging.warning(f"加载配置文件失败: {config_file}, 使用默认配置。错误: {str(e)}")
    
    def _load_from_env(self):
        """从环境变量加载配置
        
        环境变量格式: PDF_EXTRACTOR_<配置项名称大写>
        例如: PDF_EXTRACTOR_EXTRACT_KEY_INFO=true
        """
        prefix = "PDF_EXTRACTOR_"
        
        # 布尔类型配置
        bool_configs = {
            'extract_key_info': 'EXTRACT_KEY_INFO',
            'show_progress': 'SHOW_PROGRESS',
            'log_to_file': 'LOG_TO_FILE',
        }
        
        for attr, env_name in bool_configs.items():
            env_value = os.environ.get(prefix + env_name)
            if env_value is not None:
                setattr(self.config, attr, env_value.lower() in ('true', '1', 'yes'))
        
        # 整数类型配置
        int_configs = {
            'max_keywords': 'MAX_KEYWORDS',
            'summary_max_length': 'SUMMARY_MAX_LENGTH',
            'show_progress_threshold': 'SHOW_PROGRESS_THRESHOLD',
        }
        
        for attr, env_name in int_configs.items():
            env_value = os.environ.get(prefix + env_name)
            if env_value is not None:
                try:
                    setattr(self.config, attr, int(env_value))
                except ValueError:
                    pass
        
        # 字符串类型配置
        str_configs = {
            'default_output_format': 'DEFAULT_OUTPUT_FORMAT',
            'output_encoding': 'OUTPUT_ENCODING',
            'log_level': 'LOG_LEVEL',
            'log_file_path': 'LOG_FILE_PATH',
        }
        
        for attr, env_name in str_configs.items():
            env_value = os.environ.get(prefix + env_name)
            if env_value is not None:
                setattr(self.config, attr, env_value)
    
    def save_config(self, config_path: Optional[str] = None):
        """保存配置到文件
        
        参数:
            config_path: 配置文件路径（可选）。如果不提供，使用默认路径
        """
        if config_path:
            save_path = Path(config_path)
        elif self.config_path:
            save_path = self.config_path
        else:
            # 使用默认的用户配置路径
            save_path = self.DEFAULT_CONFIG_PATHS[0]
        
        # 确保目录存在
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 保存配置
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(asdict(self.config), f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise IOError(f"保存配置文件失败: {save_path}。错误: {str(e)}")
    
    def get_config(self) -> ExtractionConfig:
        """获取当前配置
        
        返回:
            配置对象
        """
        return self.config
    
    def update_config(self, **kwargs):
        """更新配置
        
        参数:
            **kwargs: 要更新的配置项
        """
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
    
    def reset_to_defaults(self):
        """重置为默认配置"""
        self.config = ExtractionConfig()


# 全局配置管理器实例
_config_manager: Optional[ConfigManager] = None


def get_config_manager(config_path: Optional[str] = None) -> ConfigManager:
    """获取配置管理器实例（单例模式）
    
    参数:
        config_path: 配置文件路径（可选）
        
    返回:
        配置管理器实例
    """
    global _config_manager
    
    if _config_manager is None:
        _config_manager = ConfigManager(config_path)
    
    return _config_manager


def get_config(config_path: Optional[str] = None) -> ExtractionConfig:
    """获取配置对象（便捷函数）
    
    参数:
        config_path: 配置文件路径（可选）
        
    返回:
        配置对象
    """
    return get_config_manager(config_path).get_config()
