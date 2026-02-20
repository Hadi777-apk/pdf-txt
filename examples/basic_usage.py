#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基本使用示例

演示 PDF 文本提取工具的基本功能。
"""

import sys
import os

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.pdf_extraction_service import PDFExtractionService


def example_1_basic_extraction():
    """示例 1：基本文本提取"""
    print("=" * 60)
    print("示例 1：基本文本提取")
    print("=" * 60)
    
    service = PDFExtractionService()
    
    # 提取 PDF 文本
    result = service.extract(
        file_path="examples/sample_chinese.pdf",
        output_format="text",
        extract_key_info=False
    )
    
    print(f"\n提取成功！")
    print(f"文件路径：{result.file_path}")
    print(f"总页数：{result.page_count}")
    print(f"提取时间：{result.extraction_time:.2f} 秒")
    print(f"\n前 500 个字符：")
    print(result.total_text[:500])
    print("...")


def example_2_save_to_file():
    """示例 2：保存到文件"""
    print("\n" + "=" * 60)
    print("示例 2：保存提取结果到文件")
    print("=" * 60)
    
    service = PDFExtractionService()
    
    # 提取并保存到文件
    result = service.extract(
        file_path="examples/sample_chinese.pdf",
        output_format="text",
        extract_key_info=False,
        output_file="examples/output.txt"
    )
    
    print(f"\n提取成功并保存到文件！")
    print(f"输出文件：examples/output.txt")
    print(f"文件大小：{len(result.total_text)} 字符")


def example_3_json_output():
    """示例 3：JSON 格式输出"""
    print("\n" + "=" * 60)
    print("示例 3：JSON 格式输出")
    print("=" * 60)
    
    service = PDFExtractionService()
    
    # 提取并输出为 JSON
    result = service.extract(
        file_path="examples/sample_chinese.pdf",
        output_format="json",
        extract_key_info=False,
        output_file="examples/output.json"
    )
    
    print(f"\n提取成功并保存为 JSON 格式！")
    print(f"输出文件：examples/output.json")
    print(f"包含 {result.page_count} 个页面的详细信息")


def example_4_extract_key_info():
    """示例 4：提取关键信息"""
    print("\n" + "=" * 60)
    print("示例 4：提取关键信息")
    print("=" * 60)
    
    service = PDFExtractionService()
    
    # 提取文本和关键信息
    result = service.extract(
        file_path="examples/sample_chinese.pdf",
        output_format="text",
        extract_key_info=True
    )
    
    print(f"\n提取成功！")
    
    if result.key_info:
        print(f"\n标题和章节：")
        for heading in result.key_info.headings[:5]:
            print(f"  • {heading}")
        
        print(f"\n关键词（前 10 个）：")
        for keyword in result.key_info.keywords[:10]:
            print(f"  • {keyword}")
        
        print(f"\n摘要：")
        print(f"  {result.key_info.summary}")
        
        if result.key_info.lists:
            print(f"\n列表项（前 5 个）：")
            for item in result.key_info.lists[:5]:
                print(f"  • {item}")


def example_5_error_handling():
    """示例 5：错误处理"""
    print("\n" + "=" * 60)
    print("示例 5：错误处理")
    print("=" * 60)
    
    service = PDFExtractionService()
    
    # 尝试打开不存在的文件
    try:
        result = service.extract(
            file_path="nonexistent.pdf",
            output_format="text"
        )
    except Exception as e:
        print(f"\n捕获到错误：{type(e).__name__}")
        print(f"错误消息：{str(e)}")
    
    # 尝试打开非 PDF 文件
    try:
        result = service.extract(
            file_path="README.md",
            output_format="text"
        )
    except Exception as e:
        print(f"\n捕获到错误：{type(e).__name__}")
        print(f"错误消息：{str(e)}")


def example_6_page_by_page():
    """示例 6：逐页处理"""
    print("\n" + "=" * 60)
    print("示例 6：逐页处理")
    print("=" * 60)
    
    service = PDFExtractionService()
    
    # 提取文本
    result = service.extract(
        file_path="examples/sample_chinese.pdf",
        output_format="text",
        extract_key_info=False
    )
    
    print(f"\n逐页显示内容：")
    for page in result.pages:
        print(f"\n--- 第 {page.page_number + 1} 页 ---")
        print(f"字符数：{page.char_count}")
        if page.is_empty:
            print("（空页面）")
        else:
            print(f"内容预览：{page.text[:200]}...")


if __name__ == "__main__":
    # 运行所有示例
    try:
        example_1_basic_extraction()
        example_2_save_to_file()
        example_3_json_output()
        example_4_extract_key_info()
        example_5_error_handling()
        example_6_page_by_page()
        
        print("\n" + "=" * 60)
        print("所有示例运行完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n运行示例时出错：{e}")
        import traceback
        traceback.print_exc()
