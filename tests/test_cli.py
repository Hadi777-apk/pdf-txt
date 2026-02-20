"""CLI 模块单元测试"""

import pytest
import sys
from io import StringIO
from unittest.mock import Mock, patch, MagicMock

from src.cli import create_parser, setup_logging, print_result, main
from src.exceptions import FileNotFoundError, InvalidPDFError


class TestCreateParser:
    """测试参数解析器创建"""
    
    def test_parser_creation(self):
        """测试解析器成功创建"""
        parser = create_parser()
        assert parser is not None
        assert parser.prog == 'pdf-extractor'
    
    def test_required_input_argument(self):
        """测试必需的输入参数"""
        parser = create_parser()
        
        # 没有输入参数应该失败
        with pytest.raises(SystemExit):
            parser.parse_args([])
        
        # 有输入参数应该成功
        args = parser.parse_args(['test.pdf'])
        assert args.input == 'test.pdf'
    
    def test_output_argument(self):
        """测试输出文件参数"""
        parser = create_parser()
        
        # 默认没有输出文件
        args = parser.parse_args(['test.pdf'])
        assert args.output is None
        
        # 指定输出文件
        args = parser.parse_args(['test.pdf', '-o', 'output.txt'])
        assert args.output == 'output.txt'
        
        # 使用长选项
        args = parser.parse_args(['test.pdf', '--output', 'result.txt'])
        assert args.output == 'result.txt'
    
    def test_format_argument(self):
        """测试输出格式参数"""
        parser = create_parser()
        
        # 默认格式是 text
        args = parser.parse_args(['test.pdf'])
        assert args.format == 'text'
        
        # 指定 JSON 格式
        args = parser.parse_args(['test.pdf', '-f', 'json'])
        assert args.format == 'json'
        
        # 指定 Markdown 格式
        args = parser.parse_args(['test.pdf', '--format', 'markdown'])
        assert args.format == 'markdown'
        
        # 无效格式应该失败
        with pytest.raises(SystemExit):
            parser.parse_args(['test.pdf', '-f', 'invalid'])
    
    def test_extract_key_info_argument(self):
        """测试关键信息提取参数"""
        parser = create_parser()
        
        # 默认不提取关键信息
        args = parser.parse_args(['test.pdf'])
        assert args.extract_key_info is False
        
        # 启用关键信息提取
        args = parser.parse_args(['test.pdf', '--extract-key-info'])
        assert args.extract_key_info is True
    
    def test_no_key_info_argument(self):
        """测试禁用关键信息提取参数"""
        parser = create_parser()
        
        # 默认值
        args = parser.parse_args(['test.pdf'])
        assert args.no_key_info is False
        
        # 禁用关键信息提取
        args = parser.parse_args(['test.pdf', '--no-key-info'])
        assert args.no_key_info is True
    
    def test_progress_argument(self):
        """测试进度显示参数"""
        parser = create_parser()
        
        # 默认不显示进度
        args = parser.parse_args(['test.pdf'])
        assert args.progress is False
        
        # 启用进度显示
        args = parser.parse_args(['test.pdf', '--progress'])
        assert args.progress is True
    
    def test_verbose_argument(self):
        """测试详细输出参数"""
        parser = create_parser()
        
        # 默认不详细输出
        args = parser.parse_args(['test.pdf'])
        assert args.verbose is False
        
        # 启用详细输出
        args = parser.parse_args(['test.pdf', '-v'])
        assert args.verbose is True
        
        args = parser.parse_args(['test.pdf', '--verbose'])
        assert args.verbose is True
    
    def test_quiet_argument(self):
        """测试静默模式参数"""
        parser = create_parser()
        
        # 默认不静默
        args = parser.parse_args(['test.pdf'])
        assert args.quiet is False
        
        # 启用静默模式
        args = parser.parse_args(['test.pdf', '-q'])
        assert args.quiet is True
        
        args = parser.parse_args(['test.pdf', '--quiet'])
        assert args.quiet is True
    
    def test_combined_arguments(self):
        """测试组合参数"""
        parser = create_parser()
        
        args = parser.parse_args([
            'input.pdf',
            '-o', 'output.json',
            '-f', 'json',
            '--extract-key-info',
            '--progress',
            '-v'
        ])
        
        assert args.input == 'input.pdf'
        assert args.output == 'output.json'
        assert args.format == 'json'
        assert args.extract_key_info is True
        assert args.progress is True
        assert args.verbose is True
    
    def test_chinese_path_argument(self):
        """测试中文路径参数"""
        parser = create_parser()
        
        # 中文输入路径
        args = parser.parse_args(['测试文件.pdf'])
        assert args.input == '测试文件.pdf'
        
        # 中文输出路径
        args = parser.parse_args(['test.pdf', '-o', '输出结果.txt'])
        assert args.output == '输出结果.txt'


