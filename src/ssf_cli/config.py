"""
配置管理模块
实现三层配置系统：内置配置、全局配置、本地配置
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

import typer
from pydantic import BaseModel, Field
from rich.console import Console
from rich.table import Table

console = Console()


class SSFConfig(BaseModel):
    """SSF配置模型"""
    
    # 基础配置
    project_name: str = Field(default="SSF Project", description="项目名称")
    version: str = Field(default="0.1.0", description="项目版本")
    
    # 文件操作配置
    output_dir: str = Field(default="./renamed_files", description="输出目录")
    temp_dir: str = Field(default="./temp", description="临时目录")
    
    # 文件处理配置
    file_processing: Dict[str, Any] = Field(default={
        "default_dry_run": False,
        "default_recursive": True,
        "exclude_patterns": [".git", "__pycache__", ".DS_Store"],
        "supported_extensions": ["*"],
        "copy_instead_of_rename": True
    }, description="文件处理配置")
    
    # 重命名配置
    rename_config: Dict[str, Any] = Field(default={
        "default_prefix": "",
        "default_suffix": "",
        "conflict_resolution": "timestamp",
        "date_format": "%Y%m%d_%H%M%S",
        "preserve_original": True
    }, description="重命名配置")
    
    # 日志配置
    log_level: str = Field(default="INFO", description="日志级别")
    log_file: str = Field(default="./logs/ssf.log", description="日志文件路径")
    
    # 网络配置
    timeout: int = Field(default=30, description="请求超时时间（秒）")
    retry_count: int = Field(default=3, description="重试次数")
    
    # 其他配置
    debug: bool = Field(default=False, description="调试模式")
    verbose: bool = Field(default=False, description="详细输出")


class ConfigManager:
    """配置管理器"""
    
    def __init__(self):
        self.config_file_name = ".ssfrc"
        self.builtin_config = self._get_builtin_config()
        self.global_config_path = self._get_global_config_path()
        self.local_config_path = self._get_local_config_path()
        
    def _get_builtin_config(self) -> Dict[str, Any]:
        """获取内置配置"""
        return SSFConfig().model_dump()
    
    def _get_global_config_path(self) -> Path:
        """获取全局配置文件路径"""
        home = Path.home()
        return home / self.config_file_name
    
    def _get_local_config_path(self) -> Path:
        """获取本地配置文件路径"""
        return Path.cwd() / self.config_file_name
    
    def load_config(self) -> SSFConfig:
        """加载配置，按优先级合并"""
        config_dict = self.builtin_config.copy()
        
        # 加载全局配置
        if self.global_config_path.exists():
            try:
                with open(self.global_config_path, 'r', encoding='utf-8') as f:
                    global_config = json.load(f)
                config_dict.update(global_config)
            except Exception as e:
                console.print(f"[yellow]警告: 无法读取全局配置文件: {e}[/yellow]")
        
        # 加载本地配置
        if self.local_config_path.exists():
            try:
                with open(self.local_config_path, 'r', encoding='utf-8') as f:
                    local_config = json.load(f)
                config_dict.update(local_config)
            except Exception as e:
                console.print(f"[yellow]警告: 无法读取本地配置文件: {e}[/yellow]")
        
        return SSFConfig(**config_dict)
    
    def save_global_config(self, config: SSFConfig) -> None:
        """保存全局配置"""
        try:
            config_dict = config.model_dump()
            with open(self.global_config_path, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)
            console.print(f"[green]全局配置已保存到: {self.global_config_path}[/green]")
        except Exception as e:
            console.print(f"[red]错误: 无法保存全局配置: {e}[/red]")
    
    def save_local_config(self, config: SSFConfig) -> None:
        """保存本地配置"""
        try:
            config_dict = config.model_dump()
            with open(self.local_config_path, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)
            console.print(f"[green]本地配置已保存到: {self.local_config_path}[/green]")
        except Exception as e:
            console.print(f"[red]错误: 无法保存本地配置: {e}[/red]")
    
    def show_config(self, config: SSFConfig) -> None:
        """显示配置信息"""
        table = Table(title="SSF 配置信息")
        table.add_column("配置项", style="cyan")
        table.add_column("值", style="green")
        table.add_column("描述", style="yellow")
        
        for field_name, field in config.model_fields.items():
            value = getattr(config, field_name)
            description = field.description or ""
            table.add_row(field_name, str(value), description)
        
        console.print(table)
        
        # 显示配置文件路径
        console.print(f"\n[cyan]配置文件路径:[/cyan]")
        console.print(f"  内置配置: 内置")
        console.print(f"  全局配置: {self.global_config_path}")
        console.print(f"  本地配置: {self.local_config_path}")
    
    def create_default_configs(self) -> None:
        """创建默认配置文件"""
        default_config = SSFConfig()
        
        # 创建全局配置
        if not self.global_config_path.exists():
            self.save_global_config(default_config)
        
        # 创建本地配置
        if not self.local_config_path.exists():
            self.save_local_config(default_config)


# 全局配置管理器实例
config_manager = ConfigManager() 