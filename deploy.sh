#!/bin/bash
"""
SSF CLI 快速部署脚本
用于在新电脑上快速设置开发环境
"""

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 检查命令是否存在
check_command() {
    if command -v $1 &> /dev/null; then
        print_success "$1 已安装"
        return 0
    else
        print_error "$1 未安装"
        return 1
    fi
}

# 检查Python版本
check_python_version() {
    print_info "检查Python版本..."
    
    if command -v python3.10 &> /dev/null; then
        PYTHON_CMD="python3.10"
        print_success "找到 Python 3.10"
    elif command -v python3.11 &> /dev/null; then
        PYTHON_CMD="python3.11"
        print_success "找到 Python 3.11"
    elif command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
        print_success "找到 Python 3"
    else
        print_error "未找到合适的Python版本"
        print_info "请安装Python 3.10或更高版本"
        exit 1
    fi
    
    # 检查版本
    VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
    print_info "Python版本: $VERSION"
}

# 安装依赖
install_dependencies() {
    print_info "安装Python依赖..."
    
    # 升级pip
    $PYTHON_CMD -m pip install --upgrade pip
    
    # 安装基础依赖
    $PYTHON_CMD -m pip install typer rich pydantic click requests psutil
}

# 创建虚拟环境
create_venv() {
    print_info "创建虚拟环境..."
    
    if [ -d ".venv" ]; then
        print_warning "虚拟环境已存在，跳过创建"
    else
        $PYTHON_CMD -m venv .venv
        print_success "虚拟环境创建成功"
    fi
}

# 安装开发模式
install_dev_mode() {
    print_info "安装开发模式..."
    
    source .venv/bin/activate
    pip install -e .
    print_success "开发模式安装成功"
}

# 设置全局符号链接
setup_global_link() {
    print_info "设置全局符号链接..."
    
    # 创建用户bin目录
    mkdir -p ~/.local/bin
    
    # 创建符号链接
    if [ -L ~/.local/bin/ssf ]; then
        rm ~/.local/bin/ssf
    fi
    
    ln -sf "$(pwd)/.venv/bin/ssf" ~/.local/bin/ssf
    print_success "全局符号链接创建成功"
}

# 检查PATH
check_path() {
    print_info "检查PATH设置..."
    
    if [[ ":$PATH:" == *":$HOME/.local/bin:"* ]]; then
        print_success "PATH已包含 ~/.local/bin"
    else
        print_warning "PATH中未包含 ~/.local/bin"
        print_info "请将以下行添加到你的shell配置文件中:"
        echo "export PATH=\"\$HOME/.local/bin:\$PATH\""
    fi
}

# 测试安装
test_installation() {
    print_info "测试安装..."
    
    # 测试基本命令
    if ssf --help &> /dev/null; then
        print_success "SSF CLI 安装成功"
    else
        print_error "SSF CLI 安装失败"
        exit 1
    fi
    
    # 测试功能
    print_info "测试基本功能..."
    ssf info > /dev/null && print_success "info命令正常"
    ssf status > /dev/null && print_success "status命令正常"
    ssf system > /dev/null && print_success "system命令正常"
}

# 显示使用说明
show_usage() {
    print_info "SSF CLI 部署完成！"
    echo ""
    echo "使用方法:"
    echo "  ssf info          # 显示系统信息"
    echo "  ssf status        # 显示状态"
    echo "  ssf system        # 系统监控"
    echo "  ssf create python --name my-project  # 创建项目"
    echo "  ssf fetch https://httpbin.org/json   # 网络请求"
    echo "  ssf files list --path .              # 文件操作"
    echo ""
    echo "开发模式:"
    echo "  source .venv/bin/activate  # 激活虚拟环境"
    echo "  # 修改代码后自动生效"
    echo ""
    echo "管理脚本:"
    echo "  python setup_global_dev.py install   # 重新安装全局链接"
    echo "  python setup_global_dev.py check     # 检查状态"
    echo "  python setup_global_dev.py test      # 测试功能"
}

# 主函数
main() {
    echo "🚀 SSF CLI 快速部署脚本"
    echo "================================"
    
    # 检查系统要求
    check_command "git"
    check_python_version
    
    # 安装依赖
    install_dependencies
    
    # 创建虚拟环境
    create_venv
    
    # 安装开发模式
    install_dev_mode
    
    # 设置全局链接
    setup_global_link
    
    # 检查PATH
    check_path
    
    # 测试安装
    test_installation
    
    # 显示使用说明
    show_usage
}

# 运行主函数
main "$@" 