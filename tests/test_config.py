"""配置管理模块的单元测试"""

import os
import json
import pytest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.config import (
    ExtractionConfig,
    ConfigManager,
    get_config_manager,
    get_config
)


class TestExtractionConfig:
    """测试 ExtractionConfig 数据类"""
    
    def test_default_values(self):
        """测试默认配置值"""
        config = ExtractionConfig()
        
        assert config.extract_key_info is True
        assert config.max_keywords == 10
        assert config.summary_max_length == 200
        assert config.default_output_format == "text"
        assert config.output_encoding == "utf-8"
        assert config.show_progress_threshold == 5
        assert config.log_level == "WARNING"
        assert config.log_to_file is False
        assert config.log_file_path == "pdf_extractor.log"
    
    def test_custom_values(self):
        """测试自定义配置值"""
        config = ExtractionConfig(
            extract_key_info=False,
            max_keywords=20,
            summary_max_length=500,
            default_output_format="json",
            log_level="DEBUG"
        )
        
        assert config.extract_key_info is False
        assert config.max_keywords == 20
        assert config.summary_max_length == 500
        assert config.default_output_format == "json"
        assert config.log_level == "DEBUG"


class TestConfigManager:
    """测试 ConfigManager 类"""
    
    def test_init_with_defaults(self):
        """测试使用默认配置初始化"""
        manager = ConfigManager()
        config = manager.get_config()
        
        assert isinstance(config, ExtractionConfig)
        assert config.extract_key_info is True
    
    def test_load_from_file(self):
        """测试从配置文件加载"""
        with TemporaryDirectory() as tmpdir:
            # 创建配置文件
            config_file = Path(tmpdir) / "config.json"
            config_data = {
                "extract_key_info": False,
                "max_keywords": 15,
                "summary_max_length": 300,
                "default_output_format": "json",
                "log_level": "DEBUG"
            }
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f)
            
            # 加载配置
            manager = ConfigManager(str(config_file))
            config = manager.get_config()
            
            assert config.extract_key_info is False
            assert config.max_keywords == 15
            assert config.summary_max_length == 300
            assert config.default_output_format == "json"
            assert config.log_level == "DEBUG"
    
    def test_load_from_env(self):
        """测试从环境变量加载"""
        # 设置环境变量
        os.environ["PDF_EXTRACTOR_EXTRACT_KEY_INFO"] = "false"
        os.environ["PDF_EXTRACTOR_MAX_KEYWORDS"] = "25"
        os.environ["PDF_EXTRACTOR_LOG_LEVEL"] = "INFO"
        
        try:
            manager = ConfigManager()
            config = manager.get_config()
            
            assert config.extract_key_info is False
            assert config.max_keywords == 25
            assert config.log_level == "INFO"
        finally:
            # 清理环境变量
            del os.environ["PDF_EXTRACTOR_EXTRACT_KEY_INFO"]
            del os.environ["PDF_EXTRACTOR_MAX_KEYWORDS"]
            del os.environ["PDF_EXTRACTOR_LOG_LEVEL"]
    
    def test_save_config(self):
        """测试保存配置到文件"""
        with TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "config.json"
            
            # 创建配置管理器并修改配置
            manager = ConfigManager()
            manager.update_config(
                extract_key_info=False,
                max_keywords=30,
                log_level="ERROR"
            )
            
            # 保存配置
            manager.save_config(str(config_file))
            
            # 验证文件存在
            assert config_file.exists()
            
            # 读取并验证内容
            with open(config_file, 'r', encoding='utf-8') as f:
                saved_data = json.load(f)
            
            assert saved_data["extract_key_info"] is False
            assert saved_data["max_keywords"] == 30
            assert saved_data["log_level"] == "ERROR"
    
    def test_update_config(self):
        """测试更新配置"""
        manager = ConfigManager()
        
        # 更新配置
        manager.update_config(
            extract_key_info=False,
            max_keywords=50
        )
        
        config = manager.get_config()
        assert config.extract_key_info is False
        assert config.max_keywords == 50
        # 其他配置应保持默认值
        assert config.summary_max_length == 200
    
    def test_reset_to_defaults(self):
        """测试重置为默认配置"""
        manager = ConfigManager()
        
        # 修改配置
        manager.update_config(extract_key_info=False, max_keywords=100)
        assert manager.get_config().extract_key_info is False
        
        # 重置
        manager.reset_to_defaults()
        config = manager.get_config()
        
        assert config.extract_key_info is True
        assert config.max_keywords == 10
    
    def test_invalid_config_file(self):
        """测试加载无效的配置文件"""
        with TemporaryDirectory() as tmpdir:
            # 创建无效的配置文件
            config_file = Path(tmpdir) / "invalid.json"
            with open(config_file, 'w') as f:
                f.write("invalid json content")
            
            # 应该使用默认配置而不是崩溃
            manager = ConfigManager(str(config_file))
            config = manager.get_config()
            
            # 应该使用默认值
            assert config.extract_key_info is True


class TestConfigHelperFunctions:
    """测试配置辅助函数"""
    
    def test_get_config_manager(self):
        """测试获取配置管理器单例"""
        manager1 = get_config_manager()
        manager2 = get_config_manager()
        
        # 应该返回同一个实例
        assert manager1 is manager2
    
    def test_get_config(self):
        """测试获取配置对象"""
        config = get_config()
        
        assert isinstance(config, ExtractionConfig)
        assert config.extract_key_info is True
