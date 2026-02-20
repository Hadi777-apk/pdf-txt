"""CLI 集成测试 - 测试配置和日志系统集成"""

import pytest
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch, MagicMock

from src.cli import create_parser, main


class TestCLIConfigIntegration:
    """测试 CLI 与配置系统的集成"""
    
    def test_cli_with_config_file(self):
        """测试使用配置文件的 CLI"""
        with TemporaryDirectory() as tmpdir:
            # 创建配置文件
            config_file = Path(tmpdir) / "config.json"
            config_data = {
                "extract_key_info": False,
                "max_keywords": 20,
                "log_level": "INFO"
            }
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f)
            
            # 解析命令行参数
            parser = create_parser()
            args = parser.parse_args([
                'test.pdf',
                '-c', str(config_file)
            ])
            
            assert args.config == str(config_file)
            assert args.input == 'test.pdf'
    
    def test_cli_config_argument(self):
        """测试 CLI 配置参数"""
        parser = create_parser()
        
        # 测试带配置文件参数
        args = parser.parse_args(['input.pdf', '-c', 'config.json'])
        assert args.config == 'config.json'
        
        # 测试不带配置文件参数
        args = parser.parse_args(['input.pdf'])
        assert args.config is None
    
    @patch('src.cli.PDFExtractionService')
    def test_main_with_config(self, mock_service):
        """测试 main 函数使用配置"""
        with TemporaryDirectory() as tmpdir:
            # 创建配置文件
            config_file = Path(tmpdir) / "config.json"
            config_data = {
                "extract_key_info": True,
                "log_level": "DEBUG"
            }
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f)
            
            # 创建测试 PDF 文件
            test_pdf = Path(tmpdir) / "test.pdf"
            test_pdf.write_bytes(b'%PDF-1.4\n')
            
            # Mock 服务
            mock_instance = MagicMock()
            mock_instance.extract.return_value = "提取的文本"
            mock_service.return_value = mock_instance
            
            # 运行 main 函数
            result = main([
                str(test_pdf),
                '-c', str(config_file),
                '-q'  # 静默模式避免输出
            ])
            
            # 验证服务被调用
            assert mock_service.called
            assert mock_instance.extract.called


class TestCLILoggingIntegration:
    """测试 CLI 与日志系统的集成"""
    
    def test_verbose_flag(self):
        """测试详细模式标志"""
        parser = create_parser()
        args = parser.parse_args(['input.pdf', '-v'])
        
        assert args.verbose is True
        assert args.quiet is False
    
    def test_quiet_flag(self):
        """测试静默模式标志"""
        parser = create_parser()
        args = parser.parse_args(['input.pdf', '-q'])
        
        assert args.quiet is True
        assert args.verbose is False
    
    def test_default_logging(self):
        """测试默认日志设置"""
        parser = create_parser()
        args = parser.parse_args(['input.pdf'])
        
        assert args.verbose is False
        assert args.quiet is False


class TestCLIErrorHandling:
    """测试 CLI 错误处理"""
    
    @patch('src.cli.PDFExtractionService')
    def test_extraction_error_handling(self, mock_service):
        """测试提取错误处理"""
        from src.exceptions import FileNotFoundError as PDFFileNotFoundError
        
        # Mock 服务抛出错误
        mock_instance = MagicMock()
        mock_instance.extract.side_effect = PDFFileNotFoundError('test.pdf')
        mock_service.return_value = mock_instance
        
        # 运行 main 函数
        result = main(['nonexistent.pdf', '-q'])
        
        # 应该返回错误代码
        assert result == 1
    
    @patch('src.cli.PDFExtractionService')
    def test_keyboard_interrupt_handling(self, mock_service):
        """测试键盘中断处理"""
        # Mock 服务抛出 KeyboardInterrupt
        mock_instance = MagicMock()
        mock_instance.extract.side_effect = KeyboardInterrupt()
        mock_service.return_value = mock_instance
        
        # 运行 main 函数
        result = main(['test.pdf', '-q'])
        
        # 应该返回错误代码
        assert result == 1
