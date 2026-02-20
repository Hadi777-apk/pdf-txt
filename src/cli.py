"""命令行接口模块

提供用户友好的命令行界面，用于 PDF 文本提取工具。
支持多种输出格式和配置选项。
"""

import argparse
import sys
import logging
from pathlib import Path

from .pdf_extraction_service import PDFExtractionService
from .exceptions import PDFExtractionError
from .config import get_config_manager
from .logger import setup_logging as setup_logger_system


def create_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器
    
    返回:
        配置好的 ArgumentParser 对象
    """
    parser = argparse.ArgumentParser(
        prog='pdf-extractor',
        description='PDF 文本提取工具 - 从 PDF 文件中提取文本内容和关键信息',
        epilog='示例: pdf-extractor input.pdf -o output.txt -f json --extract-key-info',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # 必需参数：输入文件路径
    parser.add_argument(
        'input',
        type=str,
        help='PDF 文件路径（支持相对路径、绝对路径、中文路径）'
    )
    
    # 可选参数：配置文件路径
    parser.add_argument(
        '-c', '--config',
        type=str,
        default=None,
        metavar='FILE',
        help='配置文件路径（可选）。如果不指定，将使用默认配置'
    )
    
    # 可选参数：输出文件路径
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        metavar='FILE',
        help='输出文件路径（可选）。如果不指定，结果将输出到标准输出'
    )
    
    # 可选参数：输出格式
    parser.add_argument(
        '-f', '--format',
        type=str,
        choices=['text', 'json', 'markdown'],
        default='text',
        help='输出格式（默认: text）。可选值: text（纯文本）, json（JSON格式）, markdown（Markdown格式）'
    )
    
    # 可选参数：是否提取关键信息
    parser.add_argument(
        '--extract-key-info',
        action='store_true',
        default=False,
        help='提取关键信息（标题、关键词、摘要、列表）'
    )
    
    # 可选参数：不提取关键信息（与上面互斥）
    parser.add_argument(
        '--no-key-info',
        action='store_true',
        default=False,
        help='不提取关键信息，仅提取原始文本'
    )
    
    # 可选参数：显示进度
    parser.add_argument(
        '--progress',
        action='store_true',
        default=False,
        help='显示提取进度（对于大文件很有用）'
    )
    
    # 可选参数：详细输出
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        default=False,
        help='显示详细的日志信息'
    )
    
    # 可选参数：静默模式
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        default=False,
        help='静默模式，只输出结果或错误信息'
    )
    
    return parser


def setup_logging(verbose: bool = False, quiet: bool = False, config_manager=None):
    """配置日志系统
    
    参数:
        verbose: 是否显示详细日志
        quiet: 是否静默模式
        config_manager: 配置管理器（可选）
    """
    # 确定日志级别
    if quiet:
        # 静默模式：只显示错误
        level = "ERROR"
    elif verbose:
        # 详细模式：显示所有信息
        level = "DEBUG"
    else:
        # 默认模式：显示警告和错误
        level = "WARNING"
    
    # 从配置管理器获取日志配置（如果提供）
    log_to_file = False
    log_file_path = None
    format_style = "simple"
    
    if config_manager:
        config = config_manager.get_config()
        log_to_file = config.log_to_file
        log_file_path = config.log_file_path
        if verbose:
            format_style = "debug"
    
    # 使用新的日志系统
    return setup_logger_system(
        level=level,
        log_to_file=log_to_file,
        log_file_path=log_file_path,
        format_style=format_style
    )


def print_result(result: str, output_file: str = None, quiet: bool = False):
    """打印或保存结果
    
    参数:
        result: 提取的结果字符串
        output_file: 输出文件路径（如果已保存）
        quiet: 是否静默模式
    """
    if output_file:
        # 如果已保存到文件，显示成功消息
        if not quiet:
            print(f"\n✓ 提取完成！结果已保存到: {output_file}")
    else:
        # 否则输出到标准输出
        print(result)


def main(args=None):
    """主函数
    
    参数:
        args: 命令行参数列表（用于测试），如果为 None 则从 sys.argv 读取
    
    返回:
        退出代码（0 表示成功，1 表示失败）
    """
    # 解析命令行参数
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    
    # 加载配置
    config_manager = get_config_manager(parsed_args.config)
    config = config_manager.get_config()
    
    # 配置日志
    setup_logging(parsed_args.verbose, parsed_args.quiet, config_manager)
    
    # 确定是否提取关键信息
    extract_key_info = parsed_args.extract_key_info
    if parsed_args.no_key_info:
        extract_key_info = False
    elif not parsed_args.extract_key_info and not parsed_args.no_key_info:
        # 如果用户没有指定，使用配置文件中的默认值
        extract_key_info = config.extract_key_info
    
    # 确定输出格式
    output_format = parsed_args.format
    if output_format == 'text' and parsed_args.format == 'text':
        # 如果用户没有明确指定格式，使用配置文件中的默认值
        # 注意：argparse 的 default 会覆盖，所以这里只是示例
        output_format = config.default_output_format
    
    try:
        # 显示开始消息
        if not parsed_args.quiet:
            print(f"正在处理文件: {parsed_args.input}")
            if extract_key_info:
                print("将提取关键信息...")
        
        # 创建服务实例
        service = PDFExtractionService()
        
        # 执行提取
        result = service.extract(
            file_path=parsed_args.input,
            output_format=output_format,
            extract_key_info=extract_key_info,
            output_file=parsed_args.output,
            show_progress=parsed_args.progress
        )
        
        # 打印结果
        print_result(result, parsed_args.output, parsed_args.quiet)
        
        return 0
        
    except PDFExtractionError as e:
        # 处理已知的 PDF 提取错误
        print(f"\n✗ {str(e)}", file=sys.stderr)
        return 1
        
    except KeyboardInterrupt:
        # 处理用户中断
        print("\n\n✗ 操作已取消", file=sys.stderr)
        return 1
        
    except Exception as e:
        # 处理未预期的错误
        print(f"\n✗ 发生未知错误: {str(e)}", file=sys.stderr)
        if parsed_args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
