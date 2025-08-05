#!/usr/bin/env python3
"""
SSF CLI 简单安装脚本
使用虚拟环境方式安装，避免系统Python版本冲突
"""

import os
import sys
import subprocess
import shutil
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
        print(f"当前版本: {sys.version}")
        return False
    if sys.version_info >= (3, 13):
        print("❌ 错误: Python 3.13及以上版本存在兼容性问题")
        print(f"当前版本: {sys.version}")
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
                # 解析版本号
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
    print("💡 请安装Python 3.8-3.12版本")
    return None

def create_global_venv():
    """创建全局虚拟环境"""
    print("🔧 创建全局虚拟环境...")
    
    # 查找兼容的Python版本
    python_cmd = find_compatible_python()
    if not python_cmd:
        return None
    
    # 全局虚拟环境路径
    global_venv = Path.home() / ".ssf_cli_venv"
    
    try:
        # 如果已存在，删除旧的
        if global_venv.exists():
            shutil.rmtree(global_venv)
        
        # 使用兼容的Python版本创建虚拟环境
        subprocess.run([python_cmd, "-m", "venv", str(global_venv)], check=True)
        
        print(f"✅ 虚拟环境创建成功: {global_venv}")
        return global_venv
        
    except Exception as e:
        print(f"❌ 创建虚拟环境失败: {e}")
        return None

def install_in_venv(venv_path):
    """在虚拟环境中安装SSF CLI"""
    print("🔧 在虚拟环境中安装SSF CLI...")
    
    # 获取pip路径
    if os.name == 'nt':  # Windows
        pip_cmd = str(venv_path / "Scripts" / "pip")
    else:  # Unix/Linux/macOS
        pip_cmd = str(venv_path / "bin" / "pip")
    
    try:
        # 安装依赖（使用信任的源）
        subprocess.run([pip_cmd, "install", "--trusted-host", "pypi.org", "--trusted-host", "pypi.python.org", "--trusted-host", "files.pythonhosted.org", "typer", "rich", "pydantic"], check=True)
        
        # 安装SSF CLI（使用信任的源）
        result = subprocess.run([pip_cmd, "install", "--trusted-host", "pypi.org", "--trusted-host", "pypi.python.org", "--trusted-host", "files.pythonhosted.org", "-e", "."], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ SSF CLI安装成功！")
            return True
        else:
            print(f"❌ 安装失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 安装过程中出现错误: {e}")
        return False

def create_ssf_script(venv_path):
    """创建ssf脚本"""
    print("🔧 创建ssf脚本...")
    
    # 获取Python路径
    if os.name == 'nt':  # Windows
        python_cmd = str(venv_path / "Scripts" / "python")
    else:  # Unix/Linux/macOS
        python_cmd = str(venv_path / "bin" / "python")
    
    # 创建脚本内容
    script_content = f"""#!/bin/bash
# SSF CLI 启动脚本
{python_cmd} -m ssf_cli.main "$@"
"""
    
    # 写入脚本文件
    script_path = Path.home() / ".local" / "bin" / "ssf"
    script_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    # 设置执行权限
    os.chmod(script_path, 0o755)
    
    print(f"✅ 脚本创建成功: {script_path}")
    return script_path

def add_to_path():
    """添加到PATH"""
    print("🔧 配置PATH...")
    
    local_bin = Path.home() / ".local" / "bin"
    
    # 检查shell配置文件
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
            else:
                print(f"✅ PATH已在 {config} 中配置")

def verify_installation(venv_path):
    """验证安装"""
    print("🔍 验证安装...")
    
    try:
        # 获取Python路径
        if os.name == 'nt':  # Windows
            python_cmd = str(venv_path / "Scripts" / "python")
        else:  # Unix/Linux/macOS
            python_cmd = str(venv_path / "bin" / "python")
        
        # 测试导入
        result = subprocess.run([python_cmd, "-c", "import ssf_cli; print('✅ 模块导入成功')"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print(result.stdout.strip())
            return True
        else:
            print("❌ 模块导入失败")
            return False
            
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return False

def main():
    """主函数"""
    print_banner()
    
    # 检查Python版本
    if not check_python_version():
        sys.exit(1)
    
    # 检查是否在项目根目录
    if not Path("pyproject.toml").exists():
        print("❌ 错误: 请在项目根目录运行此脚本")
        sys.exit(1)
    
    # 创建虚拟环境
    venv_path = create_global_venv()
    if not venv_path:
        sys.exit(1)
    
    # 安装SSF CLI
    if not install_in_venv(venv_path):
        sys.exit(1)
    
    # 创建脚本
    script_path = create_ssf_script(venv_path)
    
    # 配置PATH
    add_to_path()
    
    # 验证安装
    if verify_installation(venv_path):
        print("\n🎉 安装完成！")
        print("现在您可以在任何地方使用 'ssf' 命令")
        print("\n示例命令:")
        print("  ssf --help          # 查看帮助")
        print("  ssf version         # 查看版本")
        print("  ssf info            # 查看系统信息")
        print("  ssf config show     # 查看配置")
        print("\n💡 如果命令不可用，请重新打开终端或运行:")
        print("  source ~/.bashrc  # 或 source ~/.zshrc")
    else:
        print("❌ 安装验证失败")
        sys.exit(1)

if __name__ == "__main__":
    main() 