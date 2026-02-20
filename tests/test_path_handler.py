"""PathHandler 单元测试"""

import os
import tempfile
from pathlib import Path

import pytest

from src.path_handler import PathHandler
from src.exceptions import PathError


class TestPathHandler:
    """PathHandler 类的单元测试"""
    
    def test_normalize_path_absolute_windows_style(self):
        """测试 Windows 风格的绝对路径规范化"""
        # 注意：在非 Windows 系统上，这会被转换为当前系统的路径格式
        path = "c:\\Users\\Administrator\\Documents\\file.pdf"
        result = PathHandler.normalize_path(path)
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_normalize_path_relative(self):
        """测试相对路径规范化"""
        path = "./test.pdf"
        result = PathHandler.normalize_path(path)
        # 应该返回绝对路径
        assert os.path.isabs(result)
        assert result.endswith("test.pdf")
    
    def test_normalize_path_with_chinese(self):
        """测试包含中文字符的路径"""
        path = "./测试文件/文档.pdf"
        result = PathHandler.normalize_path(path)
        assert "测试文件" in result
        assert "文档.pdf" in result
        assert os.path.isabs(result)
    
    def test_normalize_path_with_spaces(self):
        """测试包含空格的路径"""
        path = "./my documents/test file.pdf"
        result = PathHandler.normalize_path(path)
        assert "my documents" in result
        assert "test file.pdf" in result
        assert os.path.isabs(result)
    
    def test_normalize_path_with_tilde(self):
        """测试包含 ~ 的路径（用户目录）"""
        path = "~/documents/test.pdf"
        result = PathHandler.normalize_path(path)
        # 应该展开为实际的用户目录
        assert "~" not in result
        assert os.path.isabs(result)
    
    def test_normalize_path_empty_string(self):
        """测试空字符串"""
        with pytest.raises(PathError):
            PathHandler.normalize_path("")
    
    def test_normalize_path_none(self):
        """测试 None 值"""
        with pytest.raises(PathError):
            PathHandler.normalize_path(None)
    
    def test_validate_path_existing_file(self):
        """测试验证存在的文件"""
        # 创建临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp_path = tmp.name
        
        try:
            assert PathHandler.validate_path(tmp_path) is True
        finally:
            os.unlink(tmp_path)
    
    def test_validate_path_nonexistent_file(self):
        """测试验证不存在的文件"""
        path = "/nonexistent/path/to/file.pdf"
        assert PathHandler.validate_path(path) is False
    
    def test_validate_path_directory(self):
        """测试验证目录（应该返回 False，因为不是文件）"""
        # 使用临时目录
        with tempfile.TemporaryDirectory() as tmp_dir:
            assert PathHandler.validate_path(tmp_dir) is False
    
    def test_validate_path_empty_string(self):
        """测试验证空字符串"""
        assert PathHandler.validate_path("") is False
    
    def test_validate_path_none(self):
        """测试验证 None 值"""
        assert PathHandler.validate_path(None) is False
    
    def test_validate_path_with_chinese(self):
        """测试验证包含中文的路径"""
        # 创建包含中文的临时文件
        with tempfile.NamedTemporaryFile(
            delete=False, 
            suffix="测试.pdf",
            dir=tempfile.gettempdir()
        ) as tmp:
            tmp_path = tmp.name
        
        try:
            assert PathHandler.validate_path(tmp_path) is True
        finally:
            os.unlink(tmp_path)
    
    def test_is_pdf_file_with_pdf_extension(self):
        """测试 PDF 扩展名识别"""
        assert PathHandler.is_pdf_file("test.pdf") is True
        assert PathHandler.is_pdf_file("test.PDF") is True
        assert PathHandler.is_pdf_file("test.Pdf") is True
    
    def test_is_pdf_file_with_non_pdf_extension(self):
        """测试非 PDF 扩展名"""
        assert PathHandler.is_pdf_file("test.txt") is False
        assert PathHandler.is_pdf_file("test.doc") is False
        assert PathHandler.is_pdf_file("test.docx") is False
    
    def test_is_pdf_file_no_extension(self):
        """测试没有扩展名的文件"""
        assert PathHandler.is_pdf_file("test") is False
    
    def test_is_pdf_file_with_chinese_filename(self):
        """测试中文文件名的 PDF"""
        assert PathHandler.is_pdf_file("测试文档.pdf") is True
        assert PathHandler.is_pdf_file("测试文档.txt") is False
    
    def test_is_pdf_file_with_spaces(self):
        """测试包含空格的文件名"""
        assert PathHandler.is_pdf_file("my document.pdf") is True
        assert PathHandler.is_pdf_file("my document.txt") is False
    
    def test_is_pdf_file_empty_string(self):
        """测试空字符串"""
        assert PathHandler.is_pdf_file("") is False
    
    def test_is_pdf_file_none(self):
        """测试 None 值"""
        assert PathHandler.is_pdf_file(None) is False
    
    def test_is_pdf_file_with_path(self):
        """测试完整路径的 PDF 文件"""
        assert PathHandler.is_pdf_file("/path/to/document.pdf") is True
        assert PathHandler.is_pdf_file("c:\\Users\\test\\document.pdf") is True
        assert PathHandler.is_pdf_file("./relative/path/document.pdf") is True
