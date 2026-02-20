"""自定义异常类"""


class PDFExtractionError(Exception):
    """PDF 提取错误基类"""
    pass


class FileNotFoundError(PDFExtractionError):
    """文件不存在"""
    
    def __init__(self, path: str):
        self.path = path
        super().__init__(f"错误：找不到文件 '{path}'，请检查路径是否正确")


class InvalidPDFError(PDFExtractionError):
    """无效的 PDF 文件"""
    
    def __init__(self, path: str):
        self.path = path
        super().__init__(f"错误：文件 '{path}' 不是有效的 PDF 文件")


class PermissionError(PDFExtractionError):
    """权限不足"""
    
    def __init__(self, path: str):
        self.path = path
        super().__init__(f"错误：没有权限读取文件 '{path}'")


class ExtractionError(PDFExtractionError):
    """文本提取失败"""
    pass


class PageExtractionError(ExtractionError):
    """单页提取失败"""
    
    def __init__(self, page: int, reason: str):
        self.page = page
        self.reason = reason
        super().__init__(f"错误：提取第 {page} 页时失败：{reason}")


class EncodingError(ExtractionError):
    """编码错误"""
    
    def __init__(self):
        super().__init__("错误：文本编码转换失败，可能包含不支持的字符")


class PathError(PDFExtractionError):
    """路径错误"""
    
    def __init__(self, path: str):
        self.path = path
        super().__init__(f"错误：路径 '{path}' 格式不正确")
