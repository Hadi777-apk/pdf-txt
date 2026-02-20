"""KeyInfoAnalyzer 集成测试"""

import pytest
from src.key_info_analyzer import KeyInfoAnalyzer
from src.models import KeyInformation


class TestKeyInfoAnalyzerIntegration:
    """测试 KeyInfoAnalyzer 与其他组件的集成"""
    
    def setup_method(self):
        """每个测试方法前的设置"""
        self.analyzer = KeyInfoAnalyzer()
    
    def test_analyze_complete_document(self):
        """测试分析完整文档"""
        # 模拟一个完整的文档内容
        text = """第一章 人工智能概述

人工智能（Artificial Intelligence，AI）是计算机科学的一个重要分支。
人工智能研究如何让计算机模拟人类的智能行为。

主要应用领域包括：
• 自然语言处理
• 计算机视觉
• 机器学习
• 深度学习

1. 机器学习基础
机器学习是人工智能的核心技术之一。

2. 深度学习进阶
深度学习使用神经网络进行复杂的模式识别。

结论：人工智能正在改变我们的世界。"""
        
        # 提取所有关键信息
        headings = self.analyzer.extract_headings(text)
        keywords = self.analyzer.extract_keywords(text, top_n=5)
        summary = self.analyzer.generate_summary(text, max_length=100)
        lists = self.analyzer.extract_lists(text)
        
        # 验证标题提取
        assert len(headings) > 0
        assert any("第一章" in h for h in headings)
        
        # 验证关键词提取
        assert len(keywords) > 0
        assert any("人工智能" in kw or "智能" in kw for kw in keywords)
        
        # 验证摘要生成
        assert len(summary) > 0
        assert len(summary) <= 100
        assert "人工智能" in summary or "Artificial" in summary
        
        # 验证列表提取
        assert len(lists) > 0
        assert "自然语言处理" in lists
        assert "计算机视觉" in lists
    
    def test_create_key_information_object(self):
        """测试创建 KeyInformation 对象"""
        text = """标题行

这是一段测试文本。包含关键词：测试、文本、关键词。

• 列表项1
• 列表项2"""
        
        # 提取信息并创建 KeyInformation 对象
        key_info = KeyInformation(
            headings=self.analyzer.extract_headings(text),
            keywords=self.analyzer.extract_keywords(text, top_n=5),
            summary=self.analyzer.generate_summary(text, max_length=50),
            lists=self.analyzer.extract_lists(text)
        )
        
        # 验证对象创建成功
        assert isinstance(key_info, KeyInformation)
        assert len(key_info.headings) > 0
        assert len(key_info.keywords) > 0
        assert len(key_info.summary) > 0
        assert len(key_info.lists) == 2
    
    def test_handle_chinese_and_english_mixed(self):
        """测试处理中英文混合内容"""
        text = """Introduction to AI

人工智能（Artificial Intelligence）是一个跨学科领域。

Key Points:
• Machine Learning 机器学习
• Deep Learning 深度学习
• Natural Language Processing 自然语言处理

1. What is AI?
AI是计算机科学的一个分支。

2. Applications 应用
AI应用广泛，包括语音识别、图像识别等。"""
        
        headings = self.analyzer.extract_headings(text)
        keywords = self.analyzer.extract_keywords(text, top_n=10)
        summary = self.analyzer.generate_summary(text, max_length=100)
        lists = self.analyzer.extract_lists(text)
        
        # 应该能够处理中英文混合内容
        assert len(headings) > 0
        assert len(keywords) > 0
        assert len(summary) > 0
        assert len(lists) >= 3  # 至少有3个列表项
    
    def test_empty_document(self):
        """测试空文档"""
        text = ""
        
        key_info = KeyInformation(
            headings=self.analyzer.extract_headings(text),
            keywords=self.analyzer.extract_keywords(text),
            summary=self.analyzer.generate_summary(text),
            lists=self.analyzer.extract_lists(text)
        )
        
        # 空文档应该返回空的关键信息
        assert len(key_info.headings) == 0
        assert len(key_info.keywords) == 0
        assert key_info.summary == ""
        assert len(key_info.lists) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
