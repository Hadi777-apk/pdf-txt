"""TextExtractor 类的单元测试"""

import pytest
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from src.text_extractor import TextExtractor
from src.pdf_reader import PDFReader
from src.models import PageText, ExtractedContent
from src.exceptions import PageExtractionError


@pytest.fixture
def text_extractor():
    """创建 TextExtractor 实例"""
    return TextExtractor()


@pytest.fixture
def pdf_reader():
    """创建 PDFReader 实例"""
    return PDFReader()


@pytest.fixture
def temp_simple_pdf(tmp_path):
    """创建简单的单页 PDF"""
    pdf_path = tmp_path / "simple.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    c.drawString(100, 750, "Hello World")
    c.showPage()
    c.save()
    return str(pdf_path)


@pytest.fixture
def temp_multipage_pdf(tmp_path):
    """创建多页 PDF"""
    pdf_path = tmp_path / "multipage.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    
    for i in range(3):
        c.drawString(100, 750, f"Page {i + 1} content")
        c.showPage()
    
    c.save()
    return str(pdf_path)


@pytest.fixture
def temp_empty_page_pdf(tmp_path):
    """创建包含空页面的 PDF"""
    pdf_path = tmp_path / "empty_page.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    
    # 第一页有内容
    c.drawString(100, 750, "Page 1 content")
    c.showPage()
    
    # 第二页为空
    c.showPage()
    
    # 第三页有内容
    c.drawString(100, 750, "Page 3 content")
    c.showPage()
    
    c.save()
    return str(pdf_path)


@pytest.fixture
def temp_chinese_pdf(tmp_path):
    """创建包含中文的 PDF"""
    pdf_path = tmp_path / "chinese.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    c.drawString(100, 750, "Chinese: 你好世界")
    c.showPage()
    c.save()
    return str(pdf_path)


class TestExtractText:
    """测试 extract_text 方法"""
    
    def test_extract_text_from_valid_page(self, text_extractor, pdf_reader, temp_simple_pdf):
        """测试从有效页面提取文本"""
        document = pdf_reader.open(temp_simple_pdf)
        
        text = text_extractor.extract_text(document, 0)
        
        assert isinstance(text, str)
        assert "Hello World" in text
        
        pdf_reader.close(document)
    
    def test_extract_text_from_multipage(self, text_extractor, pdf_reader, temp_multipage_pdf):
        """测试从多页 PDF 的不同页面提取文本"""
        document = pdf_reader.open(temp_multipage_pdf)
        
        # 提取第一页
        text1 = text_extractor.extract_text(document, 0)
        assert "Page 1" in text1
        
        # 提取第二页
        text2 = text_extractor.extract_text(document, 1)
        assert "Page 2" in text2
        
        # 提取第三页
        text3 = text_extractor.extract_text(document, 2)
        assert "Page 3" in text3
        
        pdf_reader.close(document)
    
    def test_extract_text_from_empty_page(self, text_extractor, pdf_reader, temp_empty_page_pdf):
        """测试从空页面提取文本（需求 2.4）"""
        document = pdf_reader.open(temp_empty_page_pdf)
        
        # 第二页是空的
        text = text_extractor.extract_text(document, 1)
        
        # 空页面应该返回空字符串
        assert text == ""
        
        pdf_reader.close(document)
    
    def test_extract_text_invalid_page_number(self, text_extractor, pdf_reader, temp_simple_pdf):
        """测试提取无效页码"""
        document = pdf_reader.open(temp_simple_pdf)
        
        # 页码超出范围
        with pytest.raises(PageExtractionError) as exc_info:
            text_extractor.extract_text(document, 10)
        
        assert "页码超出范围" in str(exc_info.value)
        
        pdf_reader.close(document)
    
    def test_extract_text_negative_page_number(self, text_extractor, pdf_reader, temp_simple_pdf):
        """测试提取负数页码"""
        document = pdf_reader.open(temp_simple_pdf)
        
        with pytest.raises(PageExtractionError) as exc_info:
            text_extractor.extract_text(document, -1)
        
        assert "页码超出范围" in str(exc_info.value)
        
        pdf_reader.close(document)
    
    def test_extract_text_utf8_encoding(self, text_extractor, pdf_reader, temp_chinese_pdf):
        """测试 UTF-8 编码处理（需求 3.1, 3.3）"""
        document = pdf_reader.open(temp_chinese_pdf)
        
        text = text_extractor.extract_text(document, 0)
        
        # 验证可以正确编码为 UTF-8
        encoded = text.encode('utf-8')
        decoded = encoded.decode('utf-8')
        assert decoded == text
        
        # 验证包含中文内容
        assert "你好世界" in text or "Chinese" in text
        
        pdf_reader.close(document)


