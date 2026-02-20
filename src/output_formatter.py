"""输出格式化器模块"""

import json
from typing import Optional
from src.models import ExtractedContent


class OutputFormatter:
    """输出格式化器
    
    负责将提取的内容格式化为不同的输出格式（文本、JSON、Markdown）
    并支持保存到文件。
    """
    
    def format_as_text(self, content: ExtractedContent) -> str:
        """格式化为纯文本
        
        参数:
            content: 提取的内容对象
            
        返回:
            纯文本格式的字符串
        """
        lines = []
        
        # 添加文件信息
        lines.append(f"文件路径: {content.file_path}")
        lines.append(f"总页数: {content.page_count}")
        lines.append("-" * 50)
        lines.append("")
        
        # 添加每页内容
        for page in content.pages:
            lines.append(f"=== 第 {page.page_number + 1} 页 ===")
            if page.is_empty:
                lines.append("(空页面)")
            else:
                lines.append(page.text)
            lines.append("")
        
        # 添加关键信息（如果有）
        if content.key_info:
            lines.append("=" * 50)
            lines.append("关键信息")
            lines.append("=" * 50)
            lines.append("")
            
            if content.key_info.headings:
                lines.append("标题:")
                for heading in content.key_info.headings:
                    lines.append(f"  - {heading}")
                lines.append("")
            
            if content.key_info.keywords:
                lines.append("关键词:")
                lines.append(f"  {', '.join(content.key_info.keywords)}")
                lines.append("")
            
            if content.key_info.summary:
                lines.append("摘要:")
                lines.append(f"  {content.key_info.summary}")
                lines.append("")
            
            if content.key_info.lists:
                lines.append("列表项:")
                for list_item in content.key_info.lists:
                    lines.append(f"  {list_item}")
                lines.append("")
        
        # 添加错误信息（如果有）
        if content.errors:
            lines.append("=" * 50)
            lines.append("错误信息")
            lines.append("=" * 50)
            for error in content.errors:
                lines.append(f"  - {error}")
            lines.append("")
        
        return "\n".join(lines)
    
    def format_as_json(self, content: ExtractedContent) -> str:
        """格式化为 JSON
        
        参数:
            content: 提取的内容对象
            
        返回:
            JSON 格式的字符串，包含页码信息
        """
        data = {
            "file_path": content.file_path,
            "page_count": content.page_count,
            "pages": [
                {
                    "page_number": page.page_number + 1,  # 转换为 1-based
                    "text": page.text,
                    "char_count": page.char_count,
                    "is_empty": page.is_empty
                }
                for page in content.pages
            ],
            "total_text": content.total_text,
            "extraction_time": content.extraction_time
        }
        
        # 添加关键信息（如果有）
        if content.key_info:
            data["key_info"] = {
                "headings": content.key_info.headings,
                "keywords": content.key_info.keywords,
                "summary": content.key_info.summary,
                "lists": content.key_info.lists
            }
        
        # 添加错误信息（如果有）
        if content.errors:
            data["errors"] = content.errors
        
        return json.dumps(data, ensure_ascii=False, indent=2)
    
    def format_as_markdown(self, content: ExtractedContent) -> str:
        """格式化为 Markdown
        
        参数:
            content: 提取的内容对象
            
        返回:
            Markdown 格式的字符串
        """
        lines = []
        
        # 添加文件信息
        lines.append(f"# PDF 文本提取结果")
        lines.append("")
        lines.append(f"**文件路径:** {content.file_path}")
        lines.append(f"**总页数:** {content.page_count}")
        lines.append("")
        lines.append("---")
        lines.append("")
        
        # 添加每页内容
        for page in content.pages:
            lines.append(f"## 第 {page.page_number + 1} 页")
            lines.append("")
            if page.is_empty:
                lines.append("*(空页面)*")
            else:
                lines.append(page.text)
            lines.append("")
        
        # 添加关键信息（如果有）
        if content.key_info:
            lines.append("---")
            lines.append("")
            lines.append("## 关键信息")
            lines.append("")
            
            if content.key_info.headings:
                lines.append("### 标题")
                lines.append("")
                for heading in content.key_info.headings:
                    lines.append(f"- {heading}")
                lines.append("")
            
            if content.key_info.keywords:
                lines.append("### 关键词")
                lines.append("")
                lines.append(", ".join(content.key_info.keywords))
                lines.append("")
            
            if content.key_info.summary:
                lines.append("### 摘要")
                lines.append("")
                lines.append(content.key_info.summary)
                lines.append("")
            
            if content.key_info.lists:
                lines.append("### 列表项")
                lines.append("")
                for list_item in content.key_info.lists:
                    lines.append(f"- {list_item}")
                lines.append("")
        
        # 添加错误信息（如果有）
        if content.errors:
            lines.append("---")
            lines.append("")
            lines.append("## 错误信息")
            lines.append("")
            for error in content.errors:
                lines.append(f"- {error}")
            lines.append("")
        
        return "\n".join(lines)
    
    def save_to_file(self, content: str, output_path: str) -> str:
        """将内容保存到文件
        
        参数:
            content: 要保存的文本内容
            output_path: 输出文件路径
            
        返回:
            成功消息，包含输出文件路径
            
        异常:
            IOError: 文件写入失败
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"文件保存成功: {output_path}"
        except Exception as e:
            raise IOError(f"文件保存失败: {str(e)}")
