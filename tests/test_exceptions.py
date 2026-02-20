"""测试自定义异常类"""

import pytest
from src.exceptions import (
    PDFExtractionError,
    FileNotFoundError,
    InvalidPDFError,
    PermissionError,
    ExtractionError,
    PageExtractionError,
    EncodingError,
    PathError
)


class TestExceptions:
    """测试异常类"""
    
    def test_file_not_found_error(self):
        """测试文件不存在异常"""
        error = FileNotFoundError("test.pdf")
        
        assert error.path == "test.pdf"
        assert "找不到文件" in str(error)
        assert "test.pdf" in str(error)
        assert isinstance(error, PDFExtractionError)
    
    def test_invalid_pdf_error(self):
        """测试无效 PDF 异常"""
        error = InvalidPDFError("test.txt")
        
        assert error.path == "test.txt"
        assert "不是有效的 PDF 文件" in str(error)
        assert "test.txt" in str(error)
        assert isinstance(error, PDFExtractionError)
    
    def test_permission_error(self):
        """测试权限错误异常"""
        error = PermissionError("protected.pdf")
        
        assert error.path == "protected.pdf"
        assert "没有权限读取文件" in str(error)
        assert "protected.pdf" in str(error)
        assert isinstance(error, PDFExtractionError)
    
    def test_page_extraction_error(self):
        """测试页面提取错误异常"""
        error = PageExtractionError(5, "页面损坏")
        
        assert error.page == 5
        assert error.reason == "页面损坏"
        assert "第 5 页" in str(error)
        assert "页面损坏" in str(error)
        assert isinstance(error, ExtractionError)
        assert isinstance(error, PDFExtractionError)
    
    def test_encoding_error(self):
        """测试编码错误异常"""
        error = EncodingError()
        
        assert "编码转换失败" in str(error)
        assert isinstance(error, ExtractionError)
        assert isinstance(error, PDFExtractionError)
    
    def test_path_error(self):
        """测试路径错误异常"""
        error = PathError("invalid::path")
        
        assert error.path == "invalid::path"
        assert "路径" in str(error)
        assert "格式不正确" in str(error)
        assert isinstance(error, PDFExtractionError)
    
    def test_exception_hierarchy(self):
        """测试异常继承层次"""
        # 所有自定义异常都应该继承自 PDFExtractionError
        assert issubclass(FileNotFoundError, PDFExtractionError)
        assert issubclass(InvalidPDFError, PDFExtractionError)
        assert issubclass(PermissionError, PDFExtractionError)
        assert issubclass(ExtractionError, PDFExtractionError)
        assert issubclass(PageExtractionError, ExtractionError)
        assert issubclass(EncodingError, ExtractionError)
        assert issubclass(PathError, PDFExtractionError)
    
    def test_chinese_error_messages(self):
        """测试错误消息是否为中文"""
        errors = [
            FileNotFoundError("test.pdf"),
            InvalidPDFError("test.txt"),
            PermissionError("protected.pdf"),
            PageExtractionError(1, "测试原因"),
            EncodingError(),
            PathError("bad_path")
        ]
        
        for error in errors:
            # 检查错误消息包含中文字符
            error_msg = str(error)
            has_chinese = any('\u4e00' <= char <= '\u9fff' for char in error_msg)
            assert has_chinese, f"错误消息应该包含中文: {error_msg}"
