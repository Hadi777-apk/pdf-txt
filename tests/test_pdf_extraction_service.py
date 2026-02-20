"""PDFExtractionService 单元测试"""

import pytest
import os
import tempfile
from unittest.mock import Mock, patch, MagicMock
from src.pdf_extraction_service import PDFExtractionService
from src.models import PDFDocument, PageText, ExtractedContent, KeyInformation
from src.exceptions import (
    FileNotFoundError as PDFFileNotFoundError,
    InvalidPDFError,
    PathError,
    PDFExtractionError
)


class TestPDFExtractionService:
    """测试 PDFExtractionService 类"""
    
    def test_initialization(self):
        """测试服务初始化"""
        service = PDFExtractionService()
        
        assert service.reader is not None
        assert service.extractor is not None
        assert service.analyzer is not None
        assert service.formatter is not None
        assert service.path_handler is not None
    
    @patch('src.pdf_extraction_service.PDFReader')
    @patch('src.pdf_extraction_service.TextExtractor')
    @patch('src.pdf_extraction_service.KeyInfoAnalyzer')
    @patch('src.pdf_extraction_service.OutputFormatter')
    @patch('src.pdf_extraction_service.PathHandler')
    def test_extract_basic_flow(self, mock_path_handler, mock_formatter, 
                                mock_analyzer, mock_extractor, mock_reader):
        """测试基本的提取流程"""
        # 设置 mock 对象
        service = PDFExtractionService()
        
        # Mock PathHandler
        service.path_handler.normalize_path.return_value = "/test/file.pdf"
        service.path_handler.validate_path.return_value = True
        service.path_handler.is_pdf_file.return_value = True
        
        # Mock PDFReader
        mock_document = PDFDocument(
            file_path="/test/file.pdf",
            page_count=2,
            metadata={},
            _internal_handle=Mock()
        )
        service.reader.open.return_value = mock_document
        
        # Mock TextExtractor
        mock_content = ExtractedContent(
            file_path="/test/file.pdf",
            page_count=2,
            pages=[
                PageText(0, "Page 1 text", 11, False),
                PageText(1, "Page 2 text", 11, False)
            ],
            total_text="Page 1 textPage 2 text",
            errors=[]
        )
        service.extractor.extract_all_text.return_value = mock_content
        
        # Mock KeyInfoAnalyzer
        service.analyzer.extract_headings.return_value = ["Heading 1"]
        service.analyzer.extract_keywords.return_value = ["keyword1", "keyword2"]
        service.analyzer.generate_summary.return_value = "Summary text"
        service.analyzer.extract_lists.return_value = ["List item 1"]
        
        # Mock OutputFormatter
        service.formatter.format_as_text.return_value = "Formatted text output"
        
        # 执行提取
        result = service.extract("/test/file.pdf", output_format="text", extract_key_info=True)
        
        # 验证结果
        assert result == "Formatted text output"
        
        # 验证调用
        service.path_handler.normalize_path.assert_called_once_with("/test/file.pdf")
        service.path_handler.validate_path.assert_called_once()
        service.path_handler.is_pdf_file.assert_called_once()
        service.reader.open.assert_called_once()
        service.extractor.extract_all_text.assert_called_once()
        service.analyzer.extract_headings.assert_called_once()
        service.formatter.format_as_text.assert_called_once()
        service.reader.close.assert_called_once()
    
    @patch('src.pdf_extraction_service.PathHandler')
    def test_extract_invalid_path(self, mock_path_handler):
        """测试无效路径处理"""
        service = PDFExtractionService()
        service.path_handler.normalize_path.side_effect = PathError("/invalid/path")
        
        with pytest.raises(PathError):
            service.extract("/invalid/path")
    
    @patch('src.pdf_extraction_service.PathHandler')
    def test_extract_file_not_found(self, mock_path_handler):
        """测试文件不存在的情况"""
        service = PDFExtractionService()
        service.path_handler.normalize_path.return_value = "/test/nonexistent.pdf"
        service.path_handler.validate_path.return_value = False
        
        with pytest.raises(PDFFileNotFoundError):
            service.extract("/test/nonexistent.pdf")
    
    @patch('src.pdf_extraction_service.PathHandler')
    def test_extract_not_pdf_file(self, mock_path_handler):
        """测试非 PDF 文件"""
        service = PDFExtractionService()
        service.path_handler.normalize_path.return_value = "/test/file.txt"
        service.path_handler.validate_path.return_value = True
        service.path_handler.is_pdf_file.return_value = False
        
        with pytest.raises(InvalidPDFError):
            service.extract("/test/file.txt")
    
    @patch('src.pdf_extraction_service.PDFReader')
    @patch('src.pdf_extraction_service.TextExtractor')
    @patch('src.pdf_extraction_service.KeyInfoAnalyzer')
    @patch('src.pdf_extraction_service.OutputFormatter')
    @patch('src.pdf_extraction_service.PathHandler')
    def test_extract_without_key_info(self, mock_path_handler, mock_formatter,
                                     mock_analyzer, mock_extractor, mock_reader):
        """测试不提取关键信息的情况"""
        service = PDFExtractionService()
        
        # Mock PathHandler
        service.path_handler.normalize_path.return_value = "/test/file.pdf"
        service.path_handler.validate_path.return_value = True
        service.path_handler.is_pdf_file.return_value = True
        
        # Mock PDFReader
        mock_document = PDFDocument(
            file_path="/test/file.pdf",
            page_count=1,
            metadata={},
            _internal_handle=Mock()
        )
        service.reader.open.return_value = mock_document
        
        # Mock TextExtractor
        mock_content = ExtractedContent(
            file_path="/test/file.pdf",
            page_count=1,
            pages=[PageText(0, "Test text", 9, False)],
            total_text="Test text",
            errors=[]
        )
        service.extractor.extract_all_text.return_value = mock_content
        
        # Mock OutputFormatter
        service.formatter.format_as_json.return_value = '{"test": "json"}'
        
        # 执行提取（不提取关键信息）
        result = service.extract("/test/file.pdf", output_format="json", extract_key_info=False)
        
        # 验证结果
        assert result == '{"test": "json"}'
        
        # 验证格式化器被正确调用
        service.formatter.format_as_json.assert_called_once()
    
    @patch('src.pdf_extraction_service.PDFReader')
    @patch('src.pdf_extraction_service.TextExtractor')
    @patch('src.pdf_extraction_service.OutputFormatter')
    @patch('src.pdf_extraction_service.PathHandler')
    def test_extract_with_output_file(self, mock_path_handler, mock_formatter,
                                      mock_extractor, mock_reader):
        """测试保存到输出文件"""
        service = PDFExtractionService()
        
        # Mock PathHandler
        service.path_handler.normalize_path.return_value = "/test/file.pdf"
        service.path_handler.validate_path.return_value = True
        service.path_handler.is_pdf_file.return_value = True
        
        # Mock PDFReader
        mock_document = PDFDocument(
            file_path="/test/file.pdf",
            page_count=1,
            metadata={},
            _internal_handle=Mock()
        )
        service.reader.open.return_value = mock_document
        
        # Mock TextExtractor
        mock_content = ExtractedContent(
            file_path="/test/file.pdf",
            page_count=1,
            pages=[PageText(0, "Test text", 9, False)],
            total_text="Test text",
            errors=[]
        )
        service.extractor.extract_all_text.return_value = mock_content
        
        # Mock OutputFormatter
        service.formatter.format_as_text.return_value = "Formatted output"
        service.formatter.save_to_file.return_value = "文件保存成功: /output/result.txt"
        
        # 执行提取并保存
        result = service.extract(
            "/test/file.pdf",
            output_format="text",
            extract_key_info=False,
            output_file="/output/result.txt"
        )
        
        # 验证结果
        assert result == "Formatted output"
        
        # 验证保存文件被调用
        service.formatter.save_to_file.assert_called_once_with(
            "Formatted output",
            "/output/result.txt"
        )
    
    @patch('src.pdf_extraction_service.PDFReader')
    @patch('src.pdf_extraction_service.TextExtractor')
    @patch('src.pdf_extraction_service.PathHandler')
    def test_extract_unsupported_format(self, mock_path_handler, mock_extractor, mock_reader):
        """测试不支持的输出格式"""
        service = PDFExtractionService()
        
        # Mock PathHandler
        service.path_handler.normalize_path.return_value = "/test/file.pdf"
        service.path_handler.validate_path.return_value = True
        service.path_handler.is_pdf_file.return_value = True
        
        # Mock PDFReader
        mock_document = PDFDocument(
            file_path="/test/file.pdf",
            page_count=1,
            metadata={},
            _internal_handle=Mock()
        )
        service.reader.open.return_value = mock_document
        
        # Mock TextExtractor
        mock_content = ExtractedContent(
            file_path="/test/file.pdf",
            page_count=1,
            pages=[PageText(0, "Test", 4, False)],
            total_text="Test",
            errors=[]
        )
        service.extractor.extract_all_text.return_value = mock_content
        
        # 测试不支持的格式
        with pytest.raises(PDFExtractionError) as exc_info:
            service.extract("/test/file.pdf", output_format="xml", extract_key_info=False)
        
        assert "不支持的输出格式" in str(exc_info.value)
    
    def test_format_output_text(self):
        """测试文本格式输出"""
        service = PDFExtractionService()
        
        content = ExtractedContent(
            file_path="/test/file.pdf",
            page_count=1,
            pages=[PageText(0, "Test content", 12, False)],
            total_text="Test content",
            errors=[]
        )
        
        result = service._format_output(content, "text")
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_format_output_json(self):
        """测试 JSON 格式输出"""
        service = PDFExtractionService()
        
        content = ExtractedContent(
            file_path="/test/file.pdf",
            page_count=1,
            pages=[PageText(0, "Test content", 12, False)],
            total_text="Test content",
            errors=[]
        )
        
        result = service._format_output(content, "json")
        assert isinstance(result, str)
        assert "{" in result  # JSON 格式
    
    def test_format_output_markdown(self):
        """测试 Markdown 格式输出"""
        service = PDFExtractionService()
        
        content = ExtractedContent(
            file_path="/test/file.pdf",
            page_count=1,
            pages=[PageText(0, "Test content", 12, False)],
            total_text="Test content",
            errors=[]
        )
        
        result = service._format_output(content, "markdown")
        assert isinstance(result, str)
        assert "#" in result  # Markdown 标题
    
    def test_analyze_key_information(self):
        """测试关键信息分析"""
        service = PDFExtractionService()
        
        text = """
        第一章 引言
        
        这是一个测试文档。包含一些关键词和重要信息。
        
        主要内容包括：
        - 第一点
        - 第二点
        - 第三点
        """
        
        key_info = service._analyze_key_information(text)
        
        assert isinstance(key_info, KeyInformation)
        assert isinstance(key_info.headings, list)
        assert isinstance(key_info.keywords, list)
        assert isinstance(key_info.summary, str)
        assert isinstance(key_info.lists, list)
