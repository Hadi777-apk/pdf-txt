# 配置管理文档

PDF 文本提取工具支持灵活的配置管理，允许用户通过配置文件或环境变量自定义应用程序行为。

## 配置方式

配置优先级（从高到低）：
1. **环境变量** - 最高优先级
2. **配置文件** - 中等优先级
3. **默认值** - 最低优先级

## 配置文件

### 配置文件位置

系统会按以下顺序查找配置文件：

1. 命令行指定的配置文件（使用 `-c` 或 `--config` 参数）
2. 用户配置目录：`~/.pdf_extractor/config.json`
3. 当前工作目录：`./pdf_extractor_config.json`

### 配置文件格式

配置文件使用 JSON 格式，示例：

```json
{
  "extract_key_info": true,
  "max_keywords": 10,
  "summary_max_length": 200,
  "default_output_format": "text",
  "output_encoding": "utf-8",
  "show_progress_threshold": 5,
  "log_level": "WARNING",
  "log_to_file": false,
  "log_file_path": "pdf_extractor.log"
}
```

### 配置项说明

#### 关键信息提取配置

- **extract_key_info** (布尔值，默认: `true`)
  - 是否默认提取关键信息（标题、关键词、摘要等）
  - 可以通过命令行参数 `--extract-key-info` 或 `--no-key-info` 覆盖

- **max_keywords** (整数，默认: `10`)
  - 提取的最大关键词数量
  - 范围：1-100

- **summary_max_length** (整数，默认: `200`)
  - 生成摘要的最大字符数
  - 范围：50-1000

#### 输出配置

- **default_output_format** (字符串，默认: `"text"`)
  - 默认输出格式
  - 可选值：`"text"`, `"json"`, `"markdown"`

- **output_encoding** (字符串，默认: `"utf-8"`)
  - 输出文件编码
  - 推荐使用 UTF-8 以确保中文正确显示

#### 性能配置

- **show_progress_threshold** (整数，默认: `5`)
  - 当 PDF 页数超过此值时自动显示进度
  - 设置为 0 表示总是显示进度

#### 日志配置

- **log_level** (字符串，默认: `"WARNING"`)
  - 日志级别
  - 可选值：`"DEBUG"`, `"INFO"`, `"WARNING"`, `"ERROR"`, `"CRITICAL"`

- **log_to_file** (布尔值，默认: `false`)
  - 是否将日志记录到文件
  - 启用后会在用户目录创建日志文件

- **log_file_path** (字符串，默认: `"pdf_extractor.log"`)
  - 日志文件路径
  - 如果不是绝对路径，将保存在 `~/.pdf_extractor/logs/` 目录

## 环境变量

所有配置项都可以通过环境变量设置，格式为 `PDF_EXTRACTOR_<配置项名称大写>`。

### 环境变量示例

```bash
# Linux/Mac
export PDF_EXTRACTOR_EXTRACT_KEY_INFO=true
export PDF_EXTRACTOR_MAX_KEYWORDS=20
export PDF_EXTRACTOR_LOG_LEVEL=DEBUG
export PDF_EXTRACTOR_LOG_TO_FILE=true

# Windows (PowerShell)
$env:PDF_EXTRACTOR_EXTRACT_KEY_INFO="true"
$env:PDF_EXTRACTOR_MAX_KEYWORDS="20"
$env:PDF_EXTRACTOR_LOG_LEVEL="DEBUG"
$env:PDF_EXTRACTOR_LOG_TO_FILE="true"

# Windows (CMD)
set PDF_EXTRACTOR_EXTRACT_KEY_INFO=true
set PDF_EXTRACTOR_MAX_KEYWORDS=20
set PDF_EXTRACTOR_LOG_LEVEL=DEBUG
set PDF_EXTRACTOR_LOG_TO_FILE=true
```

### 环境变量列表

| 环境变量 | 配置项 | 类型 |
|---------|--------|------|
| `PDF_EXTRACTOR_EXTRACT_KEY_INFO` | extract_key_info | 布尔值 (true/false) |
| `PDF_EXTRACTOR_MAX_KEYWORDS` | max_keywords | 整数 |
| `PDF_EXTRACTOR_SUMMARY_MAX_LENGTH` | summary_max_length | 整数 |
| `PDF_EXTRACTOR_DEFAULT_OUTPUT_FORMAT` | default_output_format | 字符串 |
| `PDF_EXTRACTOR_OUTPUT_ENCODING` | output_encoding | 字符串 |
| `PDF_EXTRACTOR_SHOW_PROGRESS_THRESHOLD` | show_progress_threshold | 整数 |
| `PDF_EXTRACTOR_LOG_LEVEL` | log_level | 字符串 |
| `PDF_EXTRACTOR_LOG_TO_FILE` | log_to_file | 布尔值 (true/false) |
| `PDF_EXTRACTOR_LOG_FILE_PATH` | log_file_path | 字符串 |

## 使用示例

### 1. 使用配置文件

创建配置文件 `my_config.json`：

```json
{
  "extract_key_info": true,
  "max_keywords": 15,
  "log_level": "INFO",
  "log_to_file": true
}
```

使用配置文件运行：

```bash
pdf-extractor input.pdf -c my_config.json
```

### 2. 使用环境变量

```bash
# 设置环境变量
export PDF_EXTRACTOR_MAX_KEYWORDS=20
export PDF_EXTRACTOR_LOG_LEVEL=DEBUG

# 运行程序
pdf-extractor input.pdf
```

### 3. 混合使用

环境变量会覆盖配置文件中的设置：

```bash
# 使用配置文件，但通过环境变量覆盖日志级别
export PDF_EXTRACTOR_LOG_LEVEL=DEBUG
pdf-extractor input.pdf -c my_config.json
```

### 4. 命令行参数优先

命令行参数具有最高优先级：

```bash
# 即使配置文件设置了 extract_key_info=true，
# 命令行参数 --no-key-info 也会覆盖它
pdf-extractor input.pdf -c my_config.json --no-key-info
```

## 配置最佳实践

1. **开发环境**：使用详细日志级别
   ```json
   {
     "log_level": "DEBUG",
     "log_to_file": true
   }
   ```

2. **生产环境**：使用警告级别，启用文件日志
   ```json
   {
     "log_level": "WARNING",
     "log_to_file": true,
     "log_file_path": "/var/log/pdf_extractor.log"
   }
   ```

3. **批处理**：禁用关键信息提取以提高速度
   ```json
   {
     "extract_key_info": false,
     "show_progress_threshold": 10
   }
   ```

4. **交互使用**：启用进度显示
   ```json
   {
     "show_progress_threshold": 3
   }
   ```

## 故障排除

### 配置文件未生效

1. 检查配置文件路径是否正确
2. 验证 JSON 格式是否有效（使用 JSON 验证工具）
3. 检查文件编码是否为 UTF-8

### 环境变量未生效

1. 确认环境变量名称正确（必须以 `PDF_EXTRACTOR_` 开头）
2. 检查环境变量值的格式（布尔值使用 "true"/"false"）
3. 在 Windows 上，确保使用正确的 shell（PowerShell 或 CMD）

### 日志文件未创建

1. 确认 `log_to_file` 设置为 `true`
2. 检查日志文件路径的目录是否存在且有写入权限
3. 查看控制台是否有相关警告消息
