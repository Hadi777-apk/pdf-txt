"""PDFReader 类的单元测试"""

import os
import pytest
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from src.pdf_reader import PDFReader
from src.models import PDFDocument
from src.exceptions import (
    FileNotFoundError as PDFFileNotFoundError,
    InvalidPDFError,
    PermissionError as PDFPermissionError
)


@pytest.fixture
def pdf_reader():
    """创建 PDFReader 实例"""
    return PDFReader()


@pytest.fixture
def temp_pdf_file(tmp_path):
    """创建临时 PDF 文件"""
    pdf_path = tmp_path / "test.pdf"
    
    # 创建一个简单的 PDF 文件
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    c.drawString(100, 750, "Test PDF Content")
    c.showPage()
    c.save()
    
    return str(pdf_path)


@pytest.fixture
def temp_chinese_pdf_file(tmp_path):
    """创建包含中文内容的临时 PDF 文件"""
    pdf_path = tmp_path / "chinese_test.pdf"
    
    # 创建包含中文的 PDF
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    
    # 注册中文字体（使用系统字体）
    try:
        # 尝试使用常见的中文字体
        c.setFont("Helvetica", 12)
        c.drawString(100, 750, "Chinese Content: 中文内容测试")
    except:
        # 如果字体不可用，使用默认字体
        c.drawString(100, 750, "Chinese Content Test")
    
    c.showPage()
    c.save()
    
    return str(pdf_path)


@pytest.fixture
def temp_multipage_pdf_file(tmp_path):
    """创建多页 PDF 文件"""
    pdf_path = tmp_path / "multipage.pdf"
    
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    
    # 创建 3 页
    for i in range(3):
        c.drawString(100, 750, f"Page {i + 1}")
        c.showPage()
    
    c.save()
    
    return str(pdf_path)


@pytest.fixture
def temp_invalid_file(tmp_path):
    """创建非 PDF 文件"""
    file_path = tmp_path / "not_a_pdf.txt"
    with open(file_path, 'w') as f:
        f.write("This is not a PDF file")
    return str(file_path)


class TestPDFReaderOpen:
    """测试 open 方法"""
    
    def test_open_valid_pdf(self, pdf_reader, temp_pdf_file):
        """测试打开有效的 PDF 文件"""
        document = pdf_reader.open(temp_pdf_file)
        
        assert isinstance(document, PDFDocument)
        assert document.file_path == temp_pdf_file
        assert document.page_count > 0
        assert document._internal_handle is not None
        
        # 清理
        pdf_reader.close(document)
    
    def test_open_chinese_pdf(self, pdf_reader, temp_chinese_pdf_file):
        """测试打开包含中文的 PDF 文件"""
        document = pdf_reader.open(temp_chinese_pdf_file)
        
        assert isinstance(document, PDFDocument)
        assert document.page_count > 0
        
        # 清理
        pdf_reader.close(document)
    
    def test_open_multipage_pdf(self, pdf_reader, temp_multipage_pdf_file):
        """测试打开多页 PDF 文件"""
        document = pdf_reader.open(temp_multipage_pdf_file)
        
        assert document.page_count == 3
        
        # 清理
        pdf_reader.close(document)
    
    def test_open_nonexistent_file(self, pdf_reader):
        """测试打开不存在的文件"""
        with pytest.raises(PDFFileNotFoundError) as exc_info:
            pdf_reader.open("nonexistent_file.pdf")
        
        assert "找不到文件" in str(exc_info.value)
        assert "nonexistent_file.pdf" in str(exc_info.value)
    
    def test_open_invalid_pdf(self, pdf_reader, temp_invalid_file):
        """测试打开无效的 PDF 文件"""
        with pytest.raises(InvalidPDFError) as exc_info:
            pdf_reader.open(temp_invalid_file)
        
        assert "不是有效的 PDF 文件" in str(exc_info.value)
    
    def test_open_with_metadata(self, pdf_reader, tmp_path):
        """测试打开带元数据的 PDF 文件"""
        pdf_path = tmp_path / "metadata.pdf"
        
        # 创建带元数据的 PDF
        c = canvas.Canvas(str(pdf_path), pagesize=letter)
        c.setTitle("Test Title")
        c.setAuthor("Test Author")
        c.drawString(100, 750, "Content")
        c.showPage()
        c.save()
        
        document = pdf_reader.open(str(pdf_path))
        
        assert document.metadata is not None
        assert isinstance(document.metadata, dict)
        
        # 清理
        pdf_reader.close(document)


