import os
import uuid

from smolagents import Tool
from loguru import logger


class FileReadTool(Tool):
    """文件读取工具，用于读取指定路径的文件内容。
    
    支持多种文件格式的读取，包括文本文件、JSON、YAML等。
    
    Args:
        max_file_size (int, default 1024*1024): 最大文件大小限制（字节），默认1MB
        encoding (str, default "utf-8"): 文件编码格式
        
    Examples:
        ```python
        >>> from src.tools.file_tool import FileReadTool
        >>> file_reader = FileReadTool(max_file_size=2*1024*1024)
        >>> content = file_reader("./example.txt")
        >>> print(content)
        ```
    """
    
    name = "file_read"
    description = "读取指定路径的文件内容并返回文件内容字符串。支持文本文件、JSON、YAML等格式。"
    inputs = {
        "file_name": {
            "type": "string", 
            "description": "要读取的文件名"
        }
    }
    output_type = "string"
    
    def __init__(self, max_file_size: int = 1024*1024, encoding: str = "utf-8", work_path: str = None):
        super().__init__()
        self.max_file_size = max_file_size
        self.encoding = encoding
        self.work_path = work_path
    
    def forward(self, file_name: str) -> str:
        logger.info(f"开始读取文件: {file_name}")
        
        file_path = os.path.join(self.work_path, file_name)

        try:
            # 检查文件是否存在
            if not os.path.exists(file_path):
                logger.error(f"文件不存在: {file_path}")
                return f"错误：文件不存在 - {file_path}"
            
            # 检查是否为文件（而非目录）
            if not os.path.isfile(file_path):
                logger.error(f"指定路径不是文件: {file_path}")
                return f"错误：指定路径不是文件 - {file_path}"
            
            # 检查文件大小
            file_size = os.path.getsize(file_path)
            logger.debug(f"文件大小: {file_size} 字节, 限制: {self.max_file_size} 字节")
            
            if file_size > self.max_file_size:
                logger.warning(f"文件过大: {file_size} 字节，超过限制 {self.max_file_size} 字节")
                return f"错误：文件过大 ({file_size} 字节)，超过限制 ({self.max_file_size} 字节)"
            
            # 读取文件内容
            with open(file_path, 'r', encoding=self.encoding) as file:
                content = file.read()
            
            logger.success(f"文件读取成功: {file_path}, 内容长度: {len(content)} 字符")
            return f"## 文件读取成功\n\n**文件路径:** {file_path}\n**文件大小:** {file_size} 字节\n\n**文件内容:**\n```\n{content}\n```"
            
        except UnicodeDecodeError as e:
            logger.warning(f"文本解码失败，尝试二进制读取: {file_path}, 错误: {e}")
            try:
                # 尝试二进制模式读取
                with open(file_path, 'rb') as file:
                    content = file.read()
                logger.info(f"二进制文件读取成功: {file_path}, 大小: {len(content)} 字节")
                return f"## 二进制文件读取成功\n\n**文件路径:** {file_path}\n**文件大小:** {len(content)} 字节\n\n**注意:** 这是一个二进制文件，内容已转换为十六进制表示\n**内容预览:** {content[:100].hex()}..."
            except Exception as e:
                logger.error(f"二进制读取也失败: {file_path}, 错误: {e}")
                return f"错误：无法读取文件 - {str(e)}"
        except PermissionError as e:
            logger.error(f"权限不足，无法读取文件: {file_path}, 错误: {e}")
            return f"错误：没有权限读取文件 - {file_path}"
        except Exception as e:
            logger.error(f"读取文件时发生未知异常: {file_path}, 错误: {e}")
            return f"错误：读取文件时发生异常 - {str(e)}"


