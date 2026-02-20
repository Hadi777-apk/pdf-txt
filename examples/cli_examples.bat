@echo off
REM CLI 使用示例脚本（Windows 版本）
REM 演示 PDF 文本提取工具的命令行用法

echo ======================================
echo PDF 文本提取工具 - CLI 使用示例
echo ======================================

REM 示例 1：基本用法 - 提取文本并显示在控制台
echo.
echo 示例 1：基本用法 - 提取文本并显示
echo --------------------------------------
echo 命令：python pdf_extractor.py examples\sample_chinese.pdf
python pdf_extractor.py examples\sample_chinese.pdf

REM 示例 2：保存到文件
echo.
echo 示例 2：保存到文件
echo --------------------------------------
echo 命令：python pdf_extractor.py examples\sample_chinese.pdf -o examples\output.txt
python pdf_extractor.py examples\sample_chinese.pdf -o examples\output.txt

REM 示例 3：JSON 格式输出
echo.
echo 示例 3：JSON 格式输出
echo --------------------------------------
echo 命令：python pdf_extractor.py examples\sample_chinese.pdf -f json -o examples\output.json
python pdf_extractor.py examples\sample_chinese.pdf -f json -o examples\output.json

REM 示例 4：Markdown 格式输出
echo.
echo 示例 4：Markdown 格式输出
echo --------------------------------------
echo 命令：python pdf_extractor.py examples\sample_chinese.pdf -f markdown -o examples\output.md
python pdf_extractor.py examples\sample_chinese.pdf -f markdown -o examples\output.md

REM 示例 5：提取关键信息
echo.
echo 示例 5：提取关键信息
echo --------------------------------------
echo 命令：python pdf_extractor.py examples\sample_chinese.pdf --extract-key-info
python pdf_extractor.py examples\sample_chinese.pdf --extract-key-info

REM 示例 6：完整示例 - JSON 格式 + 关键信息
echo.
echo 示例 6：完整示例 - JSON 格式 + 关键信息
echo --------------------------------------
echo 命令：python pdf_extractor.py examples\sample_chinese.pdf -f json -o examples\full_output.json --extract-key-info
python pdf_extractor.py examples\sample_chinese.pdf -f json -o examples\full_output.json --extract-key-info

REM 示例 7：使用配置文件
echo.
echo 示例 7：使用配置文件
echo --------------------------------------
echo 命令：python pdf_extractor.py examples\sample_chinese.pdf --config pdf_extractor_config.json
python pdf_extractor.py examples\sample_chinese.pdf --config pdf_extractor_config.json

REM 示例 8：查看帮助信息
echo.
echo 示例 8：查看帮助信息
echo --------------------------------------
echo 命令：python pdf_extractor.py --help
python pdf_extractor.py --help

echo.
echo ======================================
echo 所有 CLI 示例运行完成！
echo ======================================
pause
