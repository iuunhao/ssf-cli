"""
SSF CLI 主入口文件
"""

import typer
from rich.console import Console

from .commands import app
from .utils import display_banner, get_current_working_directory

console = Console()


def main():
    """主入口函数"""
    # 收集当前执行目录
    current_dir = get_current_working_directory()
    
    # 设置环境变量，供其他模块使用
    import os
    os.environ["SSF_CURRENT_DIR"] = str(current_dir)
    
    # 运行Typer应用
    app()


if __name__ == "__main__":
    main() 