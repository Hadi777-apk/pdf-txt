"""PDF 提取服务 - 应用服务层"""

import logging
import time
from typing import Optional

from .models import ExtractedContent, KeyInformation
from .pdf_reader import PDFReader
from .text_extractor import TextExtractor
from .key_info_analyzer import KeyInfoAnalyzer
from .output_formatter import OutputFormatter
from .path_handler import PathHandler
from .exceptions import (
    PDFExtractionError,
    PathError,
    FileNotFoundError,
    InvalidPDFError
)
from .logger import log_error, log_warning

# 配置日志
logger = logging.getLogger(__name__)


class PDFExtractionService:
    """PDF 提取服务
    
    协调整个 PDF 文本提取流程，集成所有核心组件：
    - 路径处理和验证
    - PDF 文件读取
    - 文本内容提取
    - 关键信息分析
    - 输出格式化
    
    提供统一的接口用于执行完整的提取工作流。
    """
    
    def __init__(self):
        """初始化所有组件"""
        self.reader = PDFReader()
        self.extractor = TextExtractor()
        self.analyzer = KeyInfoAnalyzer()
        self.formatter = OutputFormatter()
        self.path_handler = PathHandler()
        
        logger.info("PDFExtractionService 初始化完成")
    
    def extract(
        self,
        file_path: str,
        output_format: str = "text",
        extract_key_info: bool = True,
        output_file: Optional[str] = None,
        show_progress: bool = False
    ) -> str:
        """执行完整的提取流程
        
        工作流程：
        1. 验证和规范化文件路径
        2. 打开 PDF 文件
        3. 提取所有页面的文本内容
        4. （可选）分析关键信息
        5. 格式化输出
        6. （可选）保存到文件
        
        参数:
            file_path: PDF 文件路径（支持相对路径、绝对路径、中文路径）
            output_format: 输出格式，可选值：'text', 'json', 'markdown'，默认 'text'
            extract_key_info: 是否提取关键信息（标题、关键词、摘要等），默认 True
            output_file: 输出文件路径（可选），如果提供则保存到文件
            show_progress: 是否显示进度指示（对于大文件），默认 False
            
        返回:
            格式化的提取结果字符串
            
        异常:
            PathError: 路径格式错误
            PDFFileNotFoundError: 文件不存在
            InvalidPDFError: 文件不是有效的 PDF
            PDFExtractionError: 提取过程中的其他错误
        """
        document = None
        start_time = time.time()
        
        try:
            # 步骤 1: 验证和规范化路径
            logger.info(f"开始处理文件: {file_path}")
            
            try:
                normalized_path = self.path_handler.normalize_path(file_path)
            except PathError as e:
                logger.error(f"路径格式错误: {file_path}")
                raise
            
            # 验证路径是否存在
            if not self.path_handler.validate_path(normalized_path):
                log_error(logger, "file_not_found", path=normalized_path)
                raise FileNotFoundError(normalized_path)
            
            # 验证是否为 PDF 文件
            if not self.path_handler.is_pdf_file(normalized_path):
                log_error(logger, "invalid_pdf", path=normalized_path)
                raise InvalidPDFError(normalized_path)
            
            # 步骤 2: 打开 PDF 文件
            logger.info(f"打开 PDF 文件: {normalized_path}")
            document = self.reader.open(normalized_path)
            logger.info(f"PDF 文件已打开，共 {document.page_count} 页")
            
            # 步骤 3: 提取文本内容
            logger.info("开始提取文本内容...")
            
            if show_progress and document.page_count > 5:
                # 对于大文件，显示进度
                content = self._extract_with_progress(document)
            else:
                content = self.extractor.extract_all_text(document)
            
            logger.info(f"文本提取完成，共提取 {len(content.total_text)} 个字符")
            
            # 记录提取时间
            content.extraction_time = time.time() - start_time
            
            # 步骤 4: 提取关键信息（可选）
            if extract_key_info:
                logger.info("开始分析关键信息...")
                key_info = self._analyze_key_information(content.total_text)
                content.key_info = key_info
                logger.info("关键信息分析完成")
            
            # 步骤 5: 格式化输出
            logger.info(f"格式化输出为 {output_format} 格式...")
            formatted_output = self._format_output(content, output_format)
            
            # 步骤 6: 保存到文件（可选）
            if output_file:
                logger.info(f"保存结果到文件: {output_file}")
                save_message = self.formatter.save_to_file(formatted_output, output_file)
                logger.info(save_message)
            
            logger.info("提取流程完成")
            return formatted_output
            
        except PDFExtractionError:
            # 重新抛出已知的 PDF 提取错误
            raise
        except Exception as e:
            # 捕获未预期的错误
            error_msg = f"提取过程中发生未知错误: {str(e)}"
            logger.exception(error_msg)
            raise PDFExtractionError(error_msg) from e
        finally:
            # 确保关闭 PDF 文件
            if document is not None:
                try:
                    self.reader.close(document)
                    logger.info("PDF 文件已关闭")
                except Exception as e:
                    logger.warning(f"关闭 PDF 文件时发生错误: {str(e)}")
    
    def _extract_with_progress(self, document) -> ExtractedContent:
        """带进度指示的文本提取
        
        对于大文件，显示提取进度
        
        参数:
            document: PDF 文档对象
            
        返回:
            提取的内容对象
        """
        from .models import PageText
        
        pages = []
        errors = []
        total_pages = document.page_count
        
        print(f"\n开始提取 {total_pages} 页内容...")
        
        for page_num in range(total_pages):
            try:
                # 显示进度
                progress = (page_num + 1) / total_pages * 100
                print(f"\r处理进度: {page_num + 1}/{total_pages} ({progress:.1f}%)", end='', flush=True)
                
                # 提取单页文本
                text = self.extractor.extract_text(document, page_num)
                
                # 创建 PageText 对象
                page_text = PageText(
                    page_number=page_num,
                    text=text,
                    char_count=len(text),
                    is_empty=(not text or text.strip() == "")
                )
                pages.append(page_text)
                
            except Exception as e:
                # 记录错误但继续处理
                error_msg = f"第 {page_num + 1} 页提取失败：{str(e)}"
                errors.append(error_msg)
                log_error(logger, "extraction_failed", page=page_num + 1, reason=str(e))
                
                # 添加空页面占位
                pages.append(PageText(
                    page_number=page_num,
                    text="",
                    char_count=0,
                    is_empty=True
                ))
        
        print("\n提取完成！\n")
        
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
    
    def _analyze_key_information(self, text: str) -> KeyInformation:
        """分析关键信息
        
        从文本中提取标题、关键词、摘要和列表
        
        参数:
            text: 要分析的文本内容
            
        返回:
            关键信息对象
        """
        key_info = KeyInformation()
        
        try:
            # 提取标题
            key_info.headings = self.analyzer.extract_headings(text)
            logger.debug(f"提取到 {len(key_info.headings)} 个标题")
            
            # 提取关键词
            key_info.keywords = self.analyzer.extract_keywords(text, top_n=10)
            logger.debug(f"提取到 {len(key_info.keywords)} 个关键词")
            
            # 生成摘要
            key_info.summary = self.analyzer.generate_summary(text, max_length=200)
            logger.debug(f"生成摘要，长度: {len(key_info.summary)} 字符")
            
            # 提取列表
            key_info.lists = self.analyzer.extract_lists(text)
            logger.debug(f"提取到 {len(key_info.lists)} 个列表项")
            
        except Exception as e:
            logger.warning(f"关键信息分析过程中发生错误: {str(e)}")
            log_warning(logger, "analysis_failed", reason=str(e))
            # 即使分析失败，也返回部分结果
        
        return key_info
    
    def _format_output(self, content: ExtractedContent, output_format: str) -> str:
        """格式化输出
        
        根据指定的格式类型格式化提取的内容
        
        参数:
            content: 提取的内容对象
            output_format: 输出格式（'text', 'json', 'markdown'）
            
        返回:
            格式化后的字符串
            
        异常:
            ValueError: 不支持的输出格式
        """
        format_lower = output_format.lower()
        
        if format_lower == 'text':
            return self.formatter.format_as_text(content)
        elif format_lower == 'json':
            return self.formatter.format_as_json(content)
        elif format_lower == 'markdown':
            return self.formatter.format_as_markdown(content)
        else:
            error_msg = f"不支持的输出格式: {output_format}，支持的格式: text, json, markdown"
            log_error(logger, "invalid_format", format=output_format)
            raise ValueError(error_msg)
