#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高级使用示例

演示 PDF 文本提取工具的高级功能和自定义用法。
"""

import sys
import os
import json

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.pdf_reader import PDFReader
from src.text_extractor import TextExtractor
from src.key_info_analyzer import KeyInfoAnalyzer
from src.output_formatter import OutputFormatter
from src.path_handler import PathHandler


def example_1_custom_workflow():
    """示例 1：自定义工作流程"""
    print("=" * 60)
    print("示例 1：自定义工作流程 - 使用独立组件")
    print("=" * 60)
    
    # 步骤 1：验证路径
    path_handler = PathHandler()
    file_path = "examples/sample_chinese.pdf"
    
    normalized_path = path_handler.normalize_path(file_path)
    print(f"\n1. 路径验证")
    print(f"   原始路径：{file_path}")
    print(f"   规范化路径：{normalized_path}")
    print(f"   是否为 PDF：{path_handler.is_pdf_file(normalized_path)}")
    
    # 步骤 2：打开 PDF
    reader = PDFReader()
    document = reader.open(normalized_path)
    print(f"\n2. 打开 PDF")
    print(f"   页数：{reader.get_page_count(document)}")
    print(f"   元数据：{document.metadata}")
    
    # 步骤 3：提取文本
    extractor = TextExtractor()
    extracted_content = extractor.extract_all_text(document)
    print(f"\n3. 提取文本")
    print(f"   总字符数：{len(extracted_content.total_text)}")
    print(f"   提取时间：{extracted_content.extraction_time:.2f} 秒")
    
    # 步骤 4：分析关键信息
    analyzer = KeyInfoAnalyzer()
    key_info = analyzer.analyze(extracted_content.total_text)
    print(f"\n4. 分析关键信息")
    print(f"   标题数量：{len(key_info.headings)}")
    print(f"   关键词数量：{len(key_info.keywords)}")
    print(f"   列表项数量：{len(key_info.lists)}")
    
    # 步骤 5：格式化输出
    formatter = OutputFormatter()
    extracted_content.key_info = key_info
    
    text_output = formatter.format_as_text(extracted_content)
    print(f"\n5. 格式化输出")
    print(f"   文本输出长度：{len(text_output)} 字符")
    
    # 关闭文档
    reader.close(document)
    print(f"\n6. 清理资源完成")


def example_2_batch_processing():
    """示例 2：批量处理多个 PDF 文件"""
    print("\n" + "=" * 60)
    print("示例 2：批量处理多个 PDF 文件")
    print("=" * 60)
    
    from src.pdf_extraction_service import PDFExtractionService
    
    # 假设有多个 PDF 文件
    pdf_files = [
        "examples/sample_chinese.pdf",
        # 可以添加更多文件
    ]
    
    service = PDFExtractionService()
    results = []
    
    for pdf_file in pdf_files:
        try:
            print(f"\n处理文件：{pdf_file}")
            result = service.extract(
                file_path=pdf_file,
                output_format="json",
                extract_key_info=True
            )
            
            results.append({
                "file": pdf_file,
                "success": True,
                "page_count": result.page_count,
                "char_count": len(result.total_text),
                "extraction_time": result.extraction_time
            })
            
            print(f"  ✓ 成功：{result.page_count} 页，{len(result.total_text)} 字符")
            
        except Exception as e:
            results.append({
                "file": pdf_file,
                "success": False,
                "error": str(e)
            })
            print(f"  ✗ 失败：{str(e)}")
    
    # 保存批处理结果
    with open("examples/batch_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n批处理完成！结果已保存到 examples/batch_results.json")


def example_3_custom_key_info_extraction():
    """示例 3：自定义关键信息提取"""
    print("\n" + "=" * 60)
    print("示例 3：自定义关键信息提取")
    print("=" * 60)
    
    from src.pdf_extraction_service import PDFExtractionService
    
    service = PDFExtractionService()
    
    # 提取文本
    result = service.extract(
        file_path="examples/sample_chinese.pdf",
        output_format="text",
        extract_key_info=False
    )
    
    # 使用自定义参数提取关键信息
    analyzer = KeyInfoAnalyzer()
    
    # 提取更多关键词
    keywords = analyzer.extract_keywords(result.total_text, top_n=20)
    print(f"\n关键词（前 20 个）：")
    for i, keyword in enumerate(keywords, 1):
        print(f"  {i}. {keyword}")
    
    # 生成更长的摘要
    summary = analyzer.generate_summary(result.total_text, max_length=500)
    print(f"\n摘要（500 字符）：")
    print(f"  {summary}")
    
    # 提取所有标题
    headings = analyzer.extract_headings(result.total_text)
    print(f"\n所有标题：")
    for heading in headings:
        print(f"  • {heading}")


def example_4_markdown_output():
    """示例 4：Markdown 格式输出"""
    print("\n" + "=" * 60)
    print("示例 4：Markdown 格式输出")
    print("=" * 60)
    
    from src.pdf_extraction_service import PDFExtractionService
    
    service = PDFExtractionService()
    
    # 提取并输出为 Markdown
    result = service.extract(
        file_path="examples/sample_chinese.pdf",
        output_format="markdown",
        extract_key_info=True,
        output_file="examples/output.md"
    )
    
    print(f"\n提取成功并保存为 Markdown 格式！")
    print(f"输出文件：examples/output.md")
    
    # 显示 Markdown 内容预览
    with open("examples/output.md", "r", encoding="utf-8") as f:
        content = f.read()
        print(f"\n内容预览（前 1000 字符）：")
        print(content[:1000])
        print("...")


def example_5_error_recovery():
    """示例 5：错误恢复和部分提取"""
    print("\n" + "=" * 60)
    print("示例 5：错误恢复和部分提取")
    print("=" * 60)
    
    from src.pdf_extraction_service import PDFExtractionService
    
    service = PDFExtractionService()
    
    # 即使某些页面提取失败，也能获取成功的部分
    result = service.extract(
        file_path="examples/sample_chinese.pdf",
        output_format="text",
        extract_key_info=False
    )
    
    print(f"\n提取结果：")
    print(f"  总页数：{result.page_count}")
    print(f"  成功提取的页数：{len([p for p in result.pages if not p.is_empty])}")
    print(f"  空页面数：{len([p for p in result.pages if p.is_empty])}")
    
    if result.errors:
        print(f"\n错误列表：")
        for error in result.errors:
            print(f"  • {error}")
    else:
        print(f"\n没有错误，所有页面提取成功！")


def example_6_path_handling():
    """示例 6：路径处理示例"""
    print("\n" + "=" * 60)
    print("示例 6：路径处理示例")
    print("=" * 60)
    
    path_handler = PathHandler()
    
    # 测试各种路径格式
    test_paths = [
        "examples/sample_chinese.pdf",
        "./examples/sample_chinese.pdf",
        "examples\\sample_chinese.pdf",
        os.path.abspath("examples/sample_chinese.pdf"),
    ]
    
    print(f"\n路径规范化测试：")
    for path in test_paths:
        normalized = path_handler.normalize_path(path)
        is_valid = path_handler.validate_path(normalized)
        is_pdf = path_handler.is_pdf_file(normalized)
        
        print(f"\n  原始路径：{path}")
        print(f"  规范化：{normalized}")
        print(f"  有效性：{is_valid}")
        print(f"  是 PDF：{is_pdf}")


if __name__ == "__main__":
    # 运行所有高级示例
    try:
        example_1_custom_workflow()
        example_2_batch_processing()
        example_3_custom_key_info_extraction()
        example_4_markdown_output()
        example_5_error_recovery()
        example_6_path_handling()
        
        print("\n" + "=" * 60)
        print("所有高级示例运行完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n运行示例时出错：{e}")
        import traceback
        traceback.print_exc()
