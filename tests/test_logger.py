"""日志系统模块的单元测试"""

import logging
import pytest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.logger import (
    ChineseLogger,
    setup_logging,
    get_error_message,
    log_error,
    log_warning,
    get_logger,
    ERROR_MESSAGES
)


class TestErrorMessages:
    """测试错误消息模板"""
    
    def test_error_messages_exist(self):
        """测试错误消息模板存在"""
        assert "file_not_found" in ERROR_MESSAGES
        assert "invalid_pdf" in ERROR_MESSAGES
        assert "extraction_failed" in ERROR_MESSAGES
        assert "unknown_error" in ERROR_MESSAGES
    
    def test_error_messages_are_chinese(self):
        """测试错误消息是中文"""
        for key, message in ERROR_MESSAGES.items():
            # 检查消息包含中文字符
            assert any('\u4e00' <= char <= '\u9fff' for char in message), \
                f"错误消息 '{key}' 应该包含中文字符"
    
    def test_get_error_message_with_params(self):
        """测试获取带参数的错误消息"""
        message = get_error_message("file_not_found", path="/test/file.pdf")
        
        assert "找不到文件" in message
        assert "/test/file.pdf" in message
    
    def test_get_error_message_without_params(self):
        """测试获取不需要参数的错误消息"""
        message = get_error_message("encoding_error")
        
        assert "编码转换失败" in message
    
    def test_get_error_message_unknown_type(self):
        """测试获取未知类型的错误消息"""
        message = get_error_message("nonexistent_error", error="test")
        
        # 应该返回通用错误消息
        assert "未知错误" in message


class TestChineseLogger:
    """测试 ChineseLogger 类"""
    
    def test_init_with_defaults(self):
        """测试使用默认参数初始化"""
        logger = ChineseLogger()
        
        assert logger.logger is not None
        assert logger.logger.level == logging.WARNING
    
    def test_init_with_custom_level(self):
        """测试使用自定义日志级别"""
        logger = ChineseLogger(level="DEBUG")
        
        assert logger.logger.level == logging.DEBUG
    
    def test_init_with_invalid_level(self):
        """测试使用无效的日志级别"""
        logger = ChineseLogger(level="INVALID")
        
        # 应该使用默认的 WARNING 级别
        assert logger.logger.level == logging.WARNING
    
    def test_log_to_file(self):
        """测试记录日志到文件"""
        with TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "test.log"
            
            logger = ChineseLogger(
                level="INFO",
                log_to_file=True,
                log_file_path=str(log_file)
            )
            
            # 写入日志
            logger.get_logger().info("测试日志消息")
            
            # 关闭所有处理器以释放文件
            for handler in logger.get_logger().handlers[:]:
                handler.close()
                logger.get_logger().removeHandler(handler)
            
            # 验证文件存在
            assert log_file.exists()
            
            # 验证内容
            content = log_file.read_text(encoding='utf-8')
            assert "测试日志消息" in content
    
    def test_format_styles(self):
        """测试不同的日志格式样式"""
        # 简单格式
        logger_simple = ChineseLogger(format_style="simple")
        assert logger_simple.logger is not None
        
        # 详细格式
        logger_detailed = ChineseLogger(format_style="detailed")
        assert logger_detailed.logger is not None
        
        # 调试格式
        logger_debug = ChineseLogger(format_style="debug")
        assert logger_debug.logger is not None


class TestSetupLogging:
    """测试 setup_logging 函数"""
    
    def test_setup_with_defaults(self):
        """测试使用默认参数设置日志"""
        logger = setup_logging()
        
        assert logger is not None
        assert logger.level == logging.WARNING
    
    def test_setup_with_debug_level(self):
        """测试设置 DEBUG 级别"""
        logger = setup_logging(level="DEBUG")
        
        assert logger.level == logging.DEBUG
    
    def test_setup_with_file_logging(self):
        """测试启用文件日志"""
        with TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "app.log"
            
            logger = setup_logging(
                level="INFO",
                log_to_file=True,
                log_file_path=str(log_file)
            )
            
            # 写入日志
            logger.info("文件日志测试")
            
            # 关闭所有处理器以释放文件
            for handler in logger.handlers[:]:
                handler.close()
                logger.removeHandler(handler)
            
            # 验证文件存在
            assert log_file.exists()


class TestLogHelperFunctions:
    """测试日志辅助函数"""
    
    def test_log_error(self, caplog):
        """测试记录错误日志"""
        logger = logging.getLogger("test_logger")
        logger.setLevel(logging.ERROR)
        
        with caplog.at_level(logging.ERROR, logger="test_logger"):
            log_error(logger, "file_not_found", path="/test/file.pdf")
        
        assert "找不到文件" in caplog.text
        assert "/test/file.pdf" in caplog.text
    
    def test_log_warning(self, caplog):
        """测试记录警告日志"""
        logger = logging.getLogger("test_logger")
        logger.setLevel(logging.WARNING)
        
        with caplog.at_level(logging.WARNING, logger="test_logger"):
            log_warning(logger, "partial_extraction", success=5, total=10)
        
        assert "部分页面提取失败" in caplog.text
    
    def test_get_logger(self):
        """测试获取日志记录器"""
        logger = get_logger()
        
        assert logger is not None
        assert isinstance(logger, logging.Logger)
    
    def test_get_logger_with_name(self):
        """测试获取指定名称的日志记录器"""
        logger = get_logger("custom_logger")
        
        assert logger.name == "custom_logger"


class TestChineseErrorMessages:
    """测试中文错误消息的完整性"""
    
    def test_all_error_types_have_chinese(self):
        """测试所有错误类型都有中文消息"""
        error_types = [
            "file_not_found",
            "invalid_pdf",
            "permission_denied",
            "extraction_failed",
            "encoding_error",
            "invalid_path",
            "save_failed",
            "invalid_format",
            "config_load_failed",
            "analysis_failed",
            "unknown_error",
        ]
        
        for error_type in error_types:
            message = get_error_message(error_type)
            # 验证消息包含中文字符
            assert any('\u4e00' <= char <= '\u9fff' for char in message), \
                f"错误类型 '{error_type}' 的消息应该包含中文字符"
    
    def test_error_message_formatting(self):
        """测试错误消息格式化"""
        # 测试文件不存在错误
        msg = get_error_message("file_not_found", path="test.pdf")
        assert "test.pdf" in msg
        assert "找不到文件" in msg
        
        # 测试提取失败错误
        msg = get_error_message("extraction_failed", page=5, reason="损坏")
        assert "5" in msg
        assert "损坏" in msg
        
        # 测试部分提取失败
        msg = get_error_message("partial_extraction", success=8, total=10)
        assert "8" in msg
        assert "10" in msg
