"""PDF 文件读取器"""

import os
import pdfplumber
from typing import Optional

from .models import PDFDocument
from .exceptions import (
    FileNotFoundError as PDFFileNotFoundError,
    InvalidPDFError,
    PermissionError as PDFPermissionError
)


class PDFReader:
    """PDF 文件读取器
    
    负责打开和读取 PDF 文件，处理各种错误情况。
    """
    
    def open(self, file_path: str) -> PDFDocument:
        """
        打开 PDF 文件
        
        参数:
            file_path: PDF 文件的完整路径
            
        返回:
            PDFDocument 对象
            
        异常:
            PDFFileNotFoundError: 文件不存在
            InvalidPDFError: 文件不是有效的 PDF
            PDFPermissionError: 没有读取权限
        """
        # 检查文件是否存在
        if not os.path.exists(file_path):
            raise PDFFileNotFoundError(file_path)
        
        # 检查是否有读取权限
        if not os.access(file_path, os.R_OK):
            raise PDFPermissionError(file_path)
        
        try:
            # 使用 pdfplumber 打开 PDF 文件
            pdf_handle = pdfplumber.open(file_path)
            
            # 获取页数
            page_count = len(pdf_handle.pages)
            
            # 提取元数据
            metadata = pdf_handle.metadata or {}
            
            # 创建 PDFDocument 对象
            document = PDFDocument(
                file_path=file_path,
                page_count=page_count,
                metadata=metadata,
                _internal_handle=pdf_handle
            )
            
            return document
            
        except Exception as e:
            # 如果打开失败，可能是无效的 PDF 文件
            error_msg = str(e).lower()
            if 'pdf' in error_msg or 'format' in error_msg or 'invalid' in error_msg:
                raise InvalidPDFError(file_path)
            # 其他未知错误也视为无效 PDF
            raise InvalidPDFError(file_path)
    
    def get_page_count(self, document: PDFDocument) -> int:
        """
        获取 PDF 页数
        
        参数:
            document: PDF 文档对象
            
        返回:
            页数
        """
        return document.page_count
    
    def close(self, document: PDFDocument) -> None:
        """
        关闭 PDF 文件
        
        参数:
            document: PDF 文档对象
        """
        if document._internal_handle is not None:
            document._internal_handle.close()
            document._internal_handle = None
