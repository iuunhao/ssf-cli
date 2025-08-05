"""
工具函数模块
包含路径收集、日志记录等实用功能
"""

import os
import sys
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel

console = Console()


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
    # 检查是否在虚拟环境中
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        return False
    
    # 检查安装路径
    try:
        import ssf_cli
        module_path = Path(ssf_cli.__file__).parent
        # 如果模块路径在用户目录或系统目录下，认为是全局安装
        return any(part in str(module_path) for part in ['site-packages', 'dist-packages'])
    except ImportError:
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