#!/bin/bash
# SSF CLI 一键安装脚本
# 用于从GitHub直接安装SSF CLI

set -e

echo "🚀 开始安装 SSF CLI..."

# 检查Python版本
python_version=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
major=$(echo $python_version | cut -d. -f1)
minor=$(echo $python_version | cut -d. -f2)

if [ "$major" -lt 3 ] || ([ "$major" -eq 3 ] && [ "$minor" -lt 8 ]); then
    echo "❌ 错误: 需要Python 3.8或更高版本"
    echo "当前版本: Python $python_version"
    exit 1
fi

if [ "$major" -eq 3 ] && [ "$minor" -ge 13 ]; then
    echo "❌ 错误: Python 3.13及以上版本存在兼容性问题"
    echo "当前版本: Python $python_version"
    echo "💡 建议使用Python 3.8-3.12版本"
    exit 1
fi

echo "✅ Python版本检查通过: Python $python_version"

# 检查Git
if ! command -v git &> /dev/null; then
    echo "❌ Git未安装"
    echo "💡 请先安装Git: https://git-scm.com/"
    exit 1
fi

echo "✅ Git可用: $(git --version)"

# 创建项目目录
project_dir="$HOME/ssf-cli"
echo "🔧 创建项目目录: $project_dir"

# 如果目录已存在，删除旧的
if [ -d "$project_dir" ]; then
    echo "🧹 清理旧的项目目录..."
    rm -rf "$project_dir"
fi

# 克隆仓库
repo_url="https://github.com/iuunhao/ssf-cli.git"
echo "🔧 克隆仓库: $repo_url"

if git clone --depth 1 "$repo_url" "$project_dir"; then
    echo "✅ 仓库克隆成功"
else
    echo "❌ 克隆失败"
    exit 1
fi

# 检查pyproject.toml
if [ ! -f "$project_dir/pyproject.toml" ]; then
    echo "❌ 未找到pyproject.toml文件"
    exit 1
fi

# 创建虚拟环境
venv_path="$HOME/.ssf_cli_venv"
if [ -d "$venv_path" ]; then
    echo "🧹 清理旧的虚拟环境..."
    rm -rf "$venv_path"
fi

echo "🔧 创建虚拟环境..."
python3 -m venv "$venv_path"

# 激活虚拟环境
source "$venv_path/bin/activate"

# 升级pip
echo "🔧 升级pip..."
pip install --upgrade pip --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org

# 安装依赖
echo "🔧 安装依赖..."
pip install typer rich pydantic --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org

# 安装SSF CLI
echo "🔧 安装SSF CLI..."
cd "$project_dir"
pip install -e . --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org

# 创建ssf脚本
echo "🔧 创建ssf脚本..."
script_path="$HOME/.local/bin/ssf"
mkdir -p "$(dirname "$script_path")"

cat > "$script_path" << EOF
#!/bin/bash
# SSF CLI 启动脚本
"$venv_path/bin/python" -m ssf_cli.main "\$@"
EOF

chmod +x "$script_path"
echo "✅ 脚本创建成功: $script_path"

# 添加到PATH
echo "🔧 配置PATH..."
shell_configs=("$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.bash_profile")

for config in "${shell_configs[@]}"; do
    if [ -f "$config" ]; then
        if ! grep -q "\.local/bin" "$config"; then
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$config"
            echo "✅ 已添加到 $config"
        fi
    fi
done

echo ""
echo "🎉 安装完成！"
echo "现在您可以在任何地方使用 'ssf' 命令"
echo ""
echo "示例命令:"
echo "  ssf --help          # 查看帮助"
echo "  ssf version         # 查看版本"
echo "  ssf info            # 查看系统信息"
echo "  ssf config show     # 查看配置"
echo ""
echo "💡 如果命令不可用，请重新打开终端或运行:"
echo "  source ~/.bashrc  # 或 source ~/.zshrc" 