class FileSaveTool(Tool):
    """文件保存工具，用于将内容保存到指定路径的文件中。
    
    支持创建新文件或覆盖现有文件，自动创建目录结构。
    
    Args:
        auto_create_dirs (bool, default True): 是否自动创建不存在的目录
        backup_existing (bool, default False): 是否备份现有文件
        encoding (str, default "utf-8"): 文件编码格式
        default_output_dir (str, optional): 默认输出目录，当file_path为None时使用
        
    Examples:
        ```python
        >>> from src.tools.file_tool import FileSaveTool
        >>> 
        >>> # 使用默认输出目录
        >>> file_saver = FileSaveTool(default_output_dir="tmp/my_output")
        >>> result = file_saver("Hello, World!", "test.txt")  # 保存到 tmp/my_output/test.txt
        >>> 
        >>> # 指定具体路径
        >>> result = file_saver("Hello, World!", "test.txt", "custom/path")  # 保存到 custom/path/test.txt
        >>> 
        >>> # 启用备份功能
        >>> file_saver = FileSaveTool(backup_existing=True, default_output_dir="tmp/backup_test")
        >>> result = file_saver("New content", "existing.txt")
        ```
    """
    
    name = "file_save"
    description = "将指定内容保存到文件中。支持创建新文件或覆盖现有文件，可自动创建目录结构。"
    inputs = {
        "content": {
            "type": "string",
            "description": "要保存的文件内容"
        },
        "file_name": {
            "type": "string",
            "description": "要保存的文件名"
        }
    }
    output_type = "string"
    
    def __init__(self, auto_create_dirs: bool = True, backup_existing: bool = False, encoding: str = "utf-8", work_path: str = None):
        super().__init__()
        self.auto_create_dirs = auto_create_dirs
        self.backup_existing = backup_existing
        self.encoding = encoding
        self.work_path = work_path
    
    def forward(
        self, 
        content: str, 
        file_name: str,
    ) -> str:
        # 如果没有提供文件路径，使用默认输出目录或自动生成
        if self.work_path:
            file_path = self.work_path
            # 确保默认输出目录存在
            if self.auto_create_dirs:
                os.makedirs(file_path, exist_ok=True)
        else:
            file_path = f"tmp_{uuid.uuid4().hex[:8]}"
            os.makedirs(file_path, exist_ok=True)
        
        # 构建完整的文件路径
        full_file_path = os.path.join(file_path, file_name)
        
        logger.info(f"开始保存文件: {full_file_path}, 内容长度: {len(content)} 字符")
        
        try:
            # 获取目录路径
            dir_path = os.path.dirname(full_file_path)
            logger.debug(f"目标目录: {dir_path}")
            
            # 自动创建目录
            if self.auto_create_dirs and dir_path and not os.path.exists(dir_path):
                logger.info(f"创建目录: {dir_path}")
                os.makedirs(dir_path, exist_ok=True)
                logger.success(f"目录创建成功: {dir_path}")
            
            # 备份现有文件
            backup_info = ""
            if self.backup_existing and os.path.exists(full_file_path):
                backup_path = f"{full_file_path}.backup"
                counter = 1
                while os.path.exists(backup_path):
                    backup_path = f"{full_file_path}.backup.{counter}"
                    counter += 1
                
                logger.info(f"备份现有文件: {full_file_path} -> {backup_path}")
                import shutil
                shutil.copy2(full_file_path, backup_path)
                backup_info = f"\n**备份文件:** {backup_path}"
                logger.success(f"文件备份成功: {backup_path}")
            
            # 保存文件
            with open(full_file_path, 'w', encoding=self.encoding) as file:
                file.write(content)
            
            # 获取保存后的文件信息
            file_size = os.path.getsize(full_file_path)
            logger.success(f"文件保存成功: {full_file_path}, 文件大小: {file_size} 字节")
            
            return f"## 文件保存成功\n\n**文件名:** {file_name}\n**文件大小:** {file_size} 字节\n**内容长度:** {len(content)} 字符{backup_info}"
            
        except PermissionError as e:
            logger.error(f"权限不足，无法写入文件: {file_name}, 错误: {e}")
            return f"错误：没有权限写入文件 - {file_name}"
        except OSError as e:
            logger.error(f"无法创建目录或文件: {file_name}, 错误: {e}")
            return f"错误：无法创建目录或文件 - {str(e)}"
        except Exception as e:
            logger.error(f"保存文件时发生未知异常: {file_name}, 错误: {e}")
            return f"错误：保存文件时发生异常 - {str(e)}"
