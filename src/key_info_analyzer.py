"""关键信息分析器"""

import re
from typing import List
import jieba
from collections import Counter


class KeyInfoAnalyzer:
    """关键信息分析器
    
    用于从文本中提取标题、关键词、摘要和列表等关键信息
    """
    
    def __init__(self):
        """初始化分析器"""
        # 初始化 jieba 分词器
        jieba.setLogLevel(jieba.logging.INFO)
    
    def extract_headings(self, text: str) -> List[str]:
        """提取标题和章节
        
        识别规则:
        - 全大写文本
        - 短行（少于 50 字符）
        - 数字编号开头的行
        
        参数:
            text: 要分析的文本内容
            
        返回:
            识别出的标题列表
        """
        if not text or not text.strip():
            return []
        
        headings = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # 跳过空行
            if not line:
                continue
            
            # 规则 1: 全大写文本（至少 2 个字符）
            if len(line) >= 2 and line.isupper():
                headings.append(line)
                continue
            
            # 规则 2: 短行（少于 50 字符）且不是普通句子
            # 普通句子通常以句号、问号、感叹号结尾
            if len(line) < 50 and not line.endswith(('。', '？', '！', '.', '?', '!')):
                # 检查是否像标题（不包含太多标点符号）
                punctuation_count = sum(1 for c in line if c in '，,、；;：:')
                if punctuation_count <= 1:
                    headings.append(line)
                    continue
            
            # 规则 3: 数字编号开头的行
            # 匹配模式如: "1. ", "1.1 ", "第一章", "一、", "(1)"
            number_patterns = [
                r'^\d+\.\s+',           # 1. 标题
                r'^\d+\.\d+\s+',        # 1.1 标题
                r'^第[一二三四五六七八九十百千万\d]+[章节条款部分]\s*',  # 第一章
                r'^[一二三四五六七八九十百千万]+[、\s]',  # 一、标题
                r'^\(\d+\)',            # (1) 标题
                r'^\[\d+\]',            # [1] 标题
            ]
            
            for pattern in number_patterns:
                if re.match(pattern, line):
                    headings.append(line)
                    break
        
        return headings

    def extract_keywords(self, text: str, top_n: int = 10) -> List[str]:
        """提取关键词
        
        使用 jieba 分词和词频统计识别重要词汇
        
        参数:
            text: 要分析的文本内容
            top_n: 返回的关键词数量，默认 10
            
        返回:
            关键词列表，按重要性排序
        """
        if not text or not text.strip():
            return []
        
        # 使用 jieba 分词
        words = jieba.cut(text)
        
        # 过滤停用词和无意义词
        # 停用词包括：标点符号、单字符、纯数字、常见虚词
        stopwords = {
            '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一',
            '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有',
            '看', '好', '自己', '这', '那', '里', '为', '以', '个', '用', '来', '他',
            '她', '它', '们', '这个', '那个', '什么', '怎么', '可以', '但是', '如果',
            '因为', '所以', '虽然', '然而', '而且', '或者', '并且', '但', '与', '及',
            '等', '等等', '之', '于', '对', '从', '把', '被', '让', '给', '向', '往',
            '由', '将', '得', '地', '得到', '进行', '通过', '根据', '按照', '关于',
        }
        
        # 统计词频
        word_counts = Counter()
        for word in words:
            word = word.strip()
            # 过滤条件：
            # 1. 长度至少 2 个字符
            # 2. 不是停用词
            # 3. 不是纯数字
            # 4. 不是纯标点符号
            if (len(word) >= 2 and 
                word not in stopwords and 
                not word.isdigit() and
                not all(c in '，。！？、；：""''（）【】《》\n\t ,.!?;:\'"()[]<>' for c in word)):
                word_counts[word] += 1
        
        # 返回出现频率最高的 top_n 个词
        top_keywords = [word for word, count in word_counts.most_common(top_n)]
        return top_keywords

    def generate_summary(self, text: str, max_length: int = 200) -> str:
        """生成文本摘要
        
        提取前几句作为摘要
        
        参数:
            text: 要分析的文本内容
            max_length: 摘要的最大长度（字符数），默认 200
            
        返回:
            生成的摘要文本
        """
        if not text or not text.strip():
            return ""
        
        # 清理文本
        text = text.strip()
        
        # 如果文本本身就很短，直接返回
        if len(text) <= max_length:
            return text
        
        # 按句子分割（中英文句号、问号、感叹号）
        sentence_endings = r'[。！？\.!?]+'
        sentences = re.split(sentence_endings, text)
        
        # 过滤空句子
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            # 如果没有明显的句子分隔符，直接截取前 max_length 个字符
            return text[:max_length] + ('...' if len(text) > max_length else '')
        
        # 逐句添加，直到达到最大长度
        summary = ""
        for sentence in sentences:
            # 如果添加这句话会超过最大长度
            if len(summary) + len(sentence) > max_length:
                # 如果 summary 已经有内容，就停止
                if summary:
                    break
                # 如果 summary 还是空的，至少要包含第一句的一部分
                summary = sentence[:max_length] + '...'
                break
            
            summary += sentence
            # 添加句号（如果原文有的话）
            if len(summary) < len(text) and text[len(summary)] in '。！？.!?':
                summary += text[len(summary)]
        
        return summary.strip()

    def extract_lists(self, text: str) -> List[str]:
        """提取列表和要点
        
        识别规则:
        - 以 •、-、* 开头的行
        - 数字编号列表
        
        参数:
            text: 要分析的文本内容
            
        返回:
            识别出的列表项列表
        """
        if not text or not text.strip():
            return []
        
        lists = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # 跳过空行
            if not line:
                continue
            
            # 规则 1: 以特殊符号开头的列表项
            # 匹配: •、-、*、○、●、□、■、◆、◇、▪、▫
            if re.match(r'^[•\-*○●□■◆◇▪▫]\s+', line):
                # 移除列表标记，只保留内容
                content = re.sub(r'^[•\-*○●□■◆◇▪▫]\s+', '', line)
                lists.append(content)
                continue
            
            # 规则 2: 数字编号列表
            # 匹配模式如: "1. ", "1) ", "(1) ", "1、"
            number_list_patterns = [
                r'^\d+\.\s+',           # 1. 项目
                r'^\d+\)\s+',           # 1) 项目
                r'^\(\d+\)\s+',         # (1) 项目
                r'^\d+、\s*',           # 1、项目
            ]
            
            for pattern in number_list_patterns:
                match = re.match(pattern, line)
                if match:
                    # 移除编号，只保留内容
                    content = re.sub(pattern, '', line)
                    lists.append(content)
                    break
        
        return lists
