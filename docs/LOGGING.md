# 日志系统文档

PDF 文本提取工具提供了完善的日志系统，支持中文错误消息、多级别日志记录和文件日志功能。

## 日志级别

系统支持以下日志级别（从低到高）：

| 级别 | 说明 | 使用场景 |
|------|------|----------|
| **DEBUG** | 调试信息 | 开发和调试时使用，显示详细的执行信息 |
| **INFO** | 一般信息 | 记录正常的操作流程 |
| **WARNING** | 警告信息 | 记录潜在问题，但不影响程序运行 |
| **ERROR** | 错误信息 | 记录错误，但程序可以继续运行 |
| **CRITICAL** | 严重错误 | 记录严重错误，可能导致程序终止 |

## 配置日志

### 通过命令行参数

```bash
# 详细模式（DEBUG 级别）
pdf-extractor input.pdf -v

# 静默模式（只显示错误）
pdf-extractor input.pdf -q

# 默认模式（WARNING 级别）
pdf-extractor input.pdf
```

### 通过配置文件

在配置文件中设置日志选项：

```json
{
  "log_level": "INFO",
  "log_to_file": true,
  "log_file_path": "~/.pdf_extractor/logs/app.log"
}
```

### 通过环境变量

```bash
# 设置日志级别
export PDF_EXTRACTOR_LOG_LEVEL=DEBUG

# 启用文件日志
export PDF_EXTRACTOR_LOG_TO_FILE=true

# 设置日志文件路径
export PDF_EXTRACTOR_LOG_FILE_PATH=/var/log/pdf_extractor.log
```

## 日志格式

系统支持三种日志格式：

### 1. 简单格式（默认）

```
WARNING: 部分页面提取失败，已提取 8/10 页
ERROR: 找不到文件 'test.pdf'，请检查路径是否正确
```

### 2. 详细格式

```
2024-01-15 10:30:45 - pdf_extractor - WARNING - 部分页面提取失败，已提取 8/10 页
2024-01-15 10:30:46 - pdf_extractor - ERROR - 找不到文件 'test.pdf'，请检查路径是否正确
```

### 3. 调试格式

```
2024-01-15 10:30:45 - pdf_extractor - WARNING - [pdf_extraction_service.py:123] - 部分页面提取失败，已提取 8/10 页
2024-01-15 10:30:46 - pdf_extractor - ERROR - [path_handler.py:45] - 找不到文件 'test.pdf'，请检查路径是否正确
```

## 中文错误消息

系统提供了完整的中文错误消息模板，涵盖所有错误场景：

### 文件相关错误

- **文件不存在**：`错误：找不到文件 '{path}'，请检查路径是否正确`
- **无效的 PDF**：`错误：文件 '{path}' 不是有效的 PDF 文件`
- **权限不足**：`错误：没有权限读取文件 '{path}'`
- **文件被占用**：`错误：文件 '{path}' 被其他程序占用，无法访问`

### 提取相关错误

- **提取失败**：`错误：提取第 {page} 页时失败：{reason}`
- **编码错误**：`错误：文本编码转换失败，可能包含不支持的字符`
- **空 PDF**：`警告：PDF 文件为空，没有可提取的内容`
- **部分提取失败**：`警告：部分页面提取失败，已提取 {success}/{total} 页`

### 路径相关错误

- **无效路径**：`错误：路径 '{path}' 格式不正确`
- **路径过长**：`错误：路径 '{path}' 过长，超过系统限制`

### 输出相关错误

- **保存失败**：`错误：保存文件失败：{path}，原因：{reason}`
- **无效格式**：`错误：不支持的输出格式 '{format}'，支持的格式：text, json, markdown`

### 配置相关错误

- **配置加载失败**：`警告：加载配置文件失败：{path}，使用默认配置`
- **配置保存失败**：`错误：保存配置文件失败：{path}，原因：{reason}`

### 分析相关错误

- **分析失败**：`警告：关键信息分析失败：{reason}，将返回部分结果`
- **关键词提取失败**：`警告：关键词提取失败，跳过此步骤`

## 文件日志

### 启用文件日志

通过配置文件：

```json
{
  "log_to_file": true,
  "log_file_path": "~/.pdf_extractor/logs/app.log"
}
```

或通过环境变量：

```bash
export PDF_EXTRACTOR_LOG_TO_FILE=true
export PDF_EXTRACTOR_LOG_FILE_PATH=/var/log/pdf_extractor.log
```

### 日志文件位置

如果未指定日志文件路径，系统会自动创建：

