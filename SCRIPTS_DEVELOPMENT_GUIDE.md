# SSF CLI 脚本开发指南

## 目录结构

```
src/ssf_cli/
├── core/                    # 核心模块
│   ├── __init__.py
│   ├── base.py             # 脚本基类
│   └── manager.py          # 脚本管理器
├── scripts/                # 独立脚本目录
│   ├── __init__.py
│   ├── rename.py           # 重命名脚本
│   ├── delete.py           # 删除脚本
│   └── ...                 # 其他独立脚本
├── commands.py             # CLI命令
├── config.py               # 配置管理
└── utils.py                # 工具函数
```

## 设计理念

### 1. **scripts目录保持干净**
- 只存放独立的脚本文件
- 每个脚本都是完整的、可独立运行的
- 不包含基类、管理器等基础设施代码

### 2. **core模块提供基础设施**
- `BaseScript`: 所有脚本的基类
- `ScriptManager`: 脚本管理和执行
- 提供统一的接口和工具函数

### 3. **模块化设计**
- 脚本之间相互独立
- 易于添加新脚本
- 便于维护和测试

## 如何添加新脚本

### 1. 创建脚本文件

在 `src/ssf_cli/scripts/` 目录下创建新的脚本文件，例如 `move.py`：

```python
"""
文件移动脚本
支持批量移动、模式匹配等功能
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

from ..core.base import BaseScript
from ..config import SSFConfig


class MoveScript(BaseScript):
    """文件移动脚本"""
    
    def __init__(self, config: SSFConfig, working_dir: Path):
        super().__init__(config, working_dir)
        from ..utils import get_logger
        self.logger = get_logger("move_script")
    
    def validate_params(self, **kwargs) -> bool:
        """验证参数"""
        # 实现参数验证逻辑
        return True
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """执行脚本"""
        # 实现主要逻辑
        return {"success": True, "message": "移动完成"}
    
    def get_supported_extensions(self) -> List[str]:
        """获取支持的文件扩展名"""
        return ["*"]
    
    def get_config_keys(self) -> List[str]:
        """获取使用的配置键"""
        return ["output_dir"]
```

### 2. 继承BaseScript

所有脚本都必须继承 `BaseScript` 类并实现以下方法：

#### 必需方法

- `validate_params(**kwargs) -> bool`: 验证脚本参数
- `execute(**kwargs) -> Dict[str, Any]`: 执行脚本主要逻辑

#### 可选方法

- `get_supported_extensions() -> List[str]`: 返回支持的文件扩展名
- `get_config_keys() -> List[str]`: 返回使用的配置键

### 3. 使用基类提供的工具

```python
# 查找文件
files = self.find_files(pattern, recursive)

# 获取文件信息
file_info = self.get_file_info(file_path)

# 日志记录
self.log_info("信息日志")
self.log_success("成功日志")
self.log_warning("警告日志")
self.log_error("错误日志")

# 访问配置
output_dir = self.config.output_dir
```

### 4. 参数处理

脚本会接收到来自CLI命令的参数：

```python
def execute(self, **kwargs) -> Dict[str, Any]:
    # 获取参数
    pattern = kwargs.get('pattern', '*')
    dry_run = kwargs.get('dry_run', False)
    recursive = kwargs.get('recursive', True)
    
    # 处理参数
    if not self.validate_params(**kwargs):
        return {"success": False, "error": "参数验证失败"}
    
    # 执行逻辑
    # ...
```

### 5. 返回结果格式

脚本应该返回统一的结果格式：

```python
{
    "success": True,                    # 是否成功
    "message": "操作完成",              # 消息
    "total_files": 10,                 # 总文件数
    "processed_files": 8,              # 处理成功数
    "errors": 2,                       # 错误数
    "details": [...],                  # 详细信息
    "error_details": [...]             # 错误详情
}
```

## 脚本示例

### 重命名脚本 (rename.py)

```bash
# 使用示例
ssf process rename --prefix "new_" --pattern "*.txt"
ssf process rename --replace "old=new" --dry-run
ssf process rename --format "{date}_{index}_{name}" --pattern "*.jpg"
```

### 删除脚本 (delete.py)

```bash
# 使用示例
ssf process delete --pattern "*.tmp" --dry-run
ssf process delete --pattern "*.log" --exclude "important.log"
```

## 添加CLI命令

如果需要为脚本添加特定的CLI命令，可以在 `commands.py` 中添加：

```python
@app.command()
def move(
    pattern: str = typer.Option("*", "--pattern", "-p", help="文件模式"),
    target_dir: str = typer.Option(".", "--target-dir", "-t", help="目标目录"),
    dry_run: bool = typer.Option(False, "--dry-run", help="仅预览"),
):
    """文件移动工具"""
    # 实现命令逻辑
    pass
```

## 最佳实践

### 1. **参数验证**
- 始终验证输入参数
- 提供清晰的错误信息
- 支持预览模式 (`--dry-run`)

### 2. **错误处理**
- 捕获并处理异常
- 提供详细的错误信息
- 支持部分失败的情况

### 3. **日志记录**
- 使用统一的日志格式
- 记录关键操作步骤
- 提供进度信息

### 4. **性能考虑**
- 支持大量文件处理
- 避免内存溢出
- 提供进度反馈

### 5. **安全特性**
- 支持预览模式
- 保留原文件（如适用）
- 冲突处理机制

## 测试脚本

### 1. 单元测试

```python
def test_move_script():
    config = SSFConfig()
    script = MoveScript(config, Path.cwd())
    
    # 测试参数验证
    assert script.validate_params(pattern="*.txt")
    assert not script.validate_params(pattern="")
    
    # 测试执行
    result = script.execute(pattern="*.txt", dry_run=True)
    assert result["success"] == True
```

### 2. 集成测试

```bash
# 测试脚本加载
ssf scripts

# 测试脚本执行
ssf process move --pattern "*.txt" --dry-run
```

## 调试技巧

### 1. 启用调试日志

```bash
ssf config local log_level DEBUG
```

### 2. 查看脚本信息

```bash
ssf process move --action info
```

### 3. 预览模式

```bash
ssf process move --pattern "*.txt" --dry-run
```

## 注意事项

1. **命名规范**: 脚本文件名使用小写和下划线
2. **类名规范**: 脚本类名使用PascalCase并以Script结尾
3. **文档字符串**: 为脚本和类添加详细的文档字符串
4. **类型注解**: 使用类型注解提高代码可读性
5. **错误处理**: 妥善处理异常和错误情况
6. **性能优化**: 考虑大量文件处理的性能问题

## 扩展建议

### 1. 图片处理脚本
- 批量裁剪
- 格式转换
- 压缩优化

### 2. 视频处理脚本
- 格式转换
- 压缩处理
- 提取音频

### 3. 文档处理脚本
- 批量转换
- 格式统一
- 内容提取

### 4. 数据清理脚本
- 重复文件检测
- 空文件清理
- 临时文件清理

通过这种模块化的设计，你可以轻松地添加新的文件处理脚本，同时保持代码的整洁和可维护性。 