"""
脚本基类
定义所有文件处理脚本的统一接口
"""

import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..config import SSFConfig


class BaseScript(ABC):
    """脚本基类"""
    
    def __init__(self, config: SSFConfig, working_dir: Path):
        """
        初始化脚本
        
        Args:
            config: 合并后的配置对象
            working_dir: 命令运行的目录路径
        """
        self.config = config
        self.working_dir = working_dir
        self.logger = None  # 将在子类中设置
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        执行脚本的主要逻辑
        
        Args:
            **kwargs: 脚本特定的参数
            
        Returns:
            执行结果字典
        """
        pass
    
    @abstractmethod
    def validate_params(self, **kwargs) -> bool:
        """
        验证脚本参数
        
        Args:
            **kwargs: 脚本特定的参数
            
        Returns:
            参数是否有效
        """
        pass
    
    def get_supported_extensions(self) -> List[str]:
        """
        获取脚本支持的文件扩展名
        
        Returns:
            支持的文件扩展名列表
        """
        return []
    
    def get_script_info(self) -> Dict[str, Any]:
        """
        获取脚本信息
        
        Returns:
            脚本信息字典
        """
        return {
            "name": self.__class__.__name__,
            "description": self.__doc__ or "无描述",
            "supported_extensions": self.get_supported_extensions(),
            "config_keys": self.get_config_keys()
        }
    
    def get_config_keys(self) -> List[str]:
        """
        获取脚本使用的配置键
        
        Returns:
            配置键列表
        """
        return []
    
    def log_info(self, message: str):
        """记录信息日志"""
        if self.logger:
            self.logger.info(message)
    
    def log_success(self, message: str):
        """记录成功日志"""
        if self.logger:
            self.logger.success(message)
    
    def log_warning(self, message: str):
        """记录警告日志"""
        if self.logger:
            self.logger.warning(message)
    
    def log_error(self, message: str):
        """记录错误日志"""
        if self.logger:
            self.logger.error(message)
    
    def find_files(self, pattern: str = "*", recursive: bool = True) -> List[Path]:
        """
        查找文件
        
        Args:
            pattern: 文件模式
            recursive: 是否递归查找
            
        Returns:
            文件路径列表
        """
        files = []
        
        if recursive:
            search_pattern = f"**/{pattern}"
            files = list(self.working_dir.rglob(pattern))
        else:
            files = list(self.working_dir.glob(pattern))
        
        # 过滤掉目录
        files = [f for f in files if f.is_file()]
        
        return files
    
    def get_file_info(self, file_path: Path) -> Dict[str, Any]:
        """
        获取文件信息
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件信息字典
        """
        stat = file_path.stat()
        
        return {
            "path": str(file_path),
            "name": file_path.name,
            "stem": file_path.stem,
            "suffix": file_path.suffix,
            "size": stat.st_size,
            "modified": stat.st_mtime,
            "created": stat.st_ctime,
            "is_file": file_path.is_file(),
            "is_dir": file_path.is_dir(),
            "exists": file_path.exists()
        }
    
    def backup_file(self, file_path: Path, backup_dir: Optional[Path] = None) -> Path:
        """
        备份文件
        
        Args:
            file_path: 要备份的文件路径
            backup_dir: 备份目录，如果为None则使用配置中的备份目录
            
        Returns:
            备份文件路径
        """
        if backup_dir is None:
            backup_dir = Path(self.config.backup_dir or ".backup")
        
        # 确保备份目录存在
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建备份文件名
        backup_name = f"{file_path.stem}_backup_{int(file_path.stat().st_mtime)}{file_path.suffix}"
        backup_path = backup_dir / backup_name
        
        # 复制文件
        import shutil
        shutil.copy2(file_path, backup_path)
        
        # 验证备份文件是否创建成功
        if not backup_path.exists():
            raise Exception(f"备份文件创建失败: {backup_path}")
        
        return backup_path 