"""PDF 文本提取工具"""

__version__ = "0.1.0"

from .pdf_extraction_service import PDFExtractionService
from .models import PDFDocument, PageText, ExtractedContent, KeyInformation
from .exceptions import (
    PDFExtractionError,
    FileNotFoundError,
    InvalidPDFError,
    PermissionError,
    ExtractionError,
    PageExtractionError,
    EncodingError,
    PathError
)

__all__ = [
    'PDFExtractionService',
    'PDFDocument',
    'PageText',
    'ExtractedContent',
    'KeyInformation',
    'PDFExtractionError',
    'FileNotFoundError',
    'InvalidPDFError',
    'PermissionError',
    'ExtractionError',
    'PageExtractionError',
    'EncodingError',
    'PathError',
]
