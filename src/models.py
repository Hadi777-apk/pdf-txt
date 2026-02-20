"""核心数据模型类"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PDFDocument:
    """PDF 文档对象"""
    file_path: str
    page_count: int
    metadata: Dict[str, Any] = field(default_factory=dict)
    _internal_handle: Any = None


@dataclass
class PageText:
    """页面文本"""
    page_number: int
    text: str
    char_count: int = 0
    is_empty: bool = False
    
    def __post_init__(self):
        """初始化后自动计算字符数和是否为空"""
        if self.char_count == 0:
            self.char_count = len(self.text)
        if not self.text or self.text.strip() == "":
            self.is_empty = True


@dataclass
class KeyInformation:
    """关键信息"""
    headings: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    summary: str = ""
    lists: List[str] = field(default_factory=list)


@dataclass
class ExtractedContent:
    """提取的内容"""
    file_path: str
    page_count: int
    pages: List[PageText]
    total_text: str = ""
    key_info: Optional[KeyInformation] = None
    extraction_time: float = 0.0
    errors: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """初始化后自动生成总文本"""
        if not self.total_text and self.pages:
            self.total_text = "".join(page.text for page in self.pages)
