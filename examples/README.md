# PDF 文本提取工具 - 使用示例

本目录包含 PDF 文本提取工具的各种使用示例，帮助您快速上手并了解工具的各项功能。

## 目录结构

```
examples/
├── README.md                    # 本文件
├── create_sample_pdf.py         # 创建示例 PDF 文件的脚本
├── basic_usage.py               # 基本使用示例
├── advanced_usage.py            # 高级使用示例
├── cli_examples.sh              # CLI 使用示例（Linux/Mac）
├── cli_examples.bat             # CLI 使用示例（Windows）
├── sample_chinese.pdf           # 示例 PDF 文件（运行后生成）
└── output/                      # 输出文件目录（运行后生成）
```

## 快速开始

### 1. 创建示例 PDF 文件

首先，运行以下命令创建包含中文内容的示例 PDF 文件：

```bash
python examples/create_sample_pdf.py
```

这将在 `examples/` 目录下创建 `sample_chinese.pdf` 文件。

**注意**：此脚本需要 `reportlab` 库。如果未安装，请运行：

```bash
pip install reportlab
```

### 2. 运行基本示例

运行基本使用示例，了解工具的核心功能：

```bash
python examples/basic_usage.py
```

此示例包含：
- 基本文本提取
- 保存到文件
- JSON 格式输出
- 提取关键信息
- 错误处理
- 逐页处理

### 3. 运行高级示例

运行高级使用示例，了解更多自定义功能：

```bash
python examples/advanced_usage.py
```

此示例包含：
- 自定义工作流程（使用独立组件）
- 批量处理多个 PDF 文件
- 自定义关键信息提取
- Markdown 格式输出
- 错误恢复和部分提取
- 路径处理示例

### 4. 运行 CLI 示例

#### Linux/Mac：

```bash
chmod +x examples/cli_examples.sh
./examples/cli_examples.sh
```

#### Windows：

```cmd
examples\cli_examples.bat
```

## 示例说明

### 基本使用示例 (basic_usage.py)

#### 示例 1：基本文本提取

```python
from src.pdf_extraction_service import PDFExtractionService

service = PDFExtractionService()
result = service.extract(
    file_path="examples/sample_chinese.pdf",
    output_format="text",
    extract_key_info=False
)

print(f"提取成功！总页数：{result.page_count}")
print(result.total_text)
```

#### 示例 2：保存到文件

```python
result = service.extract(
    file_path="examples/sample_chinese.pdf",
    output_format="text",
    extract_key_info=False,
    output_file="examples/output.txt"
)
```

#### 示例 3：JSON 格式输出

```python
result = service.extract(
    file_path="examples/sample_chinese.pdf",
    output_format="json",
    extract_key_info=False,
    output_file="examples/output.json"
)
```

#### 示例 4：提取关键信息

```python
result = service.extract(
    file_path="examples/sample_chinese.pdf",
    output_format="text",
    extract_key_info=True
)

if result.key_info:
    print("标题：", result.key_info.headings)
    print("关键词：", result.key_info.keywords)
    print("摘要：", result.key_info.summary)
    print("列表：", result.key_info.lists)
```

#### 示例 5：错误处理

```python
try:
    result = service.extract(
        file_path="nonexistent.pdf",
        output_format="text"
    )
except Exception as e:
    print(f"错误：{e}")
```

#### 示例 6：逐页处理

```python
result = service.extract(
    file_path="examples/sample_chinese.pdf",
    output_format="text"
)

for page in result.pages:
    print(f"第 {page.page_number + 1} 页：")
    print(f"  字符数：{page.char_count}")
    print(f"  内容：{page.text[:100]}...")
```

### 高级使用示例 (advanced_usage.py)

#### 示例 1：自定义工作流程

使用独立组件构建自定义提取流程：

```python
from src.pdf_reader import PDFReader
from src.text_extractor import TextExtractor
from src.key_info_analyzer import KeyInfoAnalyzer
from src.output_formatter import OutputFormatter

# 1. 打开 PDF
reader = PDFReader()
document = reader.open("examples/sample_chinese.pdf")

# 2. 提取文本
extractor = TextExtractor()
content = extractor.extract_all_text(document)

# 3. 分析关键信息
analyzer = KeyInfoAnalyzer()
key_info = analyzer.analyze(content.total_text)

# 4. 格式化输出
formatter = OutputFormatter()
content.key_info = key_info
output = formatter.format_as_text(content)

# 5. 清理
reader.close(document)
```

#### 示例 2：批量处理