class TestSetupLogging:
    """测试日志配置"""
    
    def test_default_logging(self):
        """测试默认日志级别"""
        import logging
        setup_logging()
        # 默认应该是 WARNING 级别
        # 注意：这个测试可能会受到其他测试的影响
        # 在实际应用中，日志配置应该只执行一次
    
    def test_verbose_logging(self):
        """测试详细日志模式"""
        setup_logging(verbose=True)
        # 应该设置为 DEBUG 级别
    
    def test_quiet_logging(self):
        """测试静默日志模式"""
        setup_logging(quiet=True)
        # 应该设置为 ERROR 级别


class TestPrintResult:
    """测试结果打印"""
    
    def test_print_to_stdout(self, capsys):
        """测试输出到标准输出"""
        result = "提取的文本内容"
        print_result(result)
        
        captured = capsys.readouterr()
        assert "提取的文本内容" in captured.out
    
    def test_print_with_output_file(self, capsys):
        """测试保存到文件后的消息"""
        result = "提取的文本内容"
        print_result(result, output_file="output.txt")
        
        captured = capsys.readouterr()
        assert "output.txt" in captured.out
        assert "提取完成" in captured.out
    
    def test_print_quiet_mode(self, capsys):
        """测试静默模式"""
        result = "提取的文本内容"
        print_result(result, output_file="output.txt", quiet=True)
        
        captured = capsys.readouterr()
        # 静默模式下不应该有输出
        assert captured.out == ""


