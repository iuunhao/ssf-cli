#!/usr/bin/env python3
"""
快速测试脚本
用于验证SSF CLI的安装和代码修改
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    print(f"🐍 Python版本: {version.major}.{version.minor}.{version.micro}")
    if version >= (3, 8):
        print("✅ Python版本符合要求")
        return True
    else:
        print("❌ Python版本过低，需要3.8+")
        return False

def create_venv():
    """创建虚拟环境"""
    venv_dir = Path(".venv")
    if not venv_dir.exists():
        print("🔧 创建虚拟环境...")
        subprocess.run([sys.executable, "-m", "venv", ".venv"])
        print("✅ 虚拟环境创建完成")
    else:
        print("✅ 虚拟环境已存在")

def install_dependencies():
    """安装依赖"""
    print("📦 安装依赖...")
    
    # 获取pip路径
    if os.name == "nt":  # Windows
        pip_cmd = [".venv/Scripts/pip"]
    else:  # Unix/Linux/macOS
        pip_cmd = [".venv/bin/pip"]
    
    # 安装依赖
    subprocess.run(pip_cmd + ["install", "--upgrade", "pip"])
    subprocess.run(pip_cmd + ["install", "typer", "rich", "pydantic", "click", "requests"])
    print("✅ 依赖安装完成")

def install_dev_mode():
    """安装开发模式"""
    print("🔗 安装开发模式...")
    
    if os.name == "nt":  # Windows
        pip_cmd = [".venv/Scripts/pip"]
    else:  # Unix/Linux/macOS
        pip_cmd = [".venv/bin/pip"]
    
    result = subprocess.run(pip_cmd + ["install", "-e", "."], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ 开发模式安装成功")
        return True
    else:
        print(f"❌ 安装失败: {result.stderr}")
        return False

def test_cli():
    """测试CLI工具"""
    print("🧪 测试CLI工具...")
    
    if os.name == "nt":  # Windows
        python_cmd = [".venv/Scripts/python"]
    else:  # Unix/Linux/macOS
        python_cmd = [".venv/bin/python"]
    
    # 测试info命令
    result = subprocess.run(python_cmd + ["-m", "ssf_cli.main", "info"], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ CLI工具运行正常")
        if "测试修改生效" in result.stdout:
            print("✅ 代码修改已生效")
        else:
            print("⚠️  代码修改可能未生效")
        return True
    else:
        print(f"❌ CLI工具运行失败: {result.stderr}")
        return False

def main():
    """主函数"""
    print("🚀 SSF CLI 快速测试")
    print("=" * 50)
    
    # 检查Python版本
    if not check_python_version():
        return
    
    # 创建虚拟环境
    create_venv()
    
    # 安装依赖
    install_dependencies()
    
    # 安装开发模式
    if not install_dev_mode():
        return
    
    # 测试CLI工具
    if test_cli():
        print("\n🎉 所有测试通过！")
        print("\n📝 使用方法:")
        print("  source .venv/bin/activate")
        print("  ssf info")
        print("  ssf status")
    else:
        print("\n💥 测试失败，请检查错误信息")

if __name__ == "__main__":
    main() 