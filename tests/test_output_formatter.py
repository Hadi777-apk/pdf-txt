"""OutputFormatter 单元测试"""

import json
import os
import tempfile
import pytest
from src.output_formatter import OutputFormatter
from src.models import ExtractedContent, PageText, KeyInformation


class TestOutputFormatter:
    """OutputFormatter 类的单元测试"""
    
    @pytest.fixture
    def formatter(self):
        """创建 OutputFormatter 实例"""
        return OutputFormatter()
    
    @pytest.fixture
    def simple_content(self):
        """创建简单的提取内容"""
        pages = [
            PageText(page_number=0, text="第一页内容", char_count=5, is_empty=False),
            PageText(page_number=1, text="第二页内容", char_count=5, is_empty=False)
        ]
        return ExtractedContent(
            file_path="test.pdf",
            page_count=2,
            pages=pages,
            total_text="第一页内容第二页内容",
            extraction_time=0.5
        )
    
    @pytest.fixture
    def content_with_key_info(self):
        """创建包含关键信息的提取内容"""
        pages = [
            PageText(page_number=0, text="标题：测试文档\n这是一个测试文档。", char_count=15, is_empty=False)
        ]
        key_info = KeyInformation(
            headings=["标题：测试文档"],
            keywords=["测试", "文档"],
            summary="这是一个测试文档。",
            lists=["- 项目1", "- 项目2"]
        )
        return ExtractedContent(
            file_path="test_with_key_info.pdf",
            page_count=1,
            pages=pages,
            total_text="标题：测试文档\n这是一个测试文档。",
            key_info=key_info,
            extraction_time=0.3
        )
    
    @pytest.fixture
    def content_with_errors(self):
        """创建包含错误的提取内容"""
        pages = [
            PageText(page_number=0, text="第一页内容", char_count=5, is_empty=False),
            PageText(page_number=1, text="", char_count=0, is_empty=True)
        ]
        return ExtractedContent(
            file_path="test_with_errors.pdf",
            page_count=2,
            pages=pages,
            total_text="第一页内容",
            errors=["第 2 页提取失败：页面损坏"],
            extraction_time=0.4
        )
    
    def test_format_as_text_simple(self, formatter, simple_content):
        """测试纯文本格式化 - 简单内容"""
        result = formatter.format_as_text(simple_content)
        
        assert "文件路径: test.pdf" in result
        assert "总页数: 2" in result
        assert "=== 第 1 页 ===" in result
        assert "第一页内容" in result
        assert "=== 第 2 页 ===" in result
        assert "第二页内容" in result
    
    def test_format_as_text_with_key_info(self, formatter, content_with_key_info):
        """测试纯文本格式化 - 包含关键信息"""
        result = formatter.format_as_text(content_with_key_info)
        
        assert "关键信息" in result
        assert "标题:" in result
        assert "标题：测试文档" in result
        assert "关键词:" in result
        assert "测试" in result
        assert "文档" in result
        assert "摘要:" in result
        assert "这是一个测试文档。" in result
        assert "列表项:" in result
        assert "- 项目1" in result
        assert "- 项目2" in result
    
    def test_format_as_text_with_errors(self, formatter, content_with_errors):
        """测试纯文本格式化 - 包含错误"""
        result = formatter.format_as_text(content_with_errors)
        
        assert "错误信息" in result
        assert "第 2 页提取失败：页面损坏" in result
        assert "(空页面)" in result
    
    def test_format_as_json_simple(self, formatter, simple_content):
        """测试 JSON 格式化 - 简单内容"""
        result = formatter.format_as_json(simple_content)
        data = json.loads(result)
        
        assert data["file_path"] == "test.pdf"
        assert data["page_count"] == 2
        assert len(data["pages"]) == 2
        assert data["pages"][0]["page_number"] == 1  # 1-based
        assert data["pages"][0]["text"] == "第一页内容"
        assert data["pages"][0]["char_count"] == 5
        assert data["pages"][0]["is_empty"] is False
        assert data["pages"][1]["page_number"] == 2
        assert data["pages"][1]["text"] == "第二页内容"
        assert data["total_text"] == "第一页内容第二页内容"
        assert data["extraction_time"] == 0.5
    
    def test_format_as_json_with_key_info(self, formatter, content_with_key_info):
        """测试 JSON 格式化 - 包含关键信息"""
        result = formatter.format_as_json(content_with_key_info)
        data = json.loads(result)
        
        assert "key_info" in data
        assert data["key_info"]["headings"] == ["标题：测试文档"]
        assert data["key_info"]["keywords"] == ["测试", "文档"]
        assert data["key_info"]["summary"] == "这是一个测试文档。"
        assert data["key_info"]["lists"] == ["- 项目1", "- 项目2"]
    
    def test_format_as_json_with_errors(self, formatter, content_with_errors):
        """测试 JSON 格式化 - 包含错误"""
        result = formatter.format_as_json(content_with_errors)
        data = json.loads(result)
        
        assert "errors" in data
        assert data["errors"] == ["第 2 页提取失败：页面损坏"]
    
    def test_format_as_json_chinese_encoding(self, formatter, simple_content):
        """测试 JSON 格式化 - 中文编码正确"""
        result = formatter.format_as_json(simple_content)
        
        # 确保中文字符没有被转义
        assert "第一页内容" in result
        assert "\\u" not in result  # 不应该有 Unicode 转义
        
        # 确保可以正确解析
        data = json.loads(result)
        assert data["pages"][0]["text"] == "第一页内容"
    
    def test_format_as_markdown_simple(self, formatter, simple_content):
        """测试 Markdown 格式化 - 简单内容"""
        result = formatter.format_as_markdown(simple_content)
        
        assert "# PDF 文本提取结果" in result
        assert "**文件路径:** test.pdf" in result
        assert "**总页数:** 2" in result
        assert "## 第 1 页" in result
        assert "第一页内容" in result
        assert "## 第 2 页" in result
        assert "第二页内容" in result
    
    def test_format_as_markdown_with_key_info(self, formatter, content_with_key_info):
        """测试 Markdown 格式化 - 包含关键信息"""
        result = formatter.format_as_markdown(content_with_key_info)
        
        assert "## 关键信息" in result
        assert "### 标题" in result
        assert "- 标题：测试文档" in result
        assert "### 关键词" in result
        assert "测试, 文档" in result
        assert "### 摘要" in result
        assert "这是一个测试文档。" in result
        assert "### 列表项" in result
        assert "- - 项目1" in result
        assert "- - 项目2" in result
    
    def test_format_as_markdown_with_errors(self, formatter, content_with_errors):
        """测试 Markdown 格式化 - 包含错误"""
        result = formatter.format_as_markdown(content_with_errors)
        
        assert "## 错误信息" in result
        assert "- 第 2 页提取失败：页面损坏" in result
        assert "*(空页面)*" in result
    
    def test_save_to_file_success(self, formatter):
        """测试文件保存 - 成功"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
            temp_path = f.name
        
        try:
            content = "测试内容\n包含中文"
            result = formatter.save_to_file(content, temp_path)
            
            assert "文件保存成功" in result
            assert temp_path in result
            
            # 验证文件内容
            with open(temp_path, 'r', encoding='utf-8') as f:
                saved_content = f.read()
            assert saved_content == content
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_save_to_file_utf8_encoding(self, formatter):
        """测试文件保存 - UTF-8 编码"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
            temp_path = f.name
        
        try:
            # 包含各种中文字符
            content = "简体中文：你好世界\n繁體中文：你好世界\n中文标点：，。！？、；：""''（）【】《》"
            formatter.save_to_file(content, temp_path)
            
            # 读取并验证
            with open(temp_path, 'r', encoding='utf-8') as f:
                saved_content = f.read()
            assert saved_content == content
            
            # 验证编码正确
            assert saved_content.encode('utf-8').decode('utf-8') == content
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_save_to_file_overwrite(self, formatter):
        """测试文件保存 - 覆盖已存在的文件"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
            temp_path = f.name
            f.write("旧内容")
        
        try:
            new_content = "新内容"
            result = formatter.save_to_file(new_content, temp_path)
            
            assert "文件保存成功" in result
            
            # 验证文件被覆盖
            with open(temp_path, 'r', encoding='utf-8') as f:
                saved_content = f.read()
            assert saved_content == new_content
            assert saved_content != "旧内容"
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_save_to_file_invalid_path(self, formatter):
        """测试文件保存 - 无效路径"""
        invalid_path = "/invalid/path/that/does/not/exist/test.txt"
        content = "测试内容"
        
        with pytest.raises(IOError) as exc_info:
            formatter.save_to_file(content, invalid_path)
        
        assert "文件保存失败" in str(exc_info.value)
    
    def test_format_as_text_empty_pages(self, formatter):
        """测试纯文本格式化 - 空页面"""
        pages = [
            PageText(page_number=0, text="", char_count=0, is_empty=True),
            PageText(page_number=1, text="", char_count=0, is_empty=True)
        ]
        content = ExtractedContent(
            file_path="empty.pdf",
            page_count=2,
            pages=pages,
            total_text=""
        )
        
        result = formatter.format_as_text(content)
        
        assert "(空页面)" in result
        assert result.count("(空页面)") == 2
    
    def test_format_as_json_empty_content(self, formatter):
        """测试 JSON 格式化 - 空内容"""
        pages = []
        content = ExtractedContent(
            file_path="empty.pdf",
            page_count=0,
            pages=pages,
            total_text=""
        )
        
        result = formatter.format_as_json(content)
        data = json.loads(result)
        
        assert data["page_count"] == 0
        assert data["pages"] == []
        assert data["total_text"] == ""
    
    def test_format_as_markdown_empty_key_info(self, formatter):
        """测试 Markdown 格式化 - 空关键信息"""
        pages = [PageText(page_number=0, text="内容", char_count=2, is_empty=False)]
        key_info = KeyInformation(
            headings=[],
            keywords=[],
            summary="",
            lists=[]
        )
        content = ExtractedContent(
            file_path="test.pdf",
            page_count=1,
            pages=pages,
            total_text="内容",
            key_info=key_info
        )
        
        result = formatter.format_as_markdown(content)
        
        # 空的关键信息部分不应该显示
        assert "## 关键信息" in result
        # 但是空的子部分不应该显示
        lines = result.split('\n')
        # 检查关键信息部分后面没有内容
        key_info_index = None
        for i, line in enumerate(lines):
            if "## 关键信息" in line:
                key_info_index = i
                break
        
        # 关键信息后应该只有空行和分隔符
        if key_info_index is not None:
            remaining_lines = [l for l in lines[key_info_index+1:] if l.strip()]
            # 如果有内容，应该不是标题、关键词等
            for line in remaining_lines:
                if line.startswith("###"):
                    # 空的部分不应该出现
                    assert False, f"空的关键信息部分不应该显示: {line}"


class TestOutputFormatterIntegration:
    """OutputFormatter 集成测试"""
    
    def test_full_workflow_text_format(self):
        """测试完整工作流 - 文本格式"""
        formatter = OutputFormatter()
        
        # 创建完整的提取内容
        pages = [
            PageText(page_number=0, text="第一页：介绍\n这是一个测试文档。", char_count=15, is_empty=False),
            PageText(page_number=1, text="第二页：详细内容\n包含更多信息。", char_count=17, is_empty=False)
        ]
        key_info = KeyInformation(
            headings=["第一页：介绍", "第二页：详细内容"],
            keywords=["测试", "文档", "信息"],
            summary="这是一个测试文档。",
            lists=["- 介绍", "- 详细内容"]
        )
        content = ExtractedContent(
            file_path="full_test.pdf",
            page_count=2,
            pages=pages,
            total_text="第一页：介绍\n这是一个测试文档。第二页：详细内容\n包含更多信息。",
            key_info=key_info,
            extraction_time=1.2
        )
        
        # 格式化为文本
        text_output = formatter.format_as_text(content)
        
        # 保存到文件
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
            temp_path = f.name
        
        try:
            result = formatter.save_to_file(text_output, temp_path)
            assert "文件保存成功" in result
            
            # 读取并验证
            with open(temp_path, 'r', encoding='utf-8') as f:
                saved_content = f.read()
            assert saved_content == text_output
            assert "第一页：介绍" in saved_content
            assert "关键信息" in saved_content
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_full_workflow_json_format(self):
        """测试完整工作流 - JSON 格式"""
        formatter = OutputFormatter()
        
        pages = [PageText(page_number=0, text="测试内容", char_count=4, is_empty=False)]
        content = ExtractedContent(
            file_path="test.pdf",
            page_count=1,
            pages=pages,
            total_text="测试内容"
        )
        
        # 格式化为 JSON
        json_output = formatter.format_as_json(content)
        
        # 保存到文件
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json', encoding='utf-8') as f:
            temp_path = f.name
        
        try:
            formatter.save_to_file(json_output, temp_path)
            
            # 读取并验证可以解析
            with open(temp_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            assert data["file_path"] == "test.pdf"
            assert data["pages"][0]["text"] == "测试内容"
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_full_workflow_markdown_format(self):
        """测试完整工作流 - Markdown 格式"""
        formatter = OutputFormatter()
        
        pages = [PageText(page_number=0, text="# 标题\n内容", char_count=6, is_empty=False)]
        content = ExtractedContent(
            file_path="test.pdf",
            page_count=1,
            pages=pages,
            total_text="# 标题\n内容"
        )
        
        # 格式化为 Markdown
        md_output = formatter.format_as_markdown(content)
        
        # 保存到文件
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md', encoding='utf-8') as f:
            temp_path = f.name
        
        try:
            formatter.save_to_file(md_output, temp_path)
            
            # 读取并验证
            with open(temp_path, 'r', encoding='utf-8') as f:
                saved_content = f.read()
            assert "# PDF 文本提取结果" in saved_content
            assert "## 第 1 页" in saved_content
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
