# SSF CLI

一个功能强大的命令行工具，提供三层配置管理和全局安装功能。

## 功能特性

- 🔧 三层配置文件管理（内置配置、全局配置、本地配置）
- 🌍 全局安装，支持在任何目录执行
- 📁 自动收集当前执行目录路径
- 🚀 基于Typer构建，提供优秀的CLI体验
- 🧹 提供完整的卸载功能

## 系统要求

- **Python版本**: 3.8 - 3.12 (不支持Python 3.13及以上版本)
- **操作系统**: Windows, macOS, Linux
- **依赖**: Git (用于远程安装)

## 项目结构

```
ssf-cli/
├── pyproject.toml          # 项目配置和依赖管理
├── README.md              # 项目文档
├── install.py             # 本地安装脚本
├── install_curl.sh        # curl一键安装脚本
├── install_remote.py      # Python远程安装脚本
├── uninstall.sh           # 卸载脚本
├── .gitignore            # Git忽略文件
└── src/
    └── ssf_cli/
        ├── __init__.py    # 包初始化
        ├── main.py        # 主入口文件
        ├── commands.py    # 命令实现
        ├── config.py      # 配置管理
        └── utils.py       # 工具函数
```

## 安装

### 本地安装（推荐）

```bash
# 使用安装脚本（推荐）
python install.py

# 或者使用uv安装
uv pip install -e .

# 或者使用pip安装
pip install -e .
```

### 远程安装（从GitHub）

```bash
# 一键安装（推荐）
curl -fsSL https://raw.githubusercontent.com/iuunhao/ssf-cli/main/install_curl.sh | bash

# 或者使用Python脚本
curl -fsSL https://raw.githubusercontent.com/iuunhao/ssf-cli/main/install_remote.py | python3 -

# 或者手动下载后运行
python install_remote.py
```

## 卸载

如果需要卸载SSF CLI，可以使用以下方法：

```bash
# 使用卸载脚本（推荐）
curl -fsSL https://raw.githubusercontent.com/iuunhao/ssf-cli/main/uninstall.sh | bash

# 或者手动下载后运行
./uninstall.sh

# 强制卸载（跳过确认）
./uninstall.sh --force
```

### 开发环境安装

```bash
# 创建虚拟环境
uv venv

# 激活虚拟环境
source .venv/bin/activate

# 安装依赖
uv pip install -e .
```



## 使用方法

安装完成后，您可以在任何地方使用`ssf`命令：

```bash
# 查看帮助
ssf --help

# 查看版本
ssf version

# 查看系统信息
ssf info

# 查看当前配置
ssf config show

# 查看当前工作目录
ssf pwd

# 查看SSF CLI状态
ssf status
```

## 配置管理

SSF CLI支持三层配置：

1. **内置配置** - CLI工具内置的默认配置
2. **全局配置** - 用户根目录的`.ssfrc`文件
3. **本地配置** - 当前执行目录的`.ssfrc`文件

配置优先级：本地配置 > 全局配置 > 内置配置

## 开发

```bash
# 安装开发依赖
uv pip install -e ".[dev]"

# 格式化代码
black src/
isort src/

# 检查代码质量
flake8 src/
```

## 许可证

MIT License 