class TestExtractAllText:
    """测试 extract_all_text 方法"""
    
    def test_extract_all_text_single_page(self, text_extractor, pdf_reader, temp_simple_pdf):
        """测试提取单页 PDF 的所有文本"""
        document = pdf_reader.open(temp_simple_pdf)
        
        content = text_extractor.extract_all_text(document)
        
        assert isinstance(content, ExtractedContent)
        assert content.page_count == 1
        assert len(content.pages) == 1
        assert "Hello World" in content.total_text
        assert len(content.errors) == 0
        
        pdf_reader.close(document)
    
    def test_extract_all_text_multipage(self, text_extractor, pdf_reader, temp_multipage_pdf):
        """测试提取多页 PDF 的所有文本（需求 2.3）"""
        document = pdf_reader.open(temp_multipage_pdf)
        
        content = text_extractor.extract_all_text(document)
        
        # 验证提取的页面数量等于文档总页数（属性 3）
        assert content.page_count == 3
        assert len(content.pages) == 3
        
        # 验证每页都有内容
        assert "Page 1" in content.pages[0].text
        assert "Page 2" in content.pages[1].text
        assert "Page 3" in content.pages[2].text
        
        # 验证总文本包含所有页面内容
        assert "Page 1" in content.total_text
        assert "Page 2" in content.total_text
        assert "Page 3" in content.total_text
        
        pdf_reader.close(document)
    
    def test_extract_all_text_with_empty_pages(self, text_extractor, pdf_reader, temp_empty_page_pdf):
        """测试提取包含空页面的 PDF（需求 2.4）"""
        document = pdf_reader.open(temp_empty_page_pdf)
        
        content = text_extractor.extract_all_text(document)
        
        assert content.page_count == 3
        assert len(content.pages) == 3
        
        # 第一页有内容
        assert not content.pages[0].is_empty
        assert "Page 1" in content.pages[0].text
        
        # 第二页为空
        assert content.pages[1].is_empty
        assert content.pages[1].text == ""
        
        # 第三页有内容
        assert not content.pages[2].is_empty
        assert "Page 3" in content.pages[2].text
        
        # 空页面不应该导致错误
        assert len(content.errors) == 0
        
        pdf_reader.close(document)
    
    def test_extract_all_text_page_order(self, text_extractor, pdf_reader, temp_multipage_pdf):
        """测试文本顺序保持不变（需求 2.2，属性 4）"""
        document = pdf_reader.open(temp_multipage_pdf)
        
        content = text_extractor.extract_all_text(document)
        
        # 验证页面按顺序排列
        for i, page in enumerate(content.pages):
            assert page.page_number == i
        
        # 验证总文本中的顺序
        pos1 = content.total_text.find("Page 1")
        pos2 = content.total_text.find("Page 2")
        pos3 = content.total_text.find("Page 3")
        
        assert pos1 < pos2 < pos3
        
        pdf_reader.close(document)
    
    def test_extract_all_text_returns_extracted_content(self, text_extractor, pdf_reader, temp_simple_pdf):
        """测试返回正确的 ExtractedContent 对象"""
        document = pdf_reader.open(temp_simple_pdf)
        
        content = text_extractor.extract_all_text(document)
        
        # 验证对象类型和属性
        assert isinstance(content, ExtractedContent)
        assert content.file_path == document.file_path
        assert content.page_count == document.page_count
        assert isinstance(content.pages, list)
        assert all(isinstance(p, PageText) for p in content.pages)
        assert isinstance(content.total_text, str)
        assert isinstance(content.errors, list)
        
        pdf_reader.close(document)
    
    def test_extract_all_text_char_count(self, text_extractor, pdf_reader, temp_simple_pdf):
        """测试字符计数正确"""
        document = pdf_reader.open(temp_simple_pdf)
        
        content = text_extractor.extract_all_text(document)
        
        # 每个页面的字符数应该等于文本长度
        for page in content.pages:
            assert page.char_count == len(page.text)
        
        pdf_reader.close(document)
    
    def test_extract_all_text_chinese_content(self, text_extractor, pdf_reader, temp_chinese_pdf):
        """测试中文内容提取（需求 3.1, 3.2, 3.3, 3.4, 3.5）"""
        document = pdf_reader.open(temp_chinese_pdf)
        
        content = text_extractor.extract_all_text(document)
        
        # 验证 UTF-8 编码正确
        assert content.total_text.encode('utf-8').decode('utf-8') == content.total_text
        
        # 验证包含中文或英文内容
        assert len(content.total_text) > 0
        
        pdf_reader.close(document)