- **Linux/Mac**：`~/.pdf_extractor/logs/pdf_extractor_YYYYMMDD.log`
- **Windows**：`C:\Users\<用户名>\.pdf_extractor\logs\pdf_extractor_YYYYMMDD.log`

### 日志文件格式

文件日志使用详细格式，包含时间戳、模块名、级别和消息：

```
2024-01-15 10:30:45,123 - pdf_extractor - INFO - 开始处理文件: test.pdf
2024-01-15 10:30:45,234 - pdf_extractor - INFO - PDF 文件已打开，共 10 页
2024-01-15 10:30:46,345 - pdf_extractor - INFO - 文本提取完成，共提取 5432 个字符
2024-01-15 10:30:46,456 - pdf_extractor - WARNING - 第 5 页提取失败：页面损坏
2024-01-15 10:30:47,567 - pdf_extractor - INFO - 提取流程完成
```

### 日志文件管理

- 日志文件按日期命名，每天创建新文件
- 系统不会自动清理旧日志，需要手动管理
- 建议定期清理或使用日志轮转工具

## 使用示例

### 1. 开发调试

启用详细日志并保存到文件：

```bash
pdf-extractor input.pdf -v -c debug_config.json
```

`debug_config.json`：
```json
{
  "log_level": "DEBUG",
  "log_to_file": true,
  "log_file_path": "./debug.log"
}
```

### 2. 生产环境

只记录警告和错误到文件：

```bash
pdf-extractor input.pdf -c production_config.json
```

`production_config.json`：
```json
{
  "log_level": "WARNING",
  "log_to_file": true,
  "log_file_path": "/var/log/pdf_extractor/app.log"
}
```

### 3. 静默批处理

只在出错时显示信息：

```bash
pdf-extractor input.pdf -q
```

### 4. 查看详细错误信息

当出现错误时，使用详细模式查看完整堆栈跟踪：

```bash
pdf-extractor problematic.pdf -v
```

## 编程接口

### 在代码中使用日志

```python
from src.logger import setup_logging, log_error, log_warning, get_logger

# 设置日志系统
logger = setup_logging(level="INFO", log_to_file=True)

# 记录信息
logger.info("开始处理文件")

# 使用中文错误消息模板
log_error(logger, "file_not_found", path="/path/to/file.pdf")
log_warning(logger, "partial_extraction", success=8, total=10)

# 获取日志记录器
logger = get_logger("my_module")
logger.debug("调试信息")
```

### 自定义错误消息

```python
from src.logger import get_error_message

# 获取格式化的错误消息
message = get_error_message("file_not_found", path="/test/file.pdf")
print(message)  # 输出：错误：找不到文件 '/test/file.pdf'，请检查路径是否正确
```

## 最佳实践

### 1. 选择合适的日志级别

- **开发**：使用 DEBUG 级别查看详细信息
- **测试**：使用 INFO 级别记录关键操作
- **生产**：使用 WARNING 级别，只记录问题
- **故障排查**：临时切换到 DEBUG 级别

### 2. 启用文件日志

在生产环境中始终启用文件日志：

```json
{
  "log_to_file": true,
  "log_file_path": "/var/log/pdf_extractor/app.log"
}
```

### 3. 日志文件轮转

使用系统工具管理日志文件大小：

**Linux (logrotate)**：

创建 `/etc/logrotate.d/pdf_extractor`：

```
/var/log/pdf_extractor/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}
```

**Windows (PowerShell 脚本)**：

```powershell
# 删除 7 天前的日志
Get-ChildItem "C:\Users\*\.pdf_extractor\logs\*.log" | 
    Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-7)} | 
    Remove-Item
```

### 4. 监控日志

使用日志监控工具实时查看错误：

```bash
# Linux/Mac
tail -f ~/.pdf_extractor/logs/pdf_extractor_*.log | grep ERROR

# Windows (PowerShell)
Get-Content -Path "$env:USERPROFILE\.pdf_extractor\logs\pdf_extractor_*.log" -Wait | Select-String "ERROR"
```

## 故障排除

### 日志未显示

1. 检查日志级别设置是否正确
2. 确认没有使用 `-q` 静默模式
3. 验证日志配置是否生效

### 日志文件未创建

1. 检查 `log_to_file` 是否设置为 `true`
2. 验证日志文件路径的目录是否存在
3. 确认有写入权限
4. 查看控制台是否有相关警告

### 日志文件过大

1. 实施日志轮转策略
2. 降低日志级别（从 DEBUG 改为 INFO 或 WARNING）
3. 定期清理旧日志文件

### 中文乱码

1. 确认日志文件使用 UTF-8 编码
2. 使用支持 UTF-8 的文本编辑器查看
3. 在 Windows 上，确保控制台支持 UTF-8
