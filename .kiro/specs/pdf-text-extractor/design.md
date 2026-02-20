# 设计文档

## 概述

PDF 文本提取工具是一个命令行应用程序，用于从 PDF 文件中提取文本内容并识别关键信息。系统采用模块化设计，将 PDF 读取、文本提取、关键信息识别和输出格式化分离为独立组件，确保代码的可维护性和可扩展性。

核心设计原则：
- 使用成熟的 PDF 处理库（PyPDF2 或 pdfplumber）处理 PDF 文件
- 支持 UTF-8 编码以确保中文内容的正确处理
- 提供清晰的错误处理和用户反馈
- 采用管道式架构，数据流从文件读取到最终输出

## 架构

系统采用分层架构，包含以下主要层次：

```
┌─────────────────────────────────────┐
│      命令行接口层 (CLI Layer)        │
│   - 参数解析                         │
│   - 用户交互                         │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│    应用服务层 (Application Layer)    │
│   - 工作流协调                       │
│   - 错误处理                         │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│    核心业务层 (Core Layer)           │
│   - PDF 读取器                       │
│   - 文本提取器                       │
│   - 关键信息分析器                   │
│   - 输出格式化器                     │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│    基础设施层 (Infrastructure)       │
│   - 文件系统访问                     │
│   - 日志记录                         │
│   - 配置管理                         │
└─────────────────────────────────────┘
```

数据流：
1. 用户通过 CLI 提供 PDF 文件路径和选项
2. 应用服务层验证输入并协调处理流程
3. PDF 读取器打开并读取文件
4. 文本提取器从 PDF 中提取文本内容
5. 关键信息分析器识别重要信息
6. 输出格式化器生成最终输出
7. 结果返回给用户

## 组件和接口

### 1. PDF 读取器 (PDFReader)

负责打开和读取 PDF 文件。

```python
class PDFReader:
    """PDF 文件读取器"""
    
    def open(file_path: str) -> PDFDocument:
        """
        打开 PDF 文件
        
        参数:
            file_path: PDF 文件的完整路径
            
        返回:
            PDFDocument 对象
            
        异常:
            FileNotFoundError: 文件不存在
            InvalidPDFError: 文件不是有效的 PDF
            PermissionError: 没有读取权限
        """
        pass
    
    def get_page_count(document: PDFDocument) -> int:
        """获取 PDF 页数"""
        pass
    
    def close(document: PDFDocument) -> None:
        """关闭 PDF 文件"""
        pass
```

### 2. 文本提取器 (TextExtractor)

从 PDF 文档中提取文本内容。

```python
class TextExtractor:
    """文本内容提取器"""
    
    def extract_text(document: PDFDocument, page_number: int) -> str:
        """
        从指定页面提取文本
        
        参数:
            document: PDF 文档对象
            page_number: 页码（从 0 开始）
            
        返回:
            提取的文本内容
            
        异常:
            ExtractionError: 提取失败
        """
        pass
    
    def extract_all_text(document: PDFDocument) -> List[PageText]:
        """
        提取所有页面的文本
        
        返回:
            包含所有页面文本的列表
        """
        pass
```

### 3. 关键信息分析器 (KeyInfoAnalyzer)

识别和提取文本中的关键信息。

```python
class KeyInfoAnalyzer:
    """关键信息分析器"""
    
    def extract_headings(text: str) -> List[str]:
        """
        提取标题和章节
        
        识别规则:
        - 全大写文本
        - 短行（少于 50 字符）
        - 数字编号开头的行
        """
        pass
    
    def extract_keywords(text: str, top_n: int = 10) -> List[str]:
        """
        提取关键词
        
        使用 TF-IDF 或词频统计识别重要词汇
        """
        pass
    
    def generate_summary(text: str, max_length: int = 200) -> str:
        """
        生成文本摘要
        
        提取前几句或使用简单的摘要算法
        """
        pass
    
    def extract_lists(text: str) -> List[str]:
        """
        提取列表和要点
        
        识别规则:
        - 以 •、-、* 开头的行
        - 数字编号列表
        """
        pass
```

### 4. 输出格式化器 (OutputFormatter)

将提取的内容格式化为不同的输出格式。

