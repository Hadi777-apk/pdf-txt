# PDF 文本提取工具 - 命令行使用指南

## 快速开始

### 基本用法

提取 PDF 文件的文本内容：

```bash
python pdf_extractor.py input.pdf
```

### 保存到文件

将提取的内容保存到文件：

```bash
python pdf_extractor.py input.pdf -o output.txt
```

### 输出格式

支持三种输出格式：

1. **纯文本格式**（默认）：
```bash
python pdf_extractor.py input.pdf -f text
```

2. **JSON 格式**：
```bash
python pdf_extractor.py input.pdf -f json -o output.json
```

3. **Markdown 格式**：
```bash
python pdf_extractor.py input.pdf -f markdown -o output.md
```

### 提取关键信息

提取标题、关键词、摘要和列表：

```bash
python pdf_extractor.py input.pdf --extract-key-info
```

### 显示进度

对于大文件，显示提取进度：

```bash
python pdf_extractor.py large_file.pdf --progress
```

## 完整参数说明

### 必需参数

- `input` - PDF 文件路径（支持相对路径、绝对路径、中文路径）

### 可选参数

- `-o, --output FILE` - 输出文件路径。如果不指定，结果将输出到标准输出
- `-f, --format {text,json,markdown}` - 输出格式（默认: text）
- `--extract-key-info` - 提取关键信息（标题、关键词、摘要、列表）
- `--no-key-info` - 不提取关键信息，仅提取原始文本
- `--progress` - 显示提取进度（对于大文件很有用）
- `-v, --verbose` - 显示详细的日志信息
- `-q, --quiet` - 静默模式，只输出结果或错误信息

## 使用示例

### 示例 1：基本文本提取

```bash
python pdf_extractor.py document.pdf
```

输出：提取的文本内容直接显示在终端

### 示例 2：提取并保存为 JSON

```bash
python pdf_extractor.py document.pdf -o result.json -f json --extract-key-info
```

输出：包含页面信息和关键信息的 JSON 文件

### 示例 3：处理中文路径

```bash
python pdf_extractor.py "C:\用户\文档\测试文件.pdf" -o "输出结果.txt"
```

### 示例 4：大文件处理

```bash
python pdf_extractor.py large_document.pdf --progress -o output.txt
```

输出：显示处理进度，完成后保存到文件

### 示例 5：静默模式

```bash
python pdf_extractor.py input.pdf -q -o output.txt
```

输出：只在出错时显示错误信息

### 示例 6：详细日志

```bash
python pdf_extractor.py input.pdf -v
```

输出：显示详细的处理日志

## 错误处理

工具会自动处理以下错误情况：

- **文件不存在**：显示清晰的错误消息
- **无效的 PDF 文件**：提示文件格式错误
- **权限不足**：提示没有读取权限
- **部分页面提取失败**：继续处理其他页面，并在结果中标注失败的页面

## 输出格式说明

### 纯文本格式

直接输出提取的文本内容，保持原始顺序。

### JSON 格式

```json
{
  "file_path": "document.pdf",
  "page_count": 10,
  "pages": [
    {
      "page_number": 0,
      "text": "第一页的内容...",
      "char_count": 1234,
      "is_empty": false
    }
  ],
  "total_text": "所有页面的文本...",
  "key_info": {
    "headings": ["标题1", "标题2"],
    "keywords": ["关键词1", "关键词2"],
    "summary": "文档摘要...",
    "lists": ["列表项1", "列表项2"]
  },
  "extraction_time": 1.23,
  "errors": []
}
```

### Markdown 格式

以 Markdown 格式输出，包含标题、页面分隔和关键信息。

## 注意事项

1. **中文支持**：工具完全支持中文内容和中文路径
2. **编码**：所有输出使用 UTF-8 编码
3. **大文件**：建议对大文件使用 `--progress` 参数查看进度
4. **关键信息**：关键信息提取功能需要使用 `--extract-key-info` 参数启用

## 获取帮助

查看完整的帮助信息：

```bash
python pdf_extractor.py --help
```
