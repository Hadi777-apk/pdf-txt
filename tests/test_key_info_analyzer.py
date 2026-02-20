"""KeyInfoAnalyzer 单元测试"""

import pytest
from src.key_info_analyzer import KeyInfoAnalyzer


class TestKeyInfoAnalyzer:
    """KeyInfoAnalyzer 类的单元测试"""
    
    def setup_method(self):
        """每个测试方法前的设置"""
        self.analyzer = KeyInfoAnalyzer()
    
    # ========== extract_headings 测试 ==========
    
    def test_extract_headings_empty_text(self):
        """测试空文本"""
        assert self.analyzer.extract_headings("") == []
        assert self.analyzer.extract_headings("   ") == []
    
    def test_extract_headings_uppercase(self):
        """测试全大写标题"""
        text = "INTRODUCTION\n这是正文内容。\nCONCLUSION"
        headings = self.analyzer.extract_headings(text)
        assert "INTRODUCTION" in headings
        assert "CONCLUSION" in headings
    
    def test_extract_headings_short_lines(self):
        """测试短行标题"""
        text = "第一章 概述\n这是一段很长的正文内容，包含了很多信息。\n第二章 详细说明"
        headings = self.analyzer.extract_headings(text)
        assert "第一章 概述" in headings
        assert "第二章 详细说明" in headings
    
    def test_extract_headings_numbered(self):
        """测试数字编号标题"""
        text = """1. 引言
这是引言的内容。
1.1 背景
背景信息。
第一章 基础知识
一、重要概念
(1) 第一个要点"""
        headings = self.analyzer.extract_headings(text)
        assert any("1. 引言" in h for h in headings)
        assert any("1.1 背景" in h for h in headings)
        assert any("第一章" in h for h in headings)
        assert any("一、" in h for h in headings)
    
    def test_extract_headings_ignores_sentences(self):
        """测试忽略普通句子"""
        text = "这是一个普通的句子。\n这是另一个句子！\n标题行"
        headings = self.analyzer.extract_headings(text)
        # 普通句子不应该被识别为标题
        assert "这是一个普通的句子。" not in headings
        assert "这是另一个句子！" not in headings
        # 短行应该被识别
        assert "标题行" in headings
    
    # ========== extract_keywords 测试 ==========
    
    def test_extract_keywords_empty_text(self):
        """测试空文本"""
        assert self.analyzer.extract_keywords("") == []
        assert self.analyzer.extract_keywords("   ") == []
    
    def test_extract_keywords_basic(self):
        """测试基本关键词提取"""
        text = "人工智能是计算机科学的一个分支。人工智能研究如何让计算机模拟人类智能。"
        keywords = self.analyzer.extract_keywords(text, top_n=5)
        # 应该包含高频词
        assert "人工智能" in keywords or "人工" in keywords or "智能" in keywords
        # 计算机可能被分词为"计算机"或"计算机科学"
        assert any("计算机" in kw for kw in keywords)
    
    def test_extract_keywords_filters_stopwords(self):
        """测试过滤停用词"""
        text = "这是一个测试文本。这个文本包含很多停用词，比如的、了、在等。但是关键词应该被提取出来。"
        keywords = self.analyzer.extract_keywords(text, top_n=10)
        # 停用词不应该出现
        assert "的" not in keywords
        assert "了" not in keywords
        assert "在" not in keywords
        assert "这" not in keywords
    
    def test_extract_keywords_top_n(self):
        """测试返回指定数量的关键词"""
        text = "机器学习 深度学习 神经网络 自然语言处理 计算机视觉 " * 10
        keywords = self.analyzer.extract_keywords(text, top_n=3)
        assert len(keywords) <= 3
    
    # ========== generate_summary 测试 ==========
    
    def test_generate_summary_empty_text(self):
        """测试空文本"""
        assert self.analyzer.generate_summary("") == ""
        assert self.analyzer.generate_summary("   ") == ""
    
    def test_generate_summary_short_text(self):
        """测试短文本（不需要截断）"""
        text = "这是一段很短的文本。"
        summary = self.analyzer.generate_summary(text, max_length=100)
        assert summary == text
    
    def test_generate_summary_long_text(self):
        """测试长文本（需要截断）"""
        text = "第一句话。第二句话。第三句话。第四句话。第五句话。"
        summary = self.analyzer.generate_summary(text, max_length=20)
        # 摘要应该短于原文
        assert len(summary) <= 20
        # 摘要应该包含文本的开头部分
        assert summary.startswith("第一句话")
    
    def test_generate_summary_respects_max_length(self):
        """测试摘要长度约束"""
        text = "这是一段很长的文本。" * 50
        max_length = 50
        summary = self.analyzer.generate_summary(text, max_length=max_length)
        assert len(summary) <= max_length
    
    def test_generate_summary_multiple_sentences(self):
        """测试多句摘要"""
        text = "第一句。第二句。第三句。第四句。第五句。第六句。第七句。"
        summary = self.analyzer.generate_summary(text, max_length=15)
        # 应该包含文本的开头部分
        assert "第一句" in summary
        # 摘要应该短于原文
        assert len(summary) < len(text)
    
    # ========== extract_lists 测试 ==========
    
    def test_extract_lists_empty_text(self):
        """测试空文本"""
        assert self.analyzer.extract_lists("") == []
        assert self.analyzer.extract_lists("   ") == []
    
    def test_extract_lists_bullet_points(self):
        """测试项目符号列表"""
        text = """正文内容
• 第一项
• 第二项
- 第三项
* 第四项
更多正文"""
        lists = self.analyzer.extract_lists(text)
        assert "第一项" in lists
        assert "第二项" in lists
        assert "第三项" in lists
        assert "第四项" in lists
    
    def test_extract_lists_numbered(self):
        """测试数字编号列表"""
        text = """1. 第一项
2. 第二项
3) 第三项
(4) 第四项
5、第五项"""
        lists = self.analyzer.extract_lists(text)
        assert "第一项" in lists
        assert "第二项" in lists
        assert "第三项" in lists
        assert "第四项" in lists
        assert "第五项" in lists
    
    def test_extract_lists_mixed(self):
        """测试混合列表格式"""
        text = """标题
• 项目符号项
1. 数字项
- 另一个项目符号项
正文内容不应该被提取"""
        lists = self.analyzer.extract_lists(text)
        assert "项目符号项" in lists
        assert "数字项" in lists
        assert "另一个项目符号项" in lists
        # 普通文本不应该被提取
        assert "正文内容不应该被提取" not in lists
    
    def test_extract_lists_removes_markers(self):
        """测试列表标记被移除"""
        text = "• 内容项\n1. 编号项"
        lists = self.analyzer.extract_lists(text)
        # 列表项不应该包含标记符号
        assert lists[0] == "内容项"
        assert lists[1] == "编号项"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