```python
class OutputFormatter:
    """输出格式化器"""
    
    def format_as_text(content: ExtractedContent) -> str:
        """格式化为纯文本"""
        pass
    
    def format_as_json(content: ExtractedContent) -> str:
        """
        格式化为 JSON
        
        结构:
        {
            "file_path": "...",
            "page_count": 10,
            "pages": [
                {"page_number": 1, "text": "..."},
                ...
            ],
            "key_info": {
                "headings": [...],
                "keywords": [...],
                "summary": "..."
            }
        }
        """
        pass
    
    def format_as_markdown(content: ExtractedContent) -> str:
        """格式化为 Markdown"""
        pass
    
    def save_to_file(content: str, output_path: str) -> None:
        """
        将内容保存到文件
        
        参数:
            content: 要保存的文本内容
            output_path: 输出文件路径
            
        异常:
            IOError: 文件写入失败
        """
        pass
```

### 5. 路径处理器 (PathHandler)

处理和验证文件路径。

```python
class PathHandler:
    """文件路径处理器"""
    
    def normalize_path(path: str) -> str:
        """
        规范化路径
        
        - 处理反斜杠和正斜杠
        - 展开相对路径
        - 处理中文字符
        """
        pass
    
    def validate_path(path: str) -> bool:
        """验证路径是否有效"""
        pass
    
    def is_pdf_file(path: str) -> bool:
        """检查文件是否为 PDF"""
        pass
```

### 6. 应用服务 (ApplicationService)

协调整个提取流程。

```python
class PDFExtractionService:
    """PDF 提取服务"""
    
    def __init__(self):
        self.reader = PDFReader()
        self.extractor = TextExtractor()
        self.analyzer = KeyInfoAnalyzer()
        self.formatter = OutputFormatter()
        self.path_handler = PathHandler()
    
    def extract(
        file_path: str,
        output_format: str = "text",
        extract_key_info: bool = True,
        output_file: Optional[str] = None
    ) -> str:
        """
        执行完整的提取流程
        
        参数:
            file_path: PDF 文件路径
            output_format: 输出格式 (text, json, markdown)
            extract_key_info: 是否提取关键信息
            output_file: 输出文件路径（可选），如果提供则保存到文件
            
        返回:
            格式化的提取结果
        """
        pass
```

## 数据模型

### PDFDocument

表示打开的 PDF 文档。

```python
class PDFDocument:
    """PDF 文档对象"""
    file_path: str
    page_count: int
    metadata: Dict[str, Any]  # 标题、作者等元数据
    _internal_handle: Any     # 底层 PDF 库的文档对象
```

### PageText

表示单个页面的文本内容。

```python
class PageText:
    """页面文本"""
    page_number: int
    text: str
    char_count: int
    is_empty: bool
```

### ExtractedContent

表示完整的提取结果。

```python
class ExtractedContent:
    """提取的内容"""
    file_path: str
    page_count: int
    pages: List[PageText]
    total_text: str
    key_info: Optional[KeyInformation]
    extraction_time: float
    errors: List[str]  # 提取过程中的错误
```

### KeyInformation

表示识别出的关键信息。

```python
class KeyInformation:
    """关键信息"""
    headings: List[str]
    keywords: List[str]
    summary: str
    lists: List[str]
```

### ExtractionError

自定义异常类型。

```python
class PDFExtractionError(Exception):
    """PDF 提取错误基类"""
    pass

class FileNotFoundError(PDFExtractionError):
    """文件不存在"""
    pass

class InvalidPDFError(PDFExtractionError):
    """无效的 PDF 文件"""
    pass

class ExtractionError(PDFExtractionError):
    """文本提取失败"""
    pass
```

## 技术选型

### PDF 处理库

推荐使用 **pdfplumber**：
- 优秀的中文支持
- 更准确的文本提取
- 保持文本布局和结构
- 活跃的社区维护

备选方案：**PyPDF2**
- 轻量级
- 广泛使用
- 但中文支持较弱

### 关键信息提取

- **jieba**：中文分词，用于关键词提取
- **正则表达式**：识别标题、列表等结构化内容
- **简单统计算法**：词频、TF-IDF

### 命令行接口

- **argparse**：Python 标准库，用于参数解析
- **rich**：美化命令行输出（可选）

## 实现细节

### 中文编码处理

所有文本处理使用 UTF-8 编码：

```python
# 读取文件时指定编码
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 输出时确保编码
output = text.encode('utf-8').decode('utf-8')
```

### Windows 路径处理

```python
import os
from pathlib import Path

def normalize_path(path: str) -> str:
    # 使用 pathlib 处理跨平台路径
    return str(Path(path).resolve())
```

### 错误处理策略

1. **文件级错误**：立即返回，提供清晰错误信息
2. **页面级错误**：记录错误，继续处理其他页面
3. **部分提取失败**：返回成功部分，标注失败页面

