#!/usr/bin/env python3
"""
SSF CLI 开发模式全局安装管理脚本
"""

import os
import sys
import subprocess
from pathlib import Path

def get_project_root():
    """获取项目根目录"""
    return Path(__file__).parent

def get_venv_path():
    """获取虚拟环境路径"""
    project_root = get_project_root()
    return project_root / ".venv"

def get_ssf_bin_path():
    """获取ssf可执行文件路径"""
    venv_path = get_venv_path()
    if os.name == "nt":  # Windows
        return venv_path / "Scripts" / "ssf.exe"
    else:  # Unix/Linux/macOS
        return venv_path / "bin" / "ssf"

def get_global_bin_path():
    """获取全局bin目录路径"""
    return Path.home() / ".local" / "bin"

def create_symlink():
    """创建符号链接"""
    ssf_bin = get_ssf_bin_path()
    global_bin = get_global_bin_path()
    global_ssf = global_bin / "ssf"
    
    # 确保全局bin目录存在
    global_bin.mkdir(parents=True, exist_ok=True)
    
    # 检查ssf是否存在于虚拟环境中
    if not ssf_bin.exists():
        print(f"❌ 错误: 虚拟环境中未找到ssf命令: {ssf_bin}")
        print("请先运行: source .venv/bin/activate && pip install -e .")
        return False
    
    # 创建符号链接
    try:
        if global_ssf.exists():
            global_ssf.unlink()
        
        global_ssf.symlink_to(ssf_bin)
        print(f"✅ 符号链接创建成功: {global_ssf} -> {ssf_bin}")
        return True
    except Exception as e:
        print(f"❌ 创建符号链接失败: {e}")
        return False

def remove_symlink():
    """移除符号链接"""
    global_ssf = get_global_bin_path() / "ssf"
    
    if global_ssf.exists():
        try:
            global_ssf.unlink()
            print(f"✅ 符号链接已移除: {global_ssf}")
            return True
        except Exception as e:
            print(f"❌ 移除符号链接失败: {e}")
            return False
    else:
        print("ℹ️  符号链接不存在")
        return True

def check_symlink():
    """检查符号链接状态"""
    global_ssf = get_global_bin_path() / "ssf"
    ssf_bin = get_ssf_bin_path()
    
    print("🔍 检查符号链接状态...")
    print(f"  虚拟环境ssf: {ssf_bin}")
    print(f"  全局符号链接: {global_ssf}")
    
    if global_ssf.exists():
        if global_ssf.is_symlink():
            target = global_ssf.resolve()
            print(f"  ✅ 符号链接存在，指向: {target}")
            if target == ssf_bin:
                print("  ✅ 符号链接正确")
                return True
            else:
                print("  ⚠️  符号链接指向错误位置")
                return False
        else:
            print("  ❌ 全局位置存在文件，但不是符号链接")
            return False
    else:
        print("  ❌ 符号链接不存在")
        return False

def test_global_usage():
    """测试全局使用"""
    print("🧪 测试全局使用...")
    
    # 切换到其他目录测试
    test_dir = Path("/tmp")
    if not test_dir.exists():
        test_dir = Path.home()
    
    try:
        result = subprocess.run(
            ["ssf", "info"], 
            capture_output=True, 
            text=True, 
            cwd=test_dir
        )
        
        if result.returncode == 0:
            print("✅ 全局ssf命令工作正常")
            if "测试修改生效" in result.stdout:
                print("✅ 代码修改已生效（开发模式）")
            return True
        else:
            print(f"❌ 全局ssf命令失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 SSF CLI 开发模式全局安装管理")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python setup_global_dev.py install    # 安装全局符号链接")
        print("  python setup_global_dev.py remove     # 移除全局符号链接")
        print("  python setup_global_dev.py check      # 检查符号链接状态")
        print("  python setup_global_dev.py test       # 测试全局使用")
        return
    
    command = sys.argv[1]
    
    if command == "install":
        print("🔧 安装全局符号链接...")
        if create_symlink():
            print("\n📝 安装完成！现在可以在任何目录使用 'ssf' 命令")
            print("💡 代码修改会自动生效（开发模式）")
        else:
            print("\n💥 安装失败")
    
    elif command == "remove":
        print("🗑️  移除全局符号链接...")
        if remove_symlink():
            print("\n✅ 移除完成")
        else:
            print("\n💥 移除失败")
    
    elif command == "check":
        check_symlink()
    
    elif command == "test":
        if check_symlink():
            test_global_usage()
        else:
            print("❌ 符号链接状态异常，请先运行 install")
    
    else:
        print(f"❌ 未知命令: {command}")

if __name__ == "__main__":
    main() 