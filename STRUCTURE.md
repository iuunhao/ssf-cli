# SSF CLI 项目结构

## 目录结构

```
ssf-cli/
├── pyproject.toml          # 项目配置和依赖管理
├── README.md              # 项目文档
├── install.py             # 安装脚本
├── .gitignore            # Git忽略文件
├── .ssfrc                # 本地配置文件
├── PROJECT_SUMMARY.md    # 项目总结文档
├── STRUCTURE.md          # 项目结构文档（本文件）
└── src/
    └── ssf_cli/
        ├── __init__.py    # 包初始化
        ├── main.py        # 主入口文件
        ├── commands.py    # 命令实现
        ├── config.py      # 配置管理
        └── utils.py       # 工具函数
```

## 文件说明

### 根目录文件

- **pyproject.toml** - 项目配置文件，包含依赖管理和构建配置
- **README.md** - 项目说明文档，包含安装和使用指南
- **install.py** - 一键安装脚本，支持全局安装
- **.gitignore** - Git版本控制忽略文件配置
- **.ssfrc** - 本地配置文件（运行时生成）
- **PROJECT_SUMMARY.md** - 详细的项目功能总结
- **STRUCTURE.md** - 项目结构说明（本文件）

### 源代码文件

#### src/ssf_cli/__init__.py
- 包初始化文件
- 定义版本信息和作者信息

#### src/ssf_cli/main.py
- 主入口文件
- 收集当前执行目录
- 设置环境变量
- 启动Typer应用

#### src/ssf_cli/commands.py
- CLI命令实现
- 包含所有用户可用的命令
- 使用Typer框架构建

#### src/ssf_cli/config.py
- 配置管理模块
- 实现三层配置系统
- 配置加载、保存、显示功能

#### src/ssf_cli/utils.py
- 工具函数模块
- 路径收集、显示功能
- 环境检查和验证

## 已移除的文件

在项目清理过程中，以下文件已被移除：

- ~~install_simple.py~~ - 重命名为 install.py
- ~~install_global.py~~ - 功能合并到 install.py
- ~~test_project/~~ - 测试目录，已移除
- ~~.venv/~~ - 开发虚拟环境，已移除

## 标准命名规范

项目采用以下标准命名规范：

1. **Python包名**: `ssf_cli` (下划线分隔)
2. **安装脚本**: `install.py` (简洁明了)
3. **配置文件**: `.ssfrc` (点开头，项目名)
4. **文档文件**: 使用描述性名称，如 `README.md`, `PROJECT_SUMMARY.md`

## 项目特点

1. **简洁结构** - 只保留必要的文件
2. **标准命名** - 遵循Python和CLI工具的标准命名规范
3. **模块化设计** - 清晰的代码组织结构
4. **易于维护** - 减少冗余文件，提高可维护性 