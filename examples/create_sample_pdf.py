#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建示例 PDF 文件

此脚本创建包含中文内容的示例 PDF 文件，用于演示 PDF 文本提取工具的功能。
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch
import os


def create_sample_pdf():
    """创建包含中文内容的示例 PDF 文件"""
    
    # 创建 examples 目录（如果不存在）
    os.makedirs("examples", exist_ok=True)
    
    # 创建 PDF 文件
    pdf_path = "examples/sample_chinese.pdf"
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4
    
    # 注册中文字体（使用系统字体）
    try:
        # Windows 系统
        pdfmetrics.registerFont(TTFont('SimSun', 'C:/Windows/Fonts/simsun.ttc'))
        font_name = 'SimSun'
    except:
        try:
            # Linux 系统
            pdfmetrics.registerFont(TTFont('SimSun', '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'))
            font_name = 'SimSun'
        except:
            # 如果找不到中文字体，使用默认字体
            font_name = 'Helvetica'
            print("警告：未找到中文字体，使用默认字体")
    
    # 第一页：标题和介绍
    c.setFont(font_name, 24)
    c.drawString(100, height - 100, "PDF 文本提取工具示例文档")
    
    c.setFont(font_name, 12)
    y = height - 150
    
    content_page1 = [
        "一、项目简介",
        "",
        "这是一个用于演示 PDF 文本提取工具功能的示例文档。",
        "本工具支持以下功能：",
        "",
        "• 读取 PDF 文件",
        "• 提取文本内容",
        "• 支持中文内容",
        "• 识别关键信息",
        "• 多种输出格式",
        "",
        "二、主要特性",
        "",
        "1. 中文支持：完整支持简体中文、繁体中文和中英文混合内容",
        "2. 路径处理：支持 Windows 路径、相对路径、包含中文和空格的路径",
        "3. 错误处理：提供清晰的中文错误消息和详细的日志记录",
        "4. 输出格式：支持纯文本、JSON 和 Markdown 格式输出",
    ]
    
    for line in content_page1:
        c.drawString(100, y, line)
        y -= 20
        if y < 100:
            break
    
    # 第二页：技术细节
    c.showPage()
    c.setFont(font_name, 16)
    c.drawString(100, height - 100, "三、技术架构")
    
    c.setFont(font_name, 12)
    y = height - 150
    
    content_page2 = [
        "核心组件：",
        "",
        "1. PDFReader - PDF 文件读取器",
        "   负责打开和读取 PDF 文件，处理各种文件格式和编码",
        "",
        "2. TextExtractor - 文本提取器",
        "   从 PDF 页面中提取文本内容，保持原始顺序和结构",
        "",
        "3. KeyInfoAnalyzer - 关键信息分析器",
        "   识别标题、关键词、摘要和列表结构",
        "",
        "4. OutputFormatter - 输出格式化器",
        "   将提取的内容格式化为不同的输出格式",
        "",
        "5. PathHandler - 路径处理器",
        "   处理和验证文件路径，支持多种路径格式",
    ]
    
    for line in content_page2:
        c.drawString(100, y, line)
        y -= 20
        if y < 100:
            break
    
    # 第三页：使用示例
    c.showPage()
    c.setFont(font_name, 16)
    c.drawString(100, height - 100, "四、使用示例")
    
    c.setFont(font_name, 12)
    y = height - 150
    
    content_page3 = [
        "基本用法：",
        "",
        "python pdf_extractor.py input.pdf",
        "",
        "指定输出文件：",
        "",
        "python pdf_extractor.py input.pdf -o output.txt",
        "",
        "JSON 格式输出：",
        "",
        "python pdf_extractor.py input.pdf -f json -o output.json",
        "",
        "提取关键信息：",
        "",
        "python pdf_extractor.py input.pdf --extract-key-info",
        "",
        "完整示例：",
        "",
        "python pdf_extractor.py sample.pdf -f json -o result.json --extract-key-info",
    ]
    
    for line in content_page3:
        c.drawString(100, y, line)
        y -= 20
        if y < 100:
            break
    
    # 保存 PDF
    c.save()
    print(f"示例 PDF 文件已创建：{pdf_path}")
    return pdf_path


if __name__ == "__main__":
    create_sample_pdf()