class TestPDFReaderGetPageCount:
    """测试 get_page_count 方法"""
    
    def test_get_page_count_single_page(self, pdf_reader, temp_pdf_file):
        """测试获取单页 PDF 的页数"""
        document = pdf_reader.open(temp_pdf_file)
        
        page_count = pdf_reader.get_page_count(document)
        assert page_count == 1
        
        # 清理
        pdf_reader.close(document)
    
    def test_get_page_count_multipage(self, pdf_reader, temp_multipage_pdf_file):
        """测试获取多页 PDF 的页数"""
        document = pdf_reader.open(temp_multipage_pdf_file)
        
        page_count = pdf_reader.get_page_count(document)
        assert page_count == 3
        
        # 清理
        pdf_reader.close(document)


class TestPDFReaderClose:
    """测试 close 方法"""
    
    def test_close_document(self, pdf_reader, temp_pdf_file):
        """测试关闭 PDF 文档"""
        document = pdf_reader.open(temp_pdf_file)
        
        assert document._internal_handle is not None
        
        pdf_reader.close(document)
        
        assert document._internal_handle is None
    
    def test_close_already_closed(self, pdf_reader, temp_pdf_file):
        """测试关闭已关闭的文档（不应抛出异常）"""
        document = pdf_reader.open(temp_pdf_file)
        
        pdf_reader.close(document)
        # 再次关闭不应抛出异常
        pdf_reader.close(document)
        
        assert document._internal_handle is None


class TestPDFReaderEdgeCases:
    """测试边缘情况"""
    
    def test_open_empty_pdf(self, pdf_reader, tmp_path):
        """测试打开空 PDF（无内容但有效）"""
        pdf_path = tmp_path / "empty.pdf"
        
        # 创建空 PDF（只有一个空页）
        c = canvas.Canvas(str(pdf_path), pagesize=letter)
        c.showPage()
        c.save()
        
        document = pdf_reader.open(str(pdf_path))
        
        assert document.page_count == 1
        
        # 清理
        pdf_reader.close(document)
    
    def test_open_path_with_spaces(self, pdf_reader, tmp_path):
        """测试打开路径包含空格的 PDF"""
        pdf_path = tmp_path / "file with spaces.pdf"
        
        c = canvas.Canvas(str(pdf_path), pagesize=letter)
        c.drawString(100, 750, "Content")
        c.showPage()
        c.save()
        
        document = pdf_reader.open(str(pdf_path))
        
        assert document.page_count == 1
        
        # 清理
        pdf_reader.close(document)
    
    def test_open_file_in_readonly_mode(self, pdf_reader, temp_pdf_file):
        """测试以只读模式打开文件（需求 1.5）
        
        pdfplumber 默认以只读模式打开文件，因此即使文件被其他程序占用，
        也应该能够成功打开。这个测试验证文件可以被多次打开。
        """
        # 第一次打开文件
        document1 = pdf_reader.open(temp_pdf_file)
        assert document1 is not None
        
        # 在不关闭第一个文档的情况下，再次打开同一文件
        # 这模拟了文件被其他程序占用的情况
        document2 = pdf_reader.open(temp_pdf_file)
        assert document2 is not None
        
        # 两个文档都应该有效
        assert document1.page_count == document2.page_count
        
        # 清理
        pdf_reader.close(document1)
        pdf_reader.close(document2)
