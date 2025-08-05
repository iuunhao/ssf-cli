#!/usr/bin/env python3
import sys
from pathlib import Path

# 添加项目路径到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

# 导入并运行主程序
from ssf_cli.main import main

if __name__ == "__main__":
    main()
