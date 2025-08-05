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
    
    table = Table(title="系统信息 - 开发模式全局可用测试1")
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
    
    基础命令:
    ssf version          - 显示版本信息
    ssf pwd             - 显示当前工作目录
    ssf info            - 显示系统信息
    ssf debug           - 显示详细调试信息
    ssf status          - 显示SSF CLI状态
    ssf help            - 显示此帮助信息
    
    配置管理:
    ssf config show     - 显示配置信息
    ssf config init     - 初始化配置文件
    ssf config global   - 设置全局配置
    ssf config local    - 设置本地配置
    
    项目工具:
    ssf create python   - 创建Python项目
    ssf create web      - 创建Web项目
    ssf create cli      - 创建CLI项目
    ssf create api      - 创建API项目
    
    网络工具:
    ssf fetch <url>     - 网络请求工具
    
    文件工具:
    ssf files list      - 列出文件
    ssf files find      - 查找文件
    ssf files count     - 统计文件
    ssf files size      - 目录大小
    
    系统工具:
    ssf system          - 系统信息工具
    
    安装管理:
    ssf install         - 一键安装SSF CLI
    
    配置管理:
    - 内置配置: CLI工具内置的默认配置
    - 全局配置: ~/.ssfrc (用户根目录)
    - 本地配置: ./.ssfrc (当前目录)
    
    配置优先级: 本地配置 > 全局配置 > 内置配置
    
    使用示例:
    ssf create python --name my-project
    ssf fetch https://httpbin.org/json
    ssf files list --path /tmp
    ssf system
    """
    
    display_info("SSF CLI 帮助", help_text)


@app.command()
def create(
    template: str = typer.Argument(..., help="项目模板类型: python, web, cli, api"),
    name: str = typer.Option(None, "--name", "-n", help="项目名称"),
    path: str = typer.Option(".", "--path", "-p", help="项目路径"),
):
    """创建新项目"""
    display_banner()
    
    if not name:
        name = typer.prompt("请输入项目名称")
    
    project_path = Path(path) / name
    
    if project_path.exists():
        display_error(f"项目目录已存在: {project_path}")
        return
    
    # 创建项目目录
    project_path.mkdir(parents=True, exist_ok=True)
    
    # 根据模板创建项目
    if template == "python":
        create_python_project(project_path, name)
    elif template == "web":
        create_web_project(project_path, name)
    elif template == "cli":
        create_cli_project(project_path, name)
    elif template == "api":
        create_api_project(project_path, name)
    else:
        display_error(f"未知的模板类型: {template}")
        return
    
    display_success(f"项目创建成功: {project_path}")


@app.command()
def fetch(
    url: str = typer.Argument(..., help="要获取的URL"),
    output: str = typer.Option(None, "--output", "-o", help="输出文件路径"),
    method: str = typer.Option("GET", "--method", "-m", help="HTTP方法"),
):
    """网络请求工具"""
    display_banner()
    
    try:
        import requests
        
        log_info(f"正在请求: {method} {url}")
        
        response = requests.request(method, url, timeout=30)
        
        if response.status_code == 200:
            display_success(f"请求成功 (状态码: {response.status_code})")
            
            if output:
                with open(output, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                display_success(f"内容已保存到: {output}")
            else:
                # 显示前500个字符
                content = response.text[:500]
                if len(response.text) > 500:
                    content += "\n... (内容已截断)"
                display_info("响应内容", content)
        else:
            display_error(f"请求失败 (状态码: {response.status_code})")
            
    except ImportError:
        display_error("缺少requests模块，请运行: pip install requests")
    except Exception as e:
        display_error(f"请求失败: {e}")


@app.command()
def files(
    action: str = typer.Argument(..., help="操作类型: list, find, count, size"),
    path: str = typer.Option(".", "--path", "-p", help="目录路径"),
    pattern: str = typer.Option("*", "--pattern", help="文件模式"),
):
    """文件操作工具"""
    display_banner()
    
    target_path = Path(path)
    
    if not target_path.exists():
        display_error(f"路径不存在: {target_path}")
        return
    
    if action == "list":
        list_files(target_path, pattern)
    elif action == "find":
        find_files(target_path, pattern)
    elif action == "count":
        count_files(target_path, pattern)
    elif action == "size":
        get_directory_size(target_path)
    else:
        display_error(f"未知的操作类型: {action}")


@app.command()
def system():
    """系统信息工具"""
    display_banner()
    
    import platform
    import psutil
    
    try:
        # 系统信息
        system_info = []
        system_info.append(("操作系统", platform.system()))
        system_info.append(("系统版本", platform.version()))
        system_info.append(("架构", platform.machine()))
        system_info.append(("处理器", platform.processor()))
        
        # 内存信息
        memory = psutil.virtual_memory()
        system_info.append(("总内存", f"{memory.total / (1024**3):.2f} GB"))
        system_info.append(("可用内存", f"{memory.available / (1024**3):.2f} GB"))
        system_info.append(("内存使用率", f"{memory.percent:.1f}%"))
        
        # CPU信息
        cpu_percent = psutil.cpu_percent(interval=1)
        system_info.append(("CPU使用率", f"{cpu_percent:.1f}%"))
        system_info.append(("CPU核心数", str(psutil.cpu_count())))
        
        # 磁盘信息
        disk = psutil.disk_usage('/')
        system_info.append(("磁盘总空间", f"{disk.total / (1024**3):.2f} GB"))
        system_info.append(("磁盘可用空间", f"{disk.free / (1024**3):.2f} GB"))
        system_info.append(("磁盘使用率", f"{disk.percent:.1f}%"))
        
        # 显示表格
        table = Table(title="系统信息")
        table.add_column("项目", style="cyan")
        table.add_column("值", style="green")
        
        for item, value in system_info:
            table.add_row(item, str(value))
        
        console.print(table)
        
    except ImportError:
        display_error("缺少psutil模块，请运行: pip install psutil")
    except Exception as e:
        display_error(f"获取系统信息失败: {e}")


# 辅助函数
def create_python_project(path: Path, name: str):
    """创建Python项目"""
    # 创建基本目录结构
    (path / "src" / name).mkdir(parents=True, exist_ok=True)
    (path / "tests").mkdir(exist_ok=True)
    (path / "docs").mkdir(exist_ok=True)
    
    # 创建pyproject.toml
    pyproject_content = f'''[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{name}"
version = "0.1.0"
description = "A Python project"
authors = [{{name = "Your Name", email = "your.email@example.com"}}]
readme = "README.md"
requires-python = ">=3.8"
dependencies = []

[project.optional-dependencies]
dev = ["pytest", "black", "isort", "flake8"]
'''
    
    with open(path / "pyproject.toml", "w") as f:
        f.write(pyproject_content)
    
    # 创建README
    readme_content = f'''# {name}

A Python project created with SSF CLI.

## Installation

```bash
pip install -e .
```

## Usage

```python
from {name} import main

main()
```
'''
    
    with open(path / "README.md", "w") as f:
        f.write(readme_content)
    
    # 创建__init__.py
    with open(path / "src" / name / "__init__.py", "w") as f:
        f.write(f'"""\n{name} package\n"""\n\n__version__ = "0.1.0"\n')


def create_web_project(path: Path, name: str):
    """创建Web项目"""
    # 创建基本目录结构
    (path / "static").mkdir(exist_ok=True)
    (path / "templates").mkdir(exist_ok=True)
    (path / "static" / "css").mkdir(exist_ok=True)
    (path / "static" / "js").mkdir(exist_ok=True)
    
    # 创建app.py
    app_content = f'''from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
'''
    
    with open(path / "app.py", "w") as f:
        f.write(app_content)
    
    # 创建requirements.txt
    requirements_content = '''flask>=2.0.0
jinja2>=3.0.0
'''
    
    with open(path / "requirements.txt", "w") as f:
        f.write(requirements_content)
    
    # 创建HTML模板
    html_content = f'''<!DOCTYPE html>
<html>
<head>
    <title>{name}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <h1>Welcome to {name}</h1>
    <p>This is a web project created with SSF CLI.</p>
    <script src="{{ url_for('static', filename='js/app.js') }}"></script>
</body>
</html>
'''
    
    with open(path / "templates" / "index.html", "w") as f:
        f.write(html_content)


def create_cli_project(path: Path, name: str):
    """创建CLI项目"""
    # 创建基本目录结构
    (path / "src" / name).mkdir(parents=True, exist_ok=True)
    
    # 创建pyproject.toml
    pyproject_content = f'''[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{name}"
version = "0.1.0"
description = "A CLI tool"
authors = [{{name = "Your Name", email = "your.email@example.com"}}]
readme = "README.md"
requires-python = ">=3.8"
dependencies = ["typer", "rich"]

[project.scripts]
{name} = "{name}.main:app"

[tool.hatch.build.targets.wheel]
packages = ["src/{name}"]
'''
    
    with open(path / "pyproject.toml", "w") as f:
        f.write(pyproject_content)
    
    # 创建main.py
    main_content = f'''import typer
from rich.console import Console

app = typer.Typer()
console = Console()

@app.command()
def hello():
    """Say hello"""
    console.print("Hello from {name}!")

if __name__ == "__main__":
    app()
'''
    
    with open(path / "src" / name / "main.py", "w") as f:
        f.write(main_content)
    
    # 创建__init__.py
    with open(path / "src" / name / "__init__.py", "w") as f:
        f.write(f'"""\n{name} CLI tool\n"""\n\n__version__ = "0.1.0"\n')


def create_api_project(path: Path, name: str):
    """创建API项目"""
    # 创建基本目录结构
    (path / "app").mkdir(exist_ok=True)
    (path / "app" / "routes").mkdir(exist_ok=True)
    (path / "app" / "models").mkdir(exist_ok=True)
    (path / "app" / "services").mkdir(exist_ok=True)
    
    # 创建main.py
    main_content = f'''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="{name} API", version="0.1.0")

# CORS设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {{"message": "Welcome to {name} API"}}

@app.get("/health")
async def health():
    return {{"status": "healthy"}}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
    
    with open(path / "main.py", "w") as f:
        f.write(main_content)
    
    # 创建requirements.txt
    requirements_content = '''fastapi>=0.68.0
uvicorn>=0.15.0
pydantic>=1.8.0
'''
    
    with open(path / "requirements.txt", "w") as f:
        f.write(requirements_content)


def list_files(path: Path, pattern: str):
    """列出文件"""
    files = list(path.glob(pattern))
    
    if not files:
        display_info("文件列表", f"在 {path} 中未找到匹配 {pattern} 的文件")
        return
    
    table = Table(title=f"文件列表 - {path}")
    table.add_column("文件名", style="cyan")
    table.add_column("类型", style="green")
    table.add_column("大小", style="yellow")
    
    for file in files[:50]:  # 限制显示50个文件
        file_type = "目录" if file.is_dir() else "文件"
        size = f"{file.stat().st_size:,} bytes" if file.is_file() else "-"
        table.add_row(file.name, file_type, size)
    
    console.print(table)
    
    if len(files) > 50:
        display_info("提示", f"显示了前50个文件，共找到 {len(files)} 个文件")


def find_files(path: Path, pattern: str):
    """查找文件"""
    files = list(path.rglob(pattern))
    
    if not files:
        display_info("查找结果", f"在 {path} 中未找到匹配 {pattern} 的文件")
        return
    
    table = Table(title=f"查找结果 - {pattern}")
    table.add_column("文件路径", style="cyan")
    table.add_column("大小", style="green")
    
    for file in files[:50]:  # 限制显示50个文件
        size = f"{file.stat().st_size:,} bytes" if file.is_file() else "-"
        table.add_row(str(file.relative_to(path)), size)
    
    console.print(table)
    
    if len(files) > 50:
        display_info("提示", f"显示了前50个文件，共找到 {len(files)} 个文件")


def count_files(path: Path, pattern: str):
    """统计文件数量"""
    files = list(path.rglob(pattern))
    
    file_count = len([f for f in files if f.is_file()])
    dir_count = len([f for f in files if f.is_dir()])
    
    display_info("文件统计", f"在 {path} 中找到:\n- 文件: {file_count} 个\n- 目录: {dir_count} 个\n- 总计: {len(files)} 个")


def get_directory_size(path: Path):
    """获取目录大小"""
    total_size = 0
    file_count = 0
    
    for file in path.rglob("*"):
        if file.is_file():
            total_size += file.stat().st_size
            file_count += 1
    
    size_gb = total_size / (1024**3)
    size_mb = total_size / (1024**2)
    
    if size_gb >= 1:
        size_str = f"{size_gb:.2f} GB"
    else:
        size_str = f"{size_mb:.2f} MB"
    
    display_info("目录大小", f"{path}:\n- 总大小: {size_str}\n- 文件数: {file_count} 个")


# 设置默认命令
@app.callback()
def main():
    """SSF CLI - 一个功能强大的命令行工具"""
    pass 