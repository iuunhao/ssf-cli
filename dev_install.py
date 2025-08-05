#!/usr/bin/env python3
"""
开发模式安装脚本
用于本地调试SSF CLI
"""

import os
import sys
import subprocess
from pathlib import Path

def install_dev_mode():
    """安装开发模式"""
    print("🔧 正在安装SSF CLI开发模式...")
    
    # 获取当前目录
    current_dir = Path.cwd()
    print(f"📁 项目目录: {current_dir}")
    
    # 检查是否在正确的目录
    if not (current_dir / "pyproject.toml").exists():
        print("❌ 错误: 请在SSF CLI项目根目录运行此脚本")
        return False
    
    # 创建虚拟环境（可选）
    venv_dir = current_dir / ".venv"
    if not venv_dir.exists():
        print("🐍 创建虚拟环境...")
        subprocess.run([sys.executable, "-m", "venv", ".venv"])
    
    # 激活虚拟环境并安装
    if os.name == "nt":  # Windows
        activate_script = venv_dir / "Scripts" / "activate.bat"
        pip_cmd = [str(venv_dir / "Scripts" / "python.exe"), "-m", "pip"]
    else:  # Unix/Linux/macOS
        activate_script = venv_dir / "bin" / "activate"
        pip_cmd = [str(venv_dir / "bin" / "python"), "-m", "pip"]
    
    # 安装依赖
    print("📦 安装依赖...")
    subprocess.run(pip_cmd + ["install", "typer", "rich", "pydantic", "click"])
    
    # 安装开发模式
    print("🔗 安装开发模式...")
    result = subprocess.run(pip_cmd + ["install", "-e", "."], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ SSF CLI开发模式安装成功！")
        print("\n📝 使用方法:")
        print("  1. 激活虚拟环境:")
        if os.name == "nt":
            print("     .venv\\Scripts\\activate")
        else:
            print("     source .venv/bin/activate")
        print("  2. 运行命令:")
        print("     ssf info")
        print("     ssf debug")
        return True
    else:
        print(f"❌ 安装失败: {result.stderr}")
        return False

def create_dev_script():
    """创建开发脚本"""
    script_content = """#!/usr/bin/env python3
import sys
from pathlib import Path

# 添加项目路径到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

# 导入并运行主程序
from ssf_cli.main import main

if __name__ == "__main__":
    main()
"""
    
    script_path = Path("dev_ssf.py")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script_content)
    
    # 设置执行权限
    if os.name != "nt":
        os.chmod(script_path, 0o755)
    
    print(f"📜 创建开发脚本: {script_path}")
    print("💡 可以直接运行: python dev_ssf.py info")

if __name__ == "__main__":
    print("🚀 SSF CLI 开发模式安装器")
    print("=" * 50)
    
    if install_dev_mode():
        create_dev_script()
        print("\n🎉 安装完成！现在可以开始开发调试了。")
    else:
        print("\n💥 安装失败，请检查错误信息。") 