class TestErrorRecovery:
    """测试错误恢复机制"""
    
    def test_extract_all_text_continues_on_error(self, text_extractor, pdf_reader, temp_multipage_pdf):
        """测试部分页面失败时继续处理（需求 2.5）
        
        注意：这个测试验证错误恢复机制的结构，但在正常 PDF 上不会触发实际错误。
        实际的错误恢复会在处理损坏的 PDF 时发生。
        """
        document = pdf_reader.open(temp_multipage_pdf)
        
        content = text_extractor.extract_all_text(document)
        
        # 正常情况下应该没有错误
        assert len(content.errors) == 0
        
        # 所有页面都应该被处理
        assert len(content.pages) == document.page_count
        
        pdf_reader.close(document)
    
    def test_extract_all_text_error_list_structure(self, text_extractor, pdf_reader, temp_simple_pdf):
        """测试错误列表结构正确"""
        document = pdf_reader.open(temp_simple_pdf)
        
        content = text_extractor.extract_all_text(document)
        
        # 错误列表应该是列表类型
        assert isinstance(content.errors, list)
        
        # 正常情况下应该为空
        assert len(content.errors) == 0
        
        pdf_reader.close(document)


class TestEdgeCases:
    """测试边缘情况"""
    
    def test_extract_text_from_closed_document(self, text_extractor, pdf_reader, temp_simple_pdf):
        """测试从已关闭的文档提取文本"""
        document = pdf_reader.open(temp_simple_pdf)
        pdf_reader.close(document)
        
        # 尝试从已关闭的文档提取文本应该失败
        with pytest.raises(PageExtractionError) as exc_info:
            text_extractor.extract_text(document, 0)
        
        assert "未正确打开" in str(exc_info.value)
    
    def test_extract_all_text_empty_pdf(self, text_extractor, pdf_reader, tmp_path):
        """测试提取只有一个空页的 PDF"""
        pdf_path = tmp_path / "empty.pdf"
        c = canvas.Canvas(str(pdf_path), pagesize=letter)
        c.showPage()
        c.save()
        
        document = pdf_reader.open(str(pdf_path))
        content = text_extractor.extract_all_text(document)
        
        assert content.page_count == 1
        assert len(content.pages) == 1
        assert content.pages[0].is_empty
        assert content.total_text == ""
        
        pdf_reader.close(document)
