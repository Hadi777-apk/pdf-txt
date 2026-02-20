"""文本内容提取器"""

import logging
from typing import List

from .models import PDFDocument, PageText, ExtractedContent
from .exceptions import PageExtractionError

# 配置日志
logger = logging.getLogger(__name__)


class TextExtractor:
    """文本内容提取器
    
    负责从 PDF 文档中提取文本内容，支持单页提取和全文提取。
    提供错误恢复机制，确保部分页面失败不影响整体提取。
    """
    
    def extract_text(self, document: PDFDocument, page_number: int) -> str:
        """
        从指定页面提取文本
        
        参数:
            document: PDF 文档对象
            page_number: 页码（从 0 开始）
            
        返回:
            提取的文本内容（UTF-8 编码）
            
        异常:
            PageExtractionError: 提取失败
        """
        try:
            # 验证页码范围
            if page_number < 0 or page_number >= document.page_count:
                raise PageExtractionError(
                    page_number + 1,
                    f"页码超出范围（总页数：{document.page_count}）"
                )
            
            # 获取页面对象
            pdf_handle = document._internal_handle
            if pdf_handle is None:
                raise PageExtractionError(
                    page_number + 1,
                    "PDF 文档未正确打开"
                )
            
            page = pdf_handle.pages[page_number]
            
            # 提取文本
            text = page.extract_text()
            
            # 处理空页面
            if text is None:
                return ""
            
            # 确保 UTF-8 编码处理正确
            # pdfplumber 返回的是 Unicode 字符串，确保可以正确编码为 UTF-8
            try:
                # 验证可以编码为 UTF-8
                text.encode('utf-8')
                return text
            except UnicodeEncodeError as e:
                # 如果编码失败，尝试替换无法编码的字符
                logger.warning(f"第 {page_number + 1} 页包含无法编码为 UTF-8 的字符，将进行替换")
                return text.encode('utf-8', errors='replace').decode('utf-8')
                
        except PageExtractionError:
            # 重新抛出已知的提取错误
            raise
        except Exception as e:
            # 捕获其他未预期的错误
            logger.error(f"提取第 {page_number + 1} 页时发生错误: {str(e)}")
            raise PageExtractionError(page_number + 1, str(e))
    
    def extract_all_text(self, document: PDFDocument) -> ExtractedContent:
        """
        提取所有页面的文本
        
        使用错误恢复机制：如果某页提取失败，记录错误并继续处理其他页面。
        
        参数:
            document: PDF 文档对象
            
        返回:
            包含所有页面文本的 ExtractedContent 对象
        """
        pages: List[PageText] = []
        errors: List[str] = []
        
        # 遍历所有页面
        for page_num in range(document.page_count):
            try:
                # 提取单页文本
                text = self.extract_text(document, page_num)
                
                # 创建 PageText 对象
                page_text = PageText(
                    page_number=page_num,
                    text=text,
                    char_count=len(text),
                    is_empty=(not text or text.strip() == "")
                )
                pages.append(page_text)
                
            except PageExtractionError as e:
                # 记录错误但继续处理
                error_msg = f"第 {page_num + 1} 页提取失败：{e.reason}"
                errors.append(error_msg)
                logger.error(error_msg)
                
                # 添加空页面占位
                pages.append(PageText(
                    page_number=page_num,
                    text="",
                    char_count=0,
                    is_empty=True
                ))
                
            except Exception as e:
                # 捕获未预期的错误
                error_msg = f"第 {page_num + 1} 页发生未知错误：{str(e)}"
                errors.append(error_msg)
                logger.exception(error_msg)
                
                # 添加空页面占位
                pages.append(PageText(
                    page_number=page_num,
                    text="",
                    char_count=0,
                    is_empty=True
                ))
        
        # 合并所有页面的文本
        total_text = "".join(page.text for page in pages)
        
        # 创建 ExtractedContent 对象
        content = ExtractedContent(
            file_path=document.file_path,
            page_count=document.page_count,
            pages=pages,
            total_text=total_text,
            errors=errors
        )
        
        return content
