"""
工具函数模块
包含路径收集、日志记录等实用功能
"""

import os
import sys
import logging
from pathlib import Path
from typing import Optional
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.logging import RichHandler

console = Console()


def setup_logger(name: str = "ssf_cli", level: str = "INFO") -> logging.Logger:
    """设置专业的日志记录器"""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # 清除现有的处理器
    logger.handlers.clear()
    
    # 创建Rich处理器，提供美观的日志输出
    rich_handler = RichHandler(
        console=console,
        show_time=True,
        show_path=False,
        markup=True,
        rich_tracebacks=True
    )
    
    # 设置格式
    formatter = logging.Formatter(
        fmt="[NLPro] %(message)s",
        datefmt="%H:%M:%S"
    )
    rich_handler.setFormatter(formatter)
    
    logger.addHandler(rich_handler)
    
    return logger


def get_logger(name: str = "ssf_cli") -> logging.Logger:
    """获取日志记录器"""
    return logging.getLogger(name)


def log_info(message: str, logger: Optional[logging.Logger] = None) -> None:
    """记录信息日志"""
    if logger is None:
        logger = get_logger()
    logger.info(f"ℹ️  {message}")


def log_success(message: str, logger: Optional[logging.Logger] = None) -> None:
    """记录成功日志"""
    if logger is None:
        logger = get_logger()
    logger.info(f"✅ {message}")


def log_warning(message: str, logger: Optional[logging.Logger] = None) -> None:
    """记录警告日志"""
    if logger is None:
        logger = get_logger()
    logger.warning(f"⚠️  {message}")


def log_error(message: str, logger: Optional[logging.Logger] = None) -> None:
    """记录错误日志"""
    if logger is None:
        logger = get_logger()
    logger.error(f"❌ {message}")


def log_debug(message: str, logger: Optional[logging.Logger] = None) -> None:
    """记录调试日志"""
    if logger is None:
        logger = get_logger()
    logger.debug(f"🔍 {message}")


def get_current_working_directory() -> Path:
    """获取当前工作目录"""
    return Path.cwd()


def get_execution_directory() -> Path:
    """获取命令执行目录"""
    return Path.cwd()


def ensure_directory_exists(directory: Path) -> None:
    """确保目录存在，如果不存在则创建"""
    directory.mkdir(parents=True, exist_ok=True)


def get_project_root() -> Optional[Path]:
    """获取项目根目录（包含pyproject.toml的目录）"""
    current = Path.cwd()
    
    # 向上查找包含pyproject.toml的目录
    for parent in [current] + list(current.parents):
        if (parent / "pyproject.toml").exists():
            return parent
    
    return None


def display_banner() -> None:
    """显示SSF CLI横幅"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                        SSF CLI                               ║
    ║                 Simple & Smart Framework                     ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    console.print(Panel(banner, style="cyan"))


def display_info(title: str, content: str) -> None:
    """显示信息面板"""
    console.print(Panel(content, title=title, style="green"))


def display_warning(message: str) -> None:
    """显示警告信息"""
    console.print(f"[yellow]⚠️  警告: {message}[/yellow]")


def display_error(message: str) -> None:
    """显示错误信息"""
    console.print(f"[red]❌ 错误: {message}[/red]")


def display_success(message: str) -> None:
    """显示成功信息"""
    console.print(f"[green]✅ {message}[/green]")


def is_installed_globally() -> bool:
    """检查是否全局安装"""
    try:
        import ssf_cli
        module_path = Path(ssf_cli.__file__).parent
        
        # 检查是否在虚拟环境中
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            return False
        
        # 检查模块路径是否在系统Python目录中
        module_path_str = str(module_path)
        
        # 检查是否在site-packages或dist-packages中
        if any(part in module_path_str for part in ['site-packages', 'dist-packages']):
            return True
        
        # 检查是否在用户安装目录中（pip install --user）
        user_site = Path(sys.__path__[0]).parent / "site-packages"
        if module_path == user_site:
            return True
        
        # 检查是否在开发模式下安装（-e 参数）
        if "src" in module_path_str and "ssf_cli" in module_path_str:
            return False
        
        # 检查是否在项目目录中运行
        current_dir = Path.cwd()
        if module_path.is_relative_to(current_dir):
            return False
        
        # 如果模块路径不在当前目录，且不在虚拟环境中，认为是全局安装
        return True
        
    except ImportError:
        return False
    except Exception:
        return False


def get_installation_info() -> dict:
    """获取安装信息"""
    info = {
        "is_global": is_installed_globally(),
        "python_version": sys.version,
        "executable": sys.executable,
        "working_directory": str(get_current_working_directory()),
    }
    
    try:
        import ssf_cli
        info["module_path"] = str(Path(ssf_cli.__file__).parent)
    except ImportError:
        info["module_path"] = "未安装"
    
    return info


def validate_python_version() -> bool:
    """验证Python版本"""
    if sys.version_info < (3, 8):
        display_error("需要Python 3.8或更高版本")
        return False
    return True


def check_dependencies() -> bool:
    """检查依赖项"""
    required_packages = ["typer", "rich", "pydantic"]
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        display_error(f"缺少依赖项: {', '.join(missing_packages)}")
        display_info("安装提示", f"请运行: pip install {' '.join(missing_packages)}")
        return False
    
    return True 