```python
def extract_all_text(document: PDFDocument) -> ExtractedContent:
    pages = []
    errors = []
    
    for i in range(document.page_count):
        try:
            text = extract_text(document, i)
            pages.append(PageText(i, text))
        except ExtractionError as e:
            errors.append(f"页面 {i+1} 提取失败: {str(e)}")
            pages.append(PageText(i, "", is_empty=True))
    
    return ExtractedContent(pages=pages, errors=errors)
```

### 进度指示

对于大文件，提供进度反馈：

```python
def extract_with_progress(document: PDFDocument):
    total_pages = document.page_count
    
    for i in range(total_pages):
        print(f"处理进度: {i+1}/{total_pages} ({(i+1)/total_pages*100:.1f}%)")
        extract_text(document, i)
```



## 正确性属性

属性是一种特征或行为，应该在系统的所有有效执行中保持为真——本质上是关于系统应该做什么的形式化陈述。属性是人类可读规范和机器可验证正确性保证之间的桥梁。

### 属性 1：有效 PDF 文件可读性

*对于任何*有效的 PDF 文件和有效的文件路径，系统应该能够成功打开并读取该文件，返回包含正确页数的 PDFDocument 对象。

**验证需求：1.1, 1.4**

### 属性 2：错误条件正确分类

*对于任何*无效输入（不存在的路径、非 PDF 文件、无权限文件），系统应该返回对应类型的特定错误（FileNotFoundError、InvalidPDFError、PermissionError），而不是通用错误。

**验证需求：1.2, 1.3, 6.2**

### 属性 3：文本提取完整性

*对于任何*成功打开的 PDF 文档，提取所有页面的文本后，提取的页面数量应该等于文档的总页数。

**验证需求：2.1, 2.3**

### 属性 4：文本顺序保持不变

*对于任何*包含有序内容的 PDF（如编号列表 1, 2, 3），提取后的文本应该保持相同的顺序。

**验证需求：2.2**

### 属性 5：部分失败不影响成功部分

*对于任何*包含部分损坏页面的 PDF，提取过程应该返回成功提取的页面内容，并在错误列表中标注失败的页面号，而不是完全失败。

**验证需求：2.5, 6.5**

### 属性 6：中文内容正确提取

*对于任何*包含中文字符（简体、繁体、标点符号）或中英文混合内容的 PDF，提取后的文本应该包含所有中文字符且编码正确，没有乱码。

**验证需求：3.1, 3.2, 3.3, 3.4, 3.5**

### 属性 7：路径规范化一致性

*对于任何*有效的文件路径（绝对路径、相对路径、包含中文、包含空格），路径处理器应该能够将其规范化为系统可识别的标准路径，且规范化后的路径指向同一文件。

**验证需求：4.1, 4.2, 4.3, 4.4**

### 属性 8：无效路径被拒绝

*对于任何*格式错误或不存在的路径，路径验证应该返回 False 或抛出适当的异常。

**验证需求：4.5**

### 属性 9：标题识别准确性

*对于任何*包含明显标题特征的文本（全大写、短行、数字编号开头），关键信息分析器应该能够识别这些标题并将其包含在标题列表中。

**验证需求：5.1**

### 属性 10：关键词提取相关性

*对于任何*文本内容，提取的关键词应该在原文中出现，且出现频率应该高于平均水平。

**验证需求：5.2**

### 属性 11：摘要长度约束

*对于任何*文本内容和指定的最大长度，生成的摘要长度应该不超过指定的最大长度，且应该短于原文。

**验证需求：5.3**

### 属性 12：列表结构保持

*对于任何*包含列表标记（•、-、*、数字编号）的文本，提取列表后应该保持原有的列表项，不丢失内容。

**验证需求：5.4**

### 属性 13：错误消息中文化

*对于任何*错误情况，返回的错误消息应该包含中文字符，而不是纯英文消息。

**验证需求：6.1**

### 属性 14：错误日志记录

*对于任何*发生的错误，系统应该在日志中记录错误类型、错误消息和发生时间。

**验证需求：6.4**

### 属性 15：纯文本输出格式

*对于任何*提取的内容，格式化为纯文本后应该是有效的字符串，且包含所有页面的文本内容。

**验证需求：7.1**

### 属性 16：JSON 序列化往返一致性

*对于任何*提取的内容对象，将其序列化为 JSON 然后反序列化，应该得到等价的对象（包含相同的文本、页码、关键信息）。

