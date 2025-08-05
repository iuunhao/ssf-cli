#!/usr/bin/env python3
"""
SSF CLI 环境检查脚本
用于验证开发环境是否正确设置
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    print("🐍 检查Python版本...")
    version = sys.version_info
    print(f"   当前版本: {version.major}.{version.minor}.{version.micro}")
    
    if version >= (3, 8):
        print("   ✅ Python版本符合要求")
        return True
    else:
        print("   ❌ Python版本过低，需要3.8+")
        return False

def check_dependencies():
    """检查依赖"""
    print("📦 检查依赖...")
    
    dependencies = [
        "typer", "rich", "pydantic", "click", "requests", "psutil"
    ]
    
    missing = []
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"   ✅ {dep}")
        except ImportError:
            print(f"   ❌ {dep} - 未安装")
            missing.append(dep)
    
    if missing:
        print(f"   缺少依赖: {', '.join(missing)}")
        print("   请运行: pip install " + " ".join(missing))
        return False
    
    return True

def check_ssf_installation():
    """检查SSF CLI安装"""
    print("🔧 检查SSF CLI安装...")
    
    try:
        result = subprocess.run(["ssf", "--help"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✅ SSF CLI 已安装")
            return True
        else:
            print("   ❌ SSF CLI 安装有问题")
            return False
    except FileNotFoundError:
        print("   ❌ SSF CLI 未找到")
        return False

def check_global_link():
    """检查全局符号链接"""
    print("🔗 检查全局符号链接...")
    
    global_ssf = Path.home() / ".local" / "bin" / "ssf"
    
    if global_ssf.exists():
        if global_ssf.is_symlink():
            target = global_ssf.resolve()
            print(f"   ✅ 符号链接存在: {global_ssf} -> {target}")
            return True
        else:
            print("   ⚠️  全局位置存在文件，但不是符号链接")
            return False
    else:
        print("   ❌ 全局符号链接不存在")
        return False

def check_path():
    """检查PATH设置"""
    print("🛣️  检查PATH设置...")
    
    path = os.environ.get("PATH", "")
    local_bin = str(Path.home() / ".local" / "bin")
    
    if local_bin in path:
        print("   ✅ PATH包含 ~/.local/bin")
        return True
    else:
        print("   ⚠️  PATH中未包含 ~/.local/bin")
        print("   请将以下行添加到shell配置文件:")
        print(f"   export PATH=\"{local_bin}:\$PATH\"")
        return False

def test_commands():
    """测试命令"""
    print("🧪 测试命令...")
    
    commands = [
        ("info", "系统信息"),
        ("status", "状态检查"),
        ("system", "系统监控"),
        ("create python --name test", "项目创建"),
        ("fetch https://httpbin.org/json", "网络请求"),
        ("files list --path .", "文件操作")
    ]
    
    success_count = 0
    for cmd, desc in commands:
        try:
            # 对于需要参数的命令，只测试帮助
            if "create" in cmd or "fetch" in cmd or "files" in cmd:
                test_cmd = cmd.split()[0] + " --help"
            else:
                test_cmd = cmd
            
            result = subprocess.run(["ssf"] + test_cmd.split(), 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"   ✅ {desc}")
                success_count += 1
            else:
                print(f"   ❌ {desc}")
        except Exception as e:
            print(f"   ❌ {desc}: {e}")
    
    return success_count == len(commands)

def check_development_mode():
    """检查开发模式"""
    print("🔍 检查开发模式...")
    
    try:
        # 检查是否在虚拟环境中
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            print("   ✅ 在虚拟环境中")
        else:
            print("   ⚠️  不在虚拟环境中")
        
        # 检查源代码路径
        project_root = Path.cwd()
        src_path = project_root / "src" / "ssf_cli"
        
        if src_path.exists():
            print(f"   ✅ 源代码路径存在: {src_path}")
            return True
        else:
            print("   ❌ 源代码路径不存在")
            return False
            
    except Exception as e:
        print(f"   ❌ 检查失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 SSF CLI 环境检查")
    print("=" * 50)
    
    checks = [
        ("Python版本", check_python_version),
        ("依赖检查", check_dependencies),
        ("SSF CLI安装", check_ssf_installation),
        ("全局符号链接", check_global_link),
        ("PATH设置", check_path),
        ("开发模式", check_development_mode),
        ("命令测试", test_commands)
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n{name}:")
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"   ❌ 检查失败: {e}")
            results.append((name, False))
    
    # 总结
    print("\n" + "=" * 50)
    print("📊 检查结果:")
    
    passed = 0
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   {name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{len(results)} 项检查通过")
    
    if passed == len(results):
        print("\n🎉 环境检查全部通过！SSF CLI 可以正常使用。")
        print("\n💡 使用提示:")
        print("   ssf info          # 显示系统信息")
        print("   ssf create python --name my-project  # 创建项目")
        print("   ssf fetch https://httpbin.org/json   # 网络请求")
        print("   ssf files list --path .              # 文件操作")
        print("   ssf system                           # 系统监控")
    else:
        print(f"\n⚠️  有 {len(results) - passed} 项检查未通过，请参考 MIGRATION.md 进行修复。")
        print("\n🔧 快速修复:")
        print("   ./deploy.sh                          # 重新部署")
        print("   python setup_global_dev.py install   # 重新安装全局链接")

if __name__ == "__main__":
    main() 