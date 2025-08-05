"""
命令模块
包含各种CLI命令的实现
"""

import typer
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
import json
import shutil

from .config import config_manager
from .utils import (
    get_current_working_directory,
    get_execution_directory,
    display_banner,
    display_info,
    display_success,
    display_warning,
    display_error,
    get_installation_info,
    validate_python_version,
    check_dependencies,
    log_info,
    log_success,
    log_warning,
    log_error,
)

console = Console()
app = typer.Typer(help="SSF CLI - 一个功能强大的命令行工具")


@app.command()
def version():
    """显示版本信息"""
    from . import __version__
    display_info("版本信息", f"SSF CLI v{__version__}")


@app.command()
def pwd():
    """显示当前工作目录"""
    current_dir = get_current_working_directory()
    execution_dir = get_execution_directory()
    
    table = Table(title="目录信息")
    table.add_column("类型", style="cyan")
    table.add_column("路径", style="green")
    
    table.add_row("当前工作目录", str(current_dir))
    table.add_row("命令执行目录", str(execution_dir))
    
    console.print(table)


@app.command()
def info():
    """显示系统信息"""
    display_banner()
    
    # 验证环境
    if not validate_python_version():
        return
    
    if not check_dependencies():
        return
    
    # 获取安装信息
    install_info = get_installation_info()
    
    table = Table(title="系统信息 - 测试修改生效")
    table.add_column("项目", style="cyan")
    table.add_column("值", style="green")
    
    table.add_row("Python版本", install_info["python_version"])
    table.add_row("可执行文件", install_info["executable"])
    table.add_row("工作目录", install_info["working_directory"])
    table.add_row("模块路径", install_info["module_path"])
    table.add_row("全局安装", "是" if install_info["is_global"] else "否")
    
    console.print(table)


@app.command()
def config(
    action: str = typer.Argument(..., help="配置操作: show, init, global, local"),
    key: str = typer.Option(None, "--key", "-k", help="配置键"),
    value: str = typer.Option(None, "--value", "-v", help="配置值"),
):
    """配置管理"""
    
    if action == "show":
        # 显示配置
        config = config_manager.load_config()
        config_manager.show_config(config)
        
    elif action == "init":
        # 初始化配置文件
        config_manager.create_default_configs()
        display_success("配置文件已创建")
        
    elif action == "global":
        # 全局配置操作
        if key and value:
            # 设置全局配置
            config = config_manager.load_config()
            if hasattr(config, key):
                # 根据字段类型转换值
                field = config.model_fields[key]
                try:
                    if field.annotation == bool:
                        # 处理布尔值
                        if value.lower() in ('true', '1', 'yes', 'on'):
                            converted_value = True
                        elif value.lower() in ('false', '0', 'no', 'off'):
                            converted_value = False
                        else:
                            display_error(f"无效的布尔值: {value}")
                            return
                    elif field.annotation == int:
                        converted_value = int(value)
                    elif field.annotation == float:
                        converted_value = float(value)
                    else:
                        converted_value = value
                    
                    setattr(config, key, converted_value)
                    config_manager.save_global_config(config)
                    display_success(f"全局配置已更新: {key} = {converted_value}")
                except (ValueError, TypeError) as e:
                    display_error(f"配置值类型错误: {e}")
            else:
                display_error(f"未知的配置键: {key}")
        else:
            display_error("设置全局配置需要提供 --key 和 --value 参数")
            
    elif action == "local":
        # 本地配置操作
        if key and value:
            # 设置本地配置
            config = config_manager.load_config()
            if hasattr(config, key):
                # 根据字段类型转换值
                field = config.model_fields[key]
                try:
                    if field.annotation == bool:
                        # 处理布尔值
                        if value.lower() in ('true', '1', 'yes', 'on'):
                            converted_value = True
                        elif value.lower() in ('false', '0', 'no', 'off'):
                            converted_value = False
                        else:
                            display_error(f"无效的布尔值: {value}")
                            return
                    elif field.annotation == int:
                        converted_value = int(value)
                    elif field.annotation == float:
                        converted_value = float(value)
                    else:
                        converted_value = value
                    
                    setattr(config, key, converted_value)
                    config_manager.save_local_config(config)
                    display_success(f"本地配置已更新: {key} = {converted_value}")
                except (ValueError, TypeError) as e:
                    display_error(f"配置值类型错误: {e}")
            else:
                display_error(f"未知的配置键: {key}")
        else:
            display_error("设置本地配置需要提供 --key 和 --value 参数")
            
    else:
        display_error(f"未知的配置操作: {action}")