**验证需求：7.2, 7.3**

### 属性 17：UTF-8 编码一致性

*对于任何*输出格式，输出的文本应该是有效的 UTF-8 编码，能够被 UTF-8 解码器正确解码。

**验证需求：7.4**

### 属性 18：文件保存往返一致性

*对于任何*提取的文本内容，将其保存到文件然后读取回来，读取的内容应该与原始内容完全一致（包括中文字符和格式）。

**验证需求：8.1, 8.2, 8.4**

### 属性 19：文件保存成功反馈

*对于任何*成功的文件保存操作，系统应该返回包含输出文件路径的成功消息。

**验证需求：8.5**

## 错误处理

### 错误类型层次

```
PDFExtractionError (基类)
├── FileNotFoundError (文件不存在)
├── InvalidPDFError (无效的 PDF 格式)
├── PermissionError (权限不足)
├── ExtractionError (提取失败)
│   ├── PageExtractionError (单页提取失败)
│   └── EncodingError (编码错误)
└── PathError (路径错误)
```

### 错误处理原则

1. **快速失败**：文件级错误（文件不存在、格式错误）立即返回
2. **优雅降级**：页面级错误记录后继续处理其他页面
3. **详细信息**：所有错误包含中文消息和上下文信息
4. **日志记录**：所有错误写入日志文件

### 错误消息模板

```python
ERROR_MESSAGES = {
    "file_not_found": "错误：找不到文件 '{path}'，请检查路径是否正确",
    "invalid_pdf": "错误：文件 '{path}' 不是有效的 PDF 文件",
    "permission_denied": "错误：没有权限读取文件 '{path}'",
    "extraction_failed": "错误：提取第 {page} 页时失败：{reason}",
    "encoding_error": "错误：文本编码转换失败，可能包含不支持的字符",
    "invalid_path": "错误：路径 '{path}' 格式不正确"
}
```

### 错误恢复策略

```python
def extract_all_text_with_recovery(document: PDFDocument) -> ExtractedContent:
    """带错误恢复的文本提取"""
    pages = []
    errors = []
    
    for page_num in range(document.page_count):
        try:
            text = extract_text(document, page_num)
            pages.append(PageText(page_num, text, len(text), False))
        except PageExtractionError as e:
            # 记录错误但继续处理
            error_msg = f"第 {page_num + 1} 页提取失败：{str(e)}"
            errors.append(error_msg)
            logger.error(error_msg)
            # 添加空页面占位
            pages.append(PageText(page_num, "", 0, True))
        except Exception as e:
            # 未预期的错误也要捕获
            error_msg = f"第 {page_num + 1} 页发生未知错误：{str(e)}"
            errors.append(error_msg)
            logger.exception(error_msg)
            pages.append(PageText(page_num, "", 0, True))
    
    return ExtractedContent(
        file_path=document.file_path,
        page_count=document.page_count,
        pages=pages,
        total_text="".join(p.text for p in pages),
        errors=errors
    )
```

## 测试策略

### 双重测试方法

系统将采用单元测试和基于属性的测试相结合的方法：

- **单元测试**：验证特定示例、边缘情况和错误条件
- **属性测试**：验证跨所有输入的通用属性

两者是互补的，对于全面覆盖都是必需的。单元测试捕获具体的错误，属性测试验证一般正确性。

### 单元测试重点

单元测试应该专注于：
- 特定的示例（如特定的 PDF 文件）
- 边缘情况（空 PDF、单页 PDF、超大 PDF）
- 错误条件（文件不存在、权限错误）
- 组件之间的集成点

避免编写过多的单元测试——基于属性的测试会处理大量输入的覆盖。

### 基于属性的测试配置

**测试库选择**：使用 **Hypothesis** 进行基于属性的测试
- Python 生态系统中最成熟的 PBT 库
- 优秀的中文字符生成支持
- 智能的反例缩减
- 与 pytest 无缝集成

**测试配置**：
- 每个属性测试最少运行 100 次迭代
- 每个测试必须引用其设计文档属性
- 标签格式：**Feature: pdf-text-extractor, Property {number}: {property_text}**

**属性测试示例**：

