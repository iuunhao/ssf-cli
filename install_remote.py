#!/usr/bin/env python3
"""
SSF CLI 远程安装脚本
支持从GitHub直接安装SSF CLI
"""

import os
import sys
import subprocess
import shutil
import tempfile
from pathlib import Path

def print_banner():
    """打印横幅"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                        SSF CLI                               ║
    ║                 Simple & Smart Framework                     ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        print("❌ 错误: 需要Python 3.8或更高版本")
        return False
    if sys.version_info >= (3, 13):
        print("❌ 错误: Python 3.13及以上版本存在兼容性问题")
        print("💡 建议使用Python 3.8-3.12版本")
        return False
    print(f"✅ Python版本检查通过: {sys.version}")
    return True

def find_compatible_python():
    """查找兼容的Python版本"""
    python_versions = [
        "python3.12", "python3.11", "python3.10", "python3.9", "python3.8",
        "python3", "python"
    ]
    
    for python_cmd in python_versions:
        try:
            result = subprocess.run([python_cmd, "--version"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                version_str = result.stdout.strip()
                import re
                version_match = re.search(r'Python (\d+)\.(\d+)', version_str)
                if version_match:
                    major, minor = int(version_match.group(1)), int(version_match.group(2))
                    if (3, 8) <= (major, minor) < (3, 13):
                        print(f"✅ 找到兼容的Python版本: {version_str}")
                        return python_cmd
        except FileNotFoundError:
            continue
    
    print("❌ 未找到兼容的Python版本")
    return None

def check_git():
    """检查git是否可用"""
    try:
        result = subprocess.run(["git", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Git可用: {result.stdout.strip()}")
            return True
        else:
            print("❌ Git不可用")
            return False
    except FileNotFoundError:
        print("❌ Git未安装")
        return False

def clone_and_install(repo_url):
    """克隆并安装"""
    print(f"🔧 克隆仓库: {repo_url}")
    
    # 创建项目目录
    project_dir = Path.home() / "ssf-cli"
    print(f"🔧 创建项目目录: {project_dir}")
    
    # 如果目录已存在，删除旧的
    if project_dir.exists():
        print("🧹 清理旧的项目目录...")
        shutil.rmtree(project_dir)
    
    # 克隆仓库
    try:
        subprocess.run(["git", "clone", "--depth", "1", repo_url, str(project_dir)], 
                     check=True, capture_output=True)
        print("✅ 仓库克隆成功")
    except subprocess.CalledProcessError as e:
        print(f"❌ 克隆失败: {e}")
        return False
    
    # 检查pyproject.toml
    if not (project_dir / "pyproject.toml").exists():
        print("❌ 未找到pyproject.toml文件")
        return False
        
        # 查找兼容的Python版本
        python_cmd = find_compatible_python()
        if not python_cmd:
            return False
        
        # 创建虚拟环境
        global_venv = Path.home() / ".ssf_cli_venv"
        if global_venv.exists():
            shutil.rmtree(global_venv)
        
        subprocess.run([python_cmd, "-m", "venv", str(global_venv)], check=True)
        
        # 安装依赖
        if os.name == 'nt':
            pip_cmd = str(global_venv / "Scripts" / "pip")
        else:
            pip_cmd = str(global_venv / "bin" / "pip")
        
        subprocess.run([pip_cmd, "install", "--trusted-host", "pypi.org", "--trusted-host", "pypi.python.org", "--trusted-host", "files.pythonhosted.org", "typer", "rich", "pydantic"], check=True)
        
        # 安装SSF CLI
        result = subprocess.run([pip_cmd, "install", "-e", "."], 
                              cwd=str(project_dir), capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ SSF CLI安装成功！")
            return True
        else:
            print(f"❌ 安装失败: {result.stderr}")
            return False

def create_ssf_script():
    """创建ssf脚本"""
    global_venv = Path.home() / ".ssf_cli_venv"
    if os.name == 'nt':
        python_cmd = str(global_venv / "Scripts" / "python")
    else:
        python_cmd = str(global_venv / "bin" / "python")
    
    script_content = f"""#!/bin/bash
# SSF CLI 启动脚本
{python_cmd} -m ssf_cli.main "$@"
"""
    
    script_path = Path.home() / ".local" / "bin" / "ssf"
    script_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    os.chmod(script_path, 0o755)
    print(f"✅ 脚本创建成功: {script_path}")

def add_to_path():
    """添加到PATH"""
    local_bin = Path.home() / ".local" / "bin"
    
    shell_configs = [
        Path.home() / ".bashrc",
        Path.home() / ".zshrc",
        Path.home() / ".bash_profile",
    ]
    
    for config in shell_configs:
        if config.exists():
            with open(config, 'r') as f:
                content = f.read()
            
            if str(local_bin) not in content:
                with open(config, 'a') as f:
                    f.write(f'\n# SSF CLI PATH\nexport PATH="$HOME/.local/bin:$PATH"\n')
                print(f"✅ 已添加到 {config}")

def main():
    """主函数"""
    print_banner()
    
    if not check_python_version():
        sys.exit(1)
    
    if not check_git():
        sys.exit(1)
    
    repo_url = input("请输入GitHub仓库URL (默认: https://github.com/iuunhao/ssf-cli.git): ").strip()
    if not repo_url:
        repo_url = "https://github.com/iuunhao/ssf-cli.git"
    
    if clone_and_install(repo_url):
        create_ssf_script()
        add_to_path()
        print("\n🎉 安装完成！")
        print("现在您可以在任何地方使用 'ssf' 命令")
    else:
        print("❌ 安装失败")
        sys.exit(1)

if __name__ == "__main__":
    main() 