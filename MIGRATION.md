# SSF CLI 迁移指南

## 🚀 快速部署到新电脑

### 方法一：一键部署（推荐）

```bash
# 1. 克隆项目
git clone <your-repo-url> ssf-cli
cd ssf-cli

# 2. 运行部署脚本
chmod +x deploy.sh
./deploy.sh
```

### 方法二：手动部署

```bash
# 1. 克隆项目
git clone <your-repo-url> ssf-cli
cd ssf-cli

# 2. 检查Python版本
python3.10 --version  # 或 python3.11 --version

# 3. 创建虚拟环境
python3.10 -m venv .venv

# 4. 激活虚拟环境
source .venv/bin/activate

# 5. 安装依赖
pip install --upgrade pip
pip install typer rich pydantic click requests psutil

# 6. 安装开发模式
pip install -e .

# 7. 设置全局符号链接
mkdir -p ~/.local/bin
ln -sf $(pwd)/.venv/bin/ssf ~/.local/bin/ssf

# 8. 测试安装
ssf info
```

## 📋 系统要求

### 必需软件
- ✅ **Git** - 版本控制
- ✅ **Python 3.10+** - 运行环境
- ✅ **pip** - 包管理器

### 推荐软件
- ✅ **Homebrew** (macOS) - 包管理器
- ✅ **VS Code** - 代码编辑器
- ✅ **iTerm2** (macOS) - 终端

## 🔧 环境配置

### 1. 安装Python

#### macOS (推荐)
```bash
# 使用Homebrew安装
brew install python@3.10

# 或安装最新版本
brew install python@3.11
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.10 python3.10-venv python3.10-pip
```

#### Windows
```bash
# 下载并安装Python 3.10+ from python.org
# 或使用winget
winget install Python.Python.3.10
```

### 2. 配置PATH

将以下行添加到你的shell配置文件 (`~/.zshrc`, `~/.bashrc`, 或 `~/.bash_profile`):

```bash
export PATH="$HOME/.local/bin:$PATH"
```

然后重新加载配置：
```bash
source ~/.zshrc  # 或 source ~/.bashrc
```

## 🧪 验证安装

运行以下命令验证安装：

```bash
# 检查SSF CLI是否可用
ssf --help

# 测试基本功能
ssf info
ssf status
ssf system

# 测试项目创建
ssf create python --name test-project
rm -rf test-project

# 测试网络请求
ssf fetch https://httpbin.org/json

# 测试文件操作
ssf files list --path .
```

## 🔄 开发工作流

### 日常开发
```bash
# 1. 激活虚拟环境（可选，因为已全局可用）
source .venv/bin/activate

# 2. 修改代码
# 编辑 src/ssf_cli/commands.py 等文件

# 3. 立即测试（代码修改自动生效）
ssf info

# 4. 提交更改
git add .
git commit -m "feat: 新功能"
```

### 管理全局链接
```bash
# 检查状态
python setup_global_dev.py check

# 重新安装全局链接
python setup_global_dev.py install

# 测试功能
python setup_global_dev.py test

# 移除全局链接
python setup_global_dev.py remove
```

## 🛠️ 故障排除

### 问题1：命令未找到
```bash
# 检查符号链接
ls -la ~/.local/bin/ssf

# 重新创建符号链接
rm ~/.local/bin/ssf
ln -sf $(pwd)/.venv/bin/ssf ~/.local/bin/ssf
```

### 问题2：依赖冲突
```bash
# 重新创建虚拟环境
rm -rf .venv
python3.10 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 问题3：权限问题
```bash
# 确保脚本有执行权限
chmod +x deploy.sh
chmod +x setup_global_dev.py
```

### 问题4：Python版本问题
```bash
# 检查可用版本
python3.10 --version
python3.11 --version
python3 --version

# 使用特定版本
python3.10 -m venv .venv
```

## 📦 依赖管理

### 核心依赖
- `typer` - CLI框架
- `rich` - 终端美化
- `pydantic` - 数据验证
- `click` - CLI工具
- `requests` - HTTP请求
- `psutil` - 系统监控

### 开发依赖
- `black` - 代码格式化
- `isort` - 导入排序
- `flake8` - 代码检查

## 🔄 更新和维护

### 更新项目
```bash
# 拉取最新代码
git pull origin main

# 重新安装（如果需要）
pip install -e . --force-reinstall

# 更新依赖
pip install --upgrade typer rich pydantic click requests psutil
```

### 备份配置
```bash
# 备份配置文件
cp ~/.ssfrc ~/.ssfrc.backup

# 恢复配置
cp ~/.ssfrc.backup ~/.ssfrc
```

## 📞 获取帮助

### 内置帮助
```bash
ssf help                    # 显示帮助
ssf debug                   # 调试信息
ssf --help                  # 命令帮助
ssf create --help           # 子命令帮助
```

### 管理脚本帮助
```bash
python setup_global_dev.py  # 显示管理脚本帮助
```

## 🎯 最佳实践

1. **使用虚拟环境** - 避免依赖冲突
2. **定期更新** - 保持依赖最新
3. **备份配置** - 保存重要设置
4. **测试功能** - 确保所有命令正常
5. **版本控制** - 使用Git管理代码

---

**快速开始：**
```bash
git clone <your-repo-url> ssf-cli && cd ssf-cli && chmod +x deploy.sh && ./deploy.sh
``` 