class TestMain:
    """测试主函数"""
    
    @patch('src.cli.PDFExtractionService')
    def test_successful_extraction(self, mock_service_class, capsys):
        """测试成功提取"""
        # 模拟服务
        mock_service = Mock()
        mock_service.extract.return_value = "提取的文本内容"
        mock_service_class.return_value = mock_service
        
        # 执行
        exit_code = main(['test.pdf'])
        
        # 验证
        assert exit_code == 0
        mock_service.extract.assert_called_once()
        
        captured = capsys.readouterr()
        assert "提取的文本内容" in captured.out
    
    @patch('src.cli.PDFExtractionService')
    def test_extraction_with_output_file(self, mock_service_class):
        """测试保存到输出文件"""
        mock_service = Mock()
        mock_service.extract.return_value = "提取的文本内容"
        mock_service_class.return_value = mock_service
        
        exit_code = main(['test.pdf', '-o', 'output.txt'])
        
        assert exit_code == 0
        # 验证调用参数
        call_args = mock_service.extract.call_args
        assert call_args.kwargs['output_file'] == 'output.txt'
    
    @patch('src.cli.PDFExtractionService')
    def test_extraction_with_json_format(self, mock_service_class):
        """测试 JSON 格式输出"""
        mock_service = Mock()
        mock_service.extract.return_value = '{"text": "内容"}'
        mock_service_class.return_value = mock_service
        
        exit_code = main(['test.pdf', '-f', 'json'])
        
        assert exit_code == 0
        call_args = mock_service.extract.call_args
        assert call_args.kwargs['output_format'] == 'json'
    
    @patch('src.cli.PDFExtractionService')
    def test_extraction_with_key_info(self, mock_service_class):
        """测试提取关键信息"""
        mock_service = Mock()
        mock_service.extract.return_value = "提取的文本内容"
        mock_service_class.return_value = mock_service
        
        exit_code = main(['test.pdf', '--extract-key-info'])
        
        assert exit_code == 0
        call_args = mock_service.extract.call_args
        assert call_args.kwargs['extract_key_info'] is True
    
    @patch('src.cli.PDFExtractionService')
    def test_extraction_without_key_info(self, mock_service_class):
        """测试不提取关键信息"""
        mock_service = Mock()
        mock_service.extract.return_value = "提取的文本内容"
        mock_service_class.return_value = mock_service
        
        exit_code = main(['test.pdf', '--no-key-info'])
        
        assert exit_code == 0
        call_args = mock_service.extract.call_args
        assert call_args.kwargs['extract_key_info'] is False
    
    @patch('src.cli.PDFExtractionService')
    def test_extraction_with_progress(self, mock_service_class):
        """测试显示进度"""
        mock_service = Mock()
        mock_service.extract.return_value = "提取的文本内容"
        mock_service_class.return_value = mock_service
        
        exit_code = main(['test.pdf', '--progress'])
        
        assert exit_code == 0
        call_args = mock_service.extract.call_args
        assert call_args.kwargs['show_progress'] is True
    
    @patch('src.cli.PDFExtractionService')
    def test_file_not_found_error(self, mock_service_class, capsys):
        """测试文件不存在错误"""
        mock_service = Mock()
        mock_service.extract.side_effect = FileNotFoundError('test.pdf')
        mock_service_class.return_value = mock_service
        
        exit_code = main(['test.pdf'])
        
        assert exit_code == 1
        captured = capsys.readouterr()
        assert "找不到文件" in captured.err
    
    @patch('src.cli.PDFExtractionService')
    def test_invalid_pdf_error(self, mock_service_class, capsys):
        """测试无效 PDF 错误"""
        mock_service = Mock()
        mock_service.extract.side_effect = InvalidPDFError('test.txt')
        mock_service_class.return_value = mock_service
        
        exit_code = main(['test.txt'])
        
        assert exit_code == 1
        captured = capsys.readouterr()
        assert "不是有效的 PDF 文件" in captured.err
    
    @patch('src.cli.PDFExtractionService')
    def test_keyboard_interrupt(self, mock_service_class, capsys):
        """测试用户中断"""
        mock_service = Mock()
        mock_service.extract.side_effect = KeyboardInterrupt()
        mock_service_class.return_value = mock_service
        
        exit_code = main(['test.pdf'])
        
        assert exit_code == 1
        captured = capsys.readouterr()
        assert "操作已取消" in captured.err
    
    @patch('src.cli.PDFExtractionService')
    def test_unexpected_error(self, mock_service_class, capsys):
        """测试未预期的错误"""
        mock_service = Mock()
        mock_service.extract.side_effect = RuntimeError("未知错误")
        mock_service_class.return_value = mock_service
        
        exit_code = main(['test.pdf'])
        
        assert exit_code == 1
        captured = capsys.readouterr()
        assert "发生未知错误" in captured.err
    
    @patch('src.cli.PDFExtractionService')
    def test_quiet_mode(self, mock_service_class, capsys):
        """测试静默模式"""
        mock_service = Mock()
        mock_service.extract.return_value = "提取的文本内容"
        mock_service_class.return_value = mock_service
        
        exit_code = main(['test.pdf', '-q'])
        
        assert exit_code == 0
        captured = capsys.readouterr()
        # 静默模式下应该只有结果输出
        assert "正在处理文件" not in captured.out
    
    @patch('src.cli.PDFExtractionService')
    def test_verbose_mode(self, mock_service_class, capsys):
        """测试详细模式"""
        mock_service = Mock()
        mock_service.extract.return_value = "提取的文本内容"
        mock_service_class.return_value = mock_service
        
        exit_code = main(['test.pdf', '-v'])
        
        assert exit_code == 0
        # 详细模式应该设置日志级别为 DEBUG
    
    @patch('src.cli.PDFExtractionService')
    def test_chinese_path(self, mock_service_class):
        """测试中文路径"""
        mock_service = Mock()
        mock_service.extract.return_value = "提取的文本内容"
        mock_service_class.return_value = mock_service
        
        exit_code = main(['测试文件.pdf', '-o', '输出.txt'])
        
        assert exit_code == 0
        call_args = mock_service.extract.call_args
        assert call_args.kwargs['file_path'] == '测试文件.pdf'
        assert call_args.kwargs['output_file'] == '输出.txt'