```python
from hypothesis import given, strategies as st
import hypothesis

# 配置最小迭代次数
hypothesis.settings.register_profile("default", max_examples=100)

@given(st.text(min_size=1))
def test_property_6_chinese_content_extraction(text_content):
    """
    Feature: pdf-text-extractor, Property 6: 中文内容正确提取
    
    对于任何包含中文字符的 PDF，提取后的文本应该包含所有中文字符且编码正确
    """
    # 创建包含文本的临时 PDF
    pdf_path = create_temp_pdf_with_text(text_content)
    
    # 提取文本
    extractor = TextExtractor()
    document = PDFReader().open(pdf_path)
    extracted = extractor.extract_all_text(document)
    
    # 验证：提取的文本应该包含原始中文内容
    assert text_content in extracted.total_text
    # 验证：编码正确（能够正确编码和解码）
    assert extracted.total_text.encode('utf-8').decode('utf-8') == extracted.total_text

@given(st.lists(st.text(), min_size=1, max_size=10))
def test_property_4_text_order_preservation(ordered_texts):
    """
    Feature: pdf-text-extractor, Property 4: 文本顺序保持不变
    
    对于任何包含有序内容的 PDF，提取后的文本应该保持相同的顺序
    """
    # 创建包含有序文本的 PDF
    pdf_path = create_temp_pdf_with_ordered_content(ordered_texts)
    
    # 提取文本
    extractor = TextExtractor()
    document = PDFReader().open(pdf_path)
    extracted = extractor.extract_all_text(document)
    
    # 验证：文本顺序保持不变
    for i, text in enumerate(ordered_texts):
        if i < len(ordered_texts) - 1:
            # 当前文本应该出现在下一个文本之前
            pos_current = extracted.total_text.find(text)
            pos_next = extracted.total_text.find(ordered_texts[i + 1])
            assert pos_current < pos_next

@given(st.text())
def test_property_16_json_serialization_roundtrip(text_content):
    """
    Feature: pdf-text-extractor, Property 16: JSON 序列化往返一致性
    
    对于任何提取的内容对象，序列化为 JSON 然后反序列化应该得到等价的对象
    """
    # 创建提取内容对象
    content = ExtractedContent(
        file_path="test.pdf",
        page_count=1,
        pages=[PageText(0, text_content, len(text_content), False)],
        total_text=text_content,
        errors=[]
    )
    
    # 序列化为 JSON
    formatter = OutputFormatter()
    json_output = formatter.format_as_json(content)
    
    # 反序列化
    import json
    parsed = json.loads(json_output)
    
    # 验证：关键字段应该保持一致
    assert parsed["file_path"] == content.file_path
    assert parsed["page_count"] == content.page_count
    assert parsed["pages"][0]["text"] == text_content
```

### 测试数据生成

使用 Hypothesis 的策略生成测试数据：

```python
from hypothesis import strategies as st

# 中文字符策略
chinese_chars = st.characters(
    whitelist_categories=('Lo',),  # Unicode 字母
    whitelist_characters='，。！？、；：""''（）【】《》'
)

chinese_text = st.text(alphabet=chinese_chars, min_size=1, max_size=1000)

# 路径策略
windows_paths = st.builds(
    lambda parts: "\\".join(parts),
    st.lists(st.text(alphabet=st.characters(blacklist_characters='\\/:*?"<>|')), 
             min_size=1, max_size=5)
)

# PDF 内容策略
pdf_content = st.builds(
    dict,
    pages=st.lists(chinese_text, min_size=1, max_size=20),
    metadata=st.fixed_dictionaries({
        'title': st.text(),
        'author': st.text()
    })
)
```

### 集成测试

测试完整的提取流程：

```python
def test_end_to_end_extraction():
    """端到端测试：从文件读取到输出"""
    # 准备测试 PDF
    test_pdf = "tests/fixtures/sample_chinese.pdf"
    
    # 执行提取
    service = PDFExtractionService()
    result = service.extract(
        file_path=test_pdf,
        output_format="json",
        extract_key_info=True
    )
    
    # 验证结果
    assert result is not None
    assert "pages" in result
    assert "key_info" in result
```

### 性能测试

虽然不是属性测试的一部分，但应该包含基本的性能基准：

```python
def test_large_pdf_performance():
    """测试大文件处理性能"""
    import time
    
    # 100 页的 PDF
    large_pdf = "tests/fixtures/large_document.pdf"
    
    start = time.time()
    service = PDFExtractionService()
    result = service.extract(large_pdf)
    duration = time.time() - start
    
    # 应该在合理时间内完成（如 30 秒）
    assert duration < 30
    assert result.page_count == 100
```

### 测试覆盖率目标

- 代码覆盖率：> 80%
- 属性测试覆盖：所有 19 个属性
- 边缘情况覆盖：空文件、单页、多页、损坏文件
- 错误路径覆盖：所有错误类型
