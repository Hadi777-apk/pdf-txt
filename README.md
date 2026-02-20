# PDF 文本提取工具

一个用于读取 PDF 文件并提取其中文本内容的 Python 应用程序。该工具支持中文内容处理，能够从指定路径读取 PDF 文件，并提取核心知识点和关键信息。

## 功能特性

- ✅ 读取 PDF 文件（支持 Windows 路径格式）
- ✅ 提取文本内容（保持原始顺序和结构）
- ✅ 中文内容支持（简体、繁体、中英文混合）
- ✅ 关键信息提取（标题、关键词、摘要、列表）
- ✅ 多种输出格式（纯文本、JSON、Markdown）
- ✅ 错误处理和用户反馈（中文错误消息）
- ✅ 文件保存（UTF-8 编码）

## 项目结构

```
pdf-text-extractor/
├── src/                    # 源代码
│   ├── __init__.py
│   ├── models.py          # 核心数据模型
│   ├── exceptions.py      # 自定义异常
│   ├── pdf_reader.py      # PDF 读取器
│   ├── text_extractor.py  # 文本提取器
│   ├── key_info_analyzer.py  # 关键信息分析器
│   ├── output_formatter.py   # 输出格式化器
│   ├── path_handler.py    # 路径处理器
│   ├── service.py         # 应用服务层
│   └── cli.py             # 命令行接口
├── tests/                 # 测试代码
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_pdf_reader.py
│   ├── test_text_extractor.py
│   └── ...
├── docs/                  # 文档
│   └── README.md
├── requirements.txt       # 依赖列表
├── pyproject.toml        # 项目配置
└── README.md             # 项目说明

```

## 安装

### 1. 创建虚拟环境

```bash
python -m venv venv
```

### 2. 激活虚拟环境

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

或者使用开发模式安装（包含测试工具）：

```bash
pip install -e ".[dev]"
```

## 使用示例

（待实现）

## 开发

### 运行测试

```bash
pytest
```

### 运行测试并查看覆盖率

```bash
pytest --cov=src --cov-report=html
```

### 运行属性测试

```bash
pytest -v tests/test_properties.py
```

## 技术栈

- **Python 3.8+**
- **pdfplumber**: PDF 处理库
- **jieba**: 中文分词
- **pytest**: 测试框架
- **hypothesis**: 基于属性的测试

## 许可证

MIT License

## 作者

hardy
