"""测试核心数据模型"""

import pytest
from src.models import PDFDocument, PageText, KeyInformation, ExtractedContent


class TestPDFDocument:
    """测试 PDFDocument 类"""
    
    def test_create_pdf_document(self):
        """测试创建 PDF 文档对象"""
        doc = PDFDocument(
            file_path="test.pdf",
            page_count=10,
            metadata={"title": "测试文档", "author": "作者"}
        )
        
        assert doc.file_path == "test.pdf"
        assert doc.page_count == 10
        assert doc.metadata["title"] == "测试文档"
        assert doc.metadata["author"] == "作者"


class TestPageText:
    """测试 PageText 类"""
    
    def test_create_page_text(self):
        """测试创建页面文本对象"""
        page = PageText(page_number=0, text="这是测试文本")
        
        assert page.page_number == 0
        assert page.text == "这是测试文本"
        assert page.char_count == 6
        assert page.is_empty is False
    
    def test_empty_page_text(self):
        """测试空页面文本"""
        page = PageText(page_number=0, text="")
        
        assert page.is_empty is True
        assert page.char_count == 0
    
    def test_whitespace_only_page(self):
        """测试只包含空白的页面"""
        page = PageText(page_number=0, text="   \n\t  ")
        
        assert page.is_empty is True


class TestKeyInformation:
    """测试 KeyInformation 类"""
    
    def test_create_key_information(self):
        """测试创建关键信息对象"""
        key_info = KeyInformation(
            headings=["第一章", "第二章"],
            keywords=["关键词1", "关键词2"],
            summary="这是摘要",
            lists=["项目1", "项目2"]
        )
        
        assert len(key_info.headings) == 2
        assert len(key_info.keywords) == 2
        assert key_info.summary == "这是摘要"
        assert len(key_info.lists) == 2


class TestExtractedContent:
    """测试 ExtractedContent 类"""
    
    def test_create_extracted_content(self):
        """测试创建提取内容对象"""
        pages = [
            PageText(0, "第一页内容"),
            PageText(1, "第二页内容")
        ]
        
        content = ExtractedContent(
            file_path="test.pdf",
            page_count=2,
            pages=pages
        )
        
        assert content.file_path == "test.pdf"
        assert content.page_count == 2
        assert len(content.pages) == 2
        assert content.total_text == "第一页内容第二页内容"
    
    def test_extracted_content_with_errors(self):
        """测试包含错误的提取内容"""
        pages = [PageText(0, "成功提取的内容")]
        errors = ["第 2 页提取失败"]
        
        content = ExtractedContent(
            file_path="test.pdf",
            page_count=2,
            pages=pages,
            errors=errors
        )
        
        assert len(content.errors) == 1
        assert "第 2 页提取失败" in content.errors
    
    def test_extracted_content_with_key_info(self):
        """测试包含关键信息的提取内容"""
        pages = [PageText(0, "测试内容")]
        key_info = KeyInformation(
            headings=["标题"],
            keywords=["关键词"]
        )
        
        content = ExtractedContent(
            file_path="test.pdf",
            page_count=1,
            pages=pages,
            key_info=key_info
        )
        
        assert content.key_info is not None
        assert len(content.key_info.headings) == 1
        assert len(content.key_info.keywords) == 1
