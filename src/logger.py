"""日志系统模块

提供统一的日志配置和中文错误消息模板。
确保所有错误都被正确记录，并提供友好的中文错误消息。
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime


# 中文错误消息模板
ERROR_MESSAGES = {
    # 文件相关错误
    "file_not_found": "错误：找不到文件 '{path}'，请检查路径是否正确",
    "invalid_pdf": "错误：文件 '{path}' 不是有效的 PDF 文件",
    "permission_denied": "错误：没有权限读取文件 '{path}'",
    "file_locked": "错误：文件 '{path}' 被其他程序占用，无法访问",
    
    # 提取相关错误
    "extraction_failed": "错误：提取第 {page} 页时失败：{reason}",
    "encoding_error": "错误：文本编码转换失败，可能包含不支持的字符",
    "empty_pdf": "警告：PDF 文件为空，没有可提取的内容",
    "partial_extraction": "警告：部分页面提取失败，已提取 {success}/{total} 页",
    
    # 路径相关错误
    "invalid_path": "错误：路径 '{path}' 格式不正确",
    "path_too_long": "错误：路径 '{path}' 过长，超过系统限制",
    
    # 输出相关错误
    "save_failed": "错误：保存文件失败：{path}，原因：{reason}",
    "invalid_format": "错误：不支持的输出格式 '{format}'，支持的格式：text, json, markdown",
    
    # 配置相关错误
    "config_load_failed": "警告：加载配置文件失败：{path}，使用默认配置",
    "config_save_failed": "错误：保存配置文件失败：{path}，原因：{reason}",
    
    # 分析相关错误
    "analysis_failed": "警告：关键信息分析失败：{reason}，将返回部分结果",
    "keyword_extraction_failed": "警告：关键词提取失败，跳过此步骤",
    
    # 通用错误
    "unknown_error": "错误：发生未知错误：{error}",
    "operation_cancelled": "操作已取消",
}


# 日志格式模板
LOG_FORMATS = {
    "simple": "%(levelname)s: %(message)s",
    "detailed": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "debug": "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
}


class ChineseLogger:
    """中文日志记录器
    
    提供统一的日志配置和中文错误消息支持。
    """
    
    def __init__(
        self,
        name: str = "pdf_extractor",
        level: str = "WARNING",
        log_to_file: bool = False,
        log_file_path: Optional[str] = None,
        format_style: str = "simple"
    ):
        """初始化日志记录器
        
        参数:
            name: 日志记录器名称
            level: 日志级别（DEBUG, INFO, WARNING, ERROR, CRITICAL）
            log_to_file: 是否记录到文件
            log_file_path: 日志文件路径（如果 log_to_file 为 True）
            format_style: 日志格式样式（simple, detailed, debug）
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self._get_log_level(level))
        
        # 清除现有的处理器
        self.logger.handlers.clear()
        
        # 获取日志格式
        log_format = LOG_FORMATS.get(format_style, LOG_FORMATS["simple"])
        formatter = logging.Formatter(log_format)
        
        # 添加控制台处理器
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # 添加文件处理器（如果需要）
        if log_to_file:
            self._add_file_handler(log_file_path, formatter)
    
    def _get_log_level(self, level: str) -> int:
        """将字符串日志级别转换为 logging 常量
        
        参数:
            level: 日志级别字符串
            
        返回:
            logging 级别常量
        """
        level_map = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        return level_map.get(level.upper(), logging.WARNING)
    
    def _add_file_handler(self, log_file_path: Optional[str], formatter: logging.Formatter):
        """添加文件处理器
        
        参数:
            log_file_path: 日志文件路径
            formatter: 日志格式化器
        """
        if not log_file_path:
            # 使用默认路径
            log_dir = Path.home() / ".pdf_extractor" / "logs"
            log_dir.mkdir(parents=True, exist_ok=True)
            log_file_path = log_dir / f"pdf_extractor_{datetime.now().strftime('%Y%m%d')}.log"
        else:
            log_file_path = Path(log_file_path)
            log_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        except Exception as e:
            self.logger.warning(f"无法创建日志文件：{log_file_path}，错误：{str(e)}")
    
    def get_logger(self) -> logging.Logger:
        """获取日志记录器实例
        
        返回:
            logging.Logger 实例
        """
        return self.logger


def setup_logging(
    level: str = "WARNING",
    log_to_file: bool = False,
    log_file_path: Optional[str] = None,
    format_style: str = "simple"
) -> logging.Logger:
    """配置日志系统（便捷函数）
    
    参数:
        level: 日志级别（DEBUG, INFO, WARNING, ERROR, CRITICAL）
        log_to_file: 是否记录到文件
        log_file_path: 日志文件路径
        format_style: 日志格式样式（simple, detailed, debug）
        
    返回:
        配置好的日志记录器
    """
    chinese_logger = ChineseLogger(
        level=level,
        log_to_file=log_to_file,
        log_file_path=log_file_path,
        format_style=format_style
    )
    return chinese_logger.get_logger()


def get_error_message(error_type: str, **kwargs) -> str:
    """获取格式化的中文错误消息
    
    参数:
        error_type: 错误类型（ERROR_MESSAGES 中的键）
        **kwargs: 消息模板中的占位符参数
        
    返回:
        格式化的错误消息
    """
    template = ERROR_MESSAGES.get(error_type, ERROR_MESSAGES["unknown_error"])
    try:
        return template.format(**kwargs)
    except KeyError:
        # 如果参数不匹配，返回原始模板
        return template


def log_error(logger: logging.Logger, error_type: str, **kwargs):
    """记录错误日志（便捷函数）
    
    参数:
        logger: 日志记录器
        error_type: 错误类型
        **kwargs: 消息模板参数
    """
    message = get_error_message(error_type, **kwargs)
    logger.error(message)


def log_warning(logger: logging.Logger, error_type: str, **kwargs):
    """记录警告日志（便捷函数）
    
    参数:
        logger: 日志记录器
        error_type: 错误类型
        **kwargs: 消息模板参数
    """
    message = get_error_message(error_type, **kwargs)
    logger.warning(message)


# 全局日志记录器实例
_global_logger: Optional[logging.Logger] = None


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """获取日志记录器实例（便捷函数）
    
    参数:
        name: 日志记录器名称（可选）
        
    返回:
        日志记录器实例
    """
    global _global_logger
    
    if _global_logger is None:
        _global_logger = setup_logging()
    
    if name:
        return logging.getLogger(name)
    
    return _global_logger
