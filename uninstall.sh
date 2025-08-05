#!/bin/bash
# SSF CLI 卸载脚本
# 完全卸载SSF CLI及其相关文件

set -e

echo "🧹 开始卸载 SSF CLI..."

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查是否以root权限运行
if [ "$EUID" -eq 0 ]; then
    echo -e "${YELLOW}⚠️  警告: 检测到root权限，将卸载系统级安装${NC}"
fi

# 卸载函数
uninstall_ssf() {
    echo "🔍 查找SSF CLI安装位置..."
    
    # 1. 删除虚拟环境
    venv_path="$HOME/.ssf_cli_venv"
    if [ -d "$venv_path" ]; then
        echo "🗑️  删除虚拟环境: $venv_path"
        rm -rf "$venv_path"
        echo -e "${GREEN}✅ 虚拟环境已删除${NC}"
    else
        echo "ℹ️  未找到虚拟环境"
    fi
    
    # 2. 删除用户级脚本
    user_script="$HOME/.local/bin/ssf"
    if [ -f "$user_script" ]; then
        echo "🗑️  删除用户级脚本: $user_script"
        rm -f "$user_script"
        echo -e "${GREEN}✅ 用户级脚本已删除${NC}"
    else
        echo "ℹ️  未找到用户级脚本"
    fi
    
    # 3. 删除系统级脚本（需要root权限）
    system_scripts=(
        "/usr/local/bin/ssf"
        "/usr/bin/ssf"
        "/Library/Frameworks/Python.framework/Versions/*/bin/ssf"
    )
    
    for script in "${system_scripts[@]}"; do
        for file in $script; do
            if [ -f "$file" ]; then
                echo "🗑️  删除系统级脚本: $file"
                if [ "$EUID" -eq 0 ]; then
                    rm -f "$file"
                    echo -e "${GREEN}✅ 系统级脚本已删除${NC}"
                else
                    echo -e "${YELLOW}⚠️  需要root权限删除: $file${NC}"
                    echo "💡 请运行: sudo rm -f $file"
                fi
            fi
        done
    done
    
    # 4. 清理项目目录
    project_dir="$HOME/ssf-cli"
    if [ -d "$project_dir" ]; then
        echo "🗑️  删除项目目录: $project_dir"
        rm -rf "$project_dir"
        echo -e "${GREEN}✅ 项目目录已删除${NC}"
    fi
    
    # 5. 清理配置文件
    config_files=(
        "$HOME/.ssfrc"
        "$HOME/Desktop/code/ssfpro/ssf-cli/.ssfrc"
    )
    
    for config in "${config_files[@]}"; do
        if [ -f "$config" ]; then
            echo "🗑️  删除配置文件: $config"
            rm -f "$config"
            echo -e "${GREEN}✅ 配置文件已删除${NC}"
        fi
    done
    
    # 5. 清理PATH配置
    echo "🔧 清理PATH配置..."
    shell_configs=("$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.bash_profile")
    
    for config in "${shell_configs[@]}"; do
        if [ -f "$config" ]; then
            # 备份原文件
            backup_file="${config}.backup.$(date +%Y%m%d_%H%M%S)"
            cp "$config" "$backup_file"
            
            # 移除SSF CLI相关的PATH配置
            if grep -q "SSF CLI PATH" "$config"; then
                echo "🗑️  清理PATH配置: $config"
                # 删除包含SSF CLI PATH的行
                sed -i.bak '/# SSF CLI PATH/d' "$config"
                sed -i.bak '/export PATH.*\.local\/bin/d' "$config"
                echo -e "${GREEN}✅ PATH配置已清理${NC}"
            fi
        fi
    done
    
    # 6. 检查并清理pip安装
    echo "🔍 检查pip安装..."
    if command -v pip &> /dev/null; then
        if pip show ssf-cli &> /dev/null; then
            echo "🗑️  卸载pip安装的ssf-cli..."
            pip uninstall -y ssf-cli
            echo -e "${GREEN}✅ pip安装已卸载${NC}"
        fi
    fi
    
    # 7. 检查并清理uv安装
    echo "🔍 检查uv安装..."
    if command -v uv &> /dev/null; then
        if uv pip list | grep -q ssf-cli; then
            echo "🗑️  卸载uv安装的ssf-cli..."
            uv pip uninstall ssf-cli
            echo -e "${GREEN}✅ uv安装已卸载${NC}"
        fi
    fi
}

# 确认卸载
confirm_uninstall() {
    echo ""
    echo -e "${YELLOW}⚠️  确认卸载SSF CLI吗？${NC}"
    echo "这将删除以下内容："
    echo "  - 虚拟环境 (~/.ssf_cli_venv)"
    echo "  - 可执行脚本 (~/.local/bin/ssf)"
    echo "  - 配置文件 (.ssfrc)"
    echo "  - PATH配置"
    echo ""
    read -p "请输入 'yes' 确认卸载: " confirm
    
    if [ "$confirm" = "yes" ]; then
        return 0
    else
        echo "❌ 取消卸载"
        exit 0
    fi
}

# 验证卸载结果
verify_uninstall() {
    echo ""
    echo "🔍 验证卸载结果..."
    
    # 检查虚拟环境
    if [ -d "$HOME/.ssf_cli_venv" ]; then
        echo -e "${RED}❌ 虚拟环境仍然存在${NC}"
    else
        echo -e "${GREEN}✅ 虚拟环境已删除${NC}"
    fi
    
    # 检查脚本
    if command -v ssf &> /dev/null; then
        echo -e "${RED}❌ ssf命令仍然可用: $(which ssf)${NC}"
    else
        echo -e "${GREEN}✅ ssf命令已删除${NC}"
    fi
    
    # 检查项目目录
    if [ -d "$HOME/ssf-cli" ]; then
        echo -e "${RED}❌ 项目目录仍然存在${NC}"
    else
        echo -e "${GREEN}✅ 项目目录已删除${NC}"
    fi
    
    # 检查配置文件
    if [ -f "$HOME/.ssfrc" ]; then
        echo -e "${RED}❌ 配置文件仍然存在${NC}"
    else
        echo -e "${GREEN}✅ 配置文件已删除${NC}"
    fi
}

# 显示帮助信息
show_help() {
    echo "SSF CLI 卸载脚本"
    echo ""
    echo "用法:"
    echo "  $0          # 交互式卸载"
    echo "  $0 --force  # 强制卸载（跳过确认）"
    echo "  $0 --help   # 显示此帮助信息"
    echo ""
    echo "选项:"
    echo "  --force     跳过确认提示"
    echo "  --help      显示帮助信息"
    echo ""
    echo "注意:"
    echo "  - 卸载前会自动备份shell配置文件"
    echo "  - 系统级安装需要root权限"
    echo "  - 建议在卸载前备份重要配置"
}

# 主函数
main() {
    case "${1:-}" in
        --help|-h)
            show_help
            exit 0
            ;;
        --force|-f)
            echo "🔧 强制卸载模式"
            ;;
        "")
            echo "🧹 SSF CLI 卸载工具"
            confirm_uninstall
            ;;
        *)
            echo "❌ 未知参数: $1"
            show_help
            exit 1
            ;;
    esac
    
    uninstall_ssf
    verify_uninstall
    
    echo ""
    echo -e "${GREEN}🎉 卸载完成！${NC}"
    echo ""
    echo "💡 提示:"
    echo "  - 如果ssf命令仍然可用，请重新打开终端"
    echo "  - 如果遇到权限问题，请使用sudo运行"
    echo "  - 备份文件保存在 ~/.bashrc.backup.* 等位置"
}

# 运行主函数
main "$@" 