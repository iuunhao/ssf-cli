#!/usr/bin/env python3
"""
测试命令注册
"""

import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from ssf_cli.commands import app
    print("✅ 成功导入commands模块")
    
    print(f"📋 注册的命令数量: {len(app.registered_commands)}")
    
    for i, cmd in enumerate(app.registered_commands):
        print(f"  {i+1}. {cmd.name} - {cmd.help}")
        
except Exception as e:
    print(f"❌ 导入失败: {e}")
    import traceback
    traceback.print_exc() 