```python
pdf_files = [
    "file1.pdf",
    "file2.pdf",
    "file3.pdf"
]

service = PDFExtractionService()
results = []

for pdf_file in pdf_files:
    try:
        result = service.extract(
            file_path=pdf_file,
            output_format="json",
            extract_key_info=True
        )
        results.append({
            "file": pdf_file,
            "success": True,
            "page_count": result.page_count
        })
    except Exception as e:
        results.append({
            "file": pdf_file,
            "success": False,
            "error": str(e)
        })
```

#### 示例 3：自定义关键信息提取

```python
analyzer = KeyInfoAnalyzer()

# 提取更多关键词
keywords = analyzer.extract_keywords(text, top_n=20)

# 生成更长的摘要
summary = analyzer.generate_summary(text, max_length=500)

# 提取所有标题
headings = analyzer.extract_headings(text)
```

### CLI 使用示例

#### 基本用法

```bash
# 提取文本并显示
python pdf_extractor.py input.pdf

# 保存到文件
python pdf_extractor.py input.pdf -o output.txt

# JSON 格式输出
python pdf_extractor.py input.pdf -f json -o output.json

# Markdown 格式输出
python pdf_extractor.py input.pdf -f markdown -o output.md

# 提取关键信息
python pdf_extractor.py input.pdf --extract-key-info

# 完整示例
python pdf_extractor.py input.pdf -f json -o output.json --extract-key-info

# 使用配置文件
python pdf_extractor.py input.pdf --config config.json

# 查看帮助
python pdf_extractor.py --help
```

## 输出格式

### 纯文本格式 (text)

```
文件路径: examples/sample_chinese.pdf
总页数: 3
提取时间: 0.15 秒

========================================
第 1 页
========================================

PDF 文本提取工具示例文档

一、项目简介
...
```

### JSON 格式 (json)

```json
{
  "file_path": "examples/sample_chinese.pdf",
  "page_count": 3,
  "extraction_time": 0.15,
  "pages": [
    {
      "page_number": 0,
      "text": "PDF 文本提取工具示例文档...",
      "char_count": 1234,
      "is_empty": false
    }
  ],
  "total_text": "...",
  "key_info": {
    "headings": ["一、项目简介", "二、主要特性"],
    "keywords": ["PDF", "文本", "提取", "工具"],
    "summary": "这是一个用于演示 PDF 文本提取工具功能的示例文档...",
    "lists": ["• 读取 PDF 文件", "• 提取文本内容"]
  },
  "errors": []
}
```

### Markdown 格式 (markdown)

```markdown
# PDF 提取结果

**文件路径**: examples/sample_chinese.pdf  
**总页数**: 3  
**提取时间**: 0.15 秒

## 关键信息

### 标题和章节
- 一、项目简介
- 二、主要特性

### 关键词
PDF, 文本, 提取, 工具

### 摘要
这是一个用于演示 PDF 文本提取工具功能的示例文档...

## 页面内容

### 第 1 页

PDF 文本提取工具示例文档
...
```

## 常见问题

### 1. 如何处理包含中文路径的文件？

工具自动处理中文路径，无需特殊配置：

```python
result = service.extract(
    file_path="C:/用户/文档/示例.pdf",
    output_format="text"
)
```

### 2. 如何处理大型 PDF 文件？

工具会自动显示进度信息。对于非常大的文件，建议使用逐页处理：

```python
result = service.extract(file_path="large.pdf")
for page in result.pages:
    # 逐页处理
    process_page(page)
```

### 3. 如何处理提取失败的页面？

工具会继续处理其他页面，并在结果中标注失败的页面：

```python
result = service.extract(file_path="input.pdf")

if result.errors:
    print("以下页面提取失败：")
    for error in result.errors:
        print(f"  {error}")

# 成功提取的内容仍然可用
print(result.total_text)
```

### 4. 如何自定义关键信息提取？

使用 `KeyInfoAnalyzer` 类的方法自定义提取参数：

```python
analyzer = KeyInfoAnalyzer()

# 提取更多关键词
keywords = analyzer.extract_keywords(text, top_n=50)

# 生成更长的摘要
summary = analyzer.generate_summary(text, max_length=1000)
```

### 5. 如何批量处理多个文件？

参考 `advanced_usage.py` 中的批量处理示例，或使用 shell 脚本：

```bash
for file in *.pdf; do
    python pdf_extractor.py "$file" -o "${file%.pdf}.txt"
done
```

## 更多资源

- [项目 README](../README.md) - 项目概述和安装说明
- [API 文档](../docs/README.md) - 详细的 API 文档
- [配置说明](../docs/CONFIGURATION.md) - 配置文件说明
- [日志说明](../docs/LOGGING.md) - 日志系统说明

## 贡献

如果您有更好的示例或发现问题，欢迎提交 Issue 或 Pull Request！
