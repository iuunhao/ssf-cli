#!/usr/bin/env python3
"""测试备份功能"""

import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent / "ssf-cli" / "src"))

from ssf_cli.config import SSFConfig
from ssf_cli.scripts.base import BaseScript

def test_backup():
    """测试备份功能"""
    # 创建配置
    config = SSFConfig()
    
    # 创建脚本实例
    script = BaseScript(config, Path.cwd())
    
    # 创建测试文件
    test_file = Path("test_backup_file.txt")
    test_file.write_text("test content")
    
    print(f"创建测试文件: {test_file}")
    print(f"文件存在: {test_file.exists()}")
    
    # 测试备份
    try:
        backup_path = script.backup_file(test_file)
        print(f"备份成功: {backup_path}")
        print(f"备份文件存在: {backup_path.exists()}")
        
        # 检查备份目录
        backup_dir = Path("./backup")
        print(f"备份目录存在: {backup_dir.exists()}")
        if backup_dir.exists():
            print(f"备份目录内容: {list(backup_dir.iterdir())}")
            
    except Exception as e:
        print(f"备份失败: {e}")
    
    # 清理
    if test_file.exists():
        test_file.unlink()

if __name__ == "__main__":
    test_backup() 