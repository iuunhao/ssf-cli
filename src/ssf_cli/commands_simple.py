"""
简化的命令模块
"""

import typer
from rich.console import Console

console = Console()
app = typer.Typer(help="SSF CLI - 一个功能强大的命令行工具")


@app.command()
def version():
    """显示版本信息"""
    console.print("SSF CLI v0.1.0")


@app.command()
def info():
    """显示系统信息"""
    console.print("系统信息")


@app.command()
def debug():
    """调试信息"""
    console.print("调试信息")


@app.command()
def help():
    """帮助信息"""
    console.print("帮助信息")


# 设置默认命令
@app.callback()
def main():
    """SSF CLI - 一个功能强大的命令行工具"""
    pass 