@app.command()
def install():
    """一键安装SSF CLI"""
    display_banner()
    
    # 检查Python版本
    if not validate_python_version():
        return
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 检查是否已安装
    install_info = get_installation_info()
    if install_info["is_global"]:
        display_warning("SSF CLI已经全局安装")
        return
    
    # 执行安装
    try:
        import subprocess
        import sys
        
        # 使用pip安装
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-e", "."
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            display_success("SSF CLI安装成功！")
            display_info("使用说明", "现在您可以在任何地方使用 'ssf' 命令")
        else:
            display_error(f"安装失败: {result.stderr}")
            
    except Exception as e:
        display_error(f"安装过程中出现错误: {e}")


@app.command()
def status():
    """显示SSF CLI状态"""
    display_banner()
    
    # 环境检查
    env_status = []
    env_status.append(("Python版本", "✅ 通过" if validate_python_version() else "❌ 失败"))
    env_status.append(("依赖检查", "✅ 通过" if check_dependencies() else "❌ 失败"))
    
    # 安装状态
    install_info = get_installation_info()
    env_status.append(("全局安装", "✅ 是" if install_info["is_global"] else "⚠️  否"))
    
    # 配置状态
    config = config_manager.load_config()
    env_status.append(("配置加载", "✅ 成功"))
    
    # 显示状态表格
    table = Table(title="SSF CLI 状态")
    table.add_column("检查项目", style="cyan")
    table.add_column("状态", style="green")
    
    for item, status in env_status:
        table.add_row(item, status)
    
    console.print(table)


@app.command()
def debug():
    """调试信息 - 显示详细的系统诊断信息"""
    display_banner()
    
    # 获取详细的安装信息
    install_info = get_installation_info()
    
    # 显示详细的调试信息
    debug_info = []
    debug_info.append(("Python版本", sys.version))
    debug_info.append(("Python可执行文件", sys.executable))
    debug_info.append(("当前工作目录", str(get_current_working_directory())))
    debug_info.append(("模块路径", install_info.get("module_path", "未知")))
    debug_info.append(("是否虚拟环境", "是" if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else "否"))
    
    # 检查sys.path
    debug_info.append(("sys.path长度", str(len(sys.path))))
    
    # 检查模块导入
    try:
        import ssf_cli
        debug_info.append(("ssf_cli模块", f"已导入: {ssf_cli.__file__}"))
    except ImportError as e:
        debug_info.append(("ssf_cli模块", f"导入失败: {e}"))
    
    # 检查配置
    try:
        config = config_manager.load_config()
        debug_info.append(("配置加载", "成功"))
    except Exception as e:
        debug_info.append(("配置加载", f"失败: {e}"))
    
    # 显示调试表格
    table = Table(title="调试信息")
    table.add_column("项目", style="cyan")
    table.add_column("值", style="green")
    
    for item, value in debug_info:
        table.add_row(item, str(value))
    
    console.print(table)
    
    # 显示sys.path的前几个路径
    console.print("\n[cyan]sys.path 前10个路径:[/cyan]")
    for i, path in enumerate(sys.path[:10]):
        console.print(f"  {i+1}. {path}")


@app.command()
def help():
    """显示帮助信息"""
    display_banner()
    
    help_text = """
    可用命令:
    
    ssf version          - 显示版本信息
    ssf pwd             - 显示当前工作目录
    ssf info            - 显示系统信息
    ssf debug           - 显示详细调试信息
    ssf config show     - 显示配置信息
    ssf config init     - 初始化配置文件
    ssf config global   - 设置全局配置
    ssf config local    - 设置本地配置
    ssf install         - 一键安装SSF CLI
    ssf status          - 显示SSF CLI状态
    ssf help            - 显示此帮助信息
    
    配置管理:
    - 内置配置: CLI工具内置的默认配置
    - 全局配置: ~/.ssfrc (用户根目录)
    - 本地配置: ./.ssfrc (当前目录)
    
    配置优先级: 本地配置 > 全局配置 > 内置配置
    """
    
    display_info("SSF CLI 帮助", help_text)


# 设置默认命令
@app.callback()
def main():
    """SSF CLI - 一个功能强大的命令行工具"""
    pass 