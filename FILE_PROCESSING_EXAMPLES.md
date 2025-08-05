# SSF CLI 文件处理功能使用示例

## 概述

SSF CLI 提供了强大的文件处理功能，支持批量重命名、模式匹配、前缀后缀、格式化等功能。所有文件处理操作都支持备份功能，确保数据安全。

## 可用脚本

### 重命名脚本 (rename)

支持多种重命名方式：
- 前缀/后缀添加
- 字符串替换
- 格式化重命名
- 批量处理
- 自动备份

## 使用示例

### 1. 基础重命名

```bash
# 为所有txt文件添加前缀
ssf process rename --prefix "new_" --pattern "*.txt"

# 为所有jpg文件添加后缀
ssf process rename --suffix "_processed" --pattern "*.jpg"

# 同时添加前缀和后缀
ssf process rename --prefix "IMG_" --suffix "_2024" --pattern "*.jpg"
```

### 2. 字符串替换

```bash
# 将文件名中的"old"替换为"new"
ssf process rename --replace "old=new" --pattern "*.txt"

# 多个替换规则（需要多次运行）
ssf process rename --replace "spaces=underscores" --pattern "*.txt"
ssf process rename --replace "UPPER=lower" --pattern "*.txt"
```

### 3. 格式化重命名

```bash
# 使用日期和索引格式化
ssf process rename --format "{date}_{index}_{name}" --pattern "*.jpg"

# 使用时间戳格式化
ssf process rename --format "{datetime}_{name}" --pattern "*.png"

# 复杂格式化
ssf process rename --format "IMG_{date}_{index:03d}_{name}" --pattern "*.jpg"
```

### 4. 预览模式

```bash
# 预览重命名结果，不实际执行
ssf process rename --prefix "new_" --pattern "*.txt" --dry-run

# 预览替换结果
ssf process rename --replace "old=new" --pattern "*.txt" --dry-run
```

### 5. 备份控制

```bash
# 启用备份（默认）
ssf process rename --prefix "new_" --pattern "*.txt" --backup

# 禁用备份
ssf process rename --prefix "new_" --pattern "*.txt" --no-backup
```

### 6. 递归控制

```bash
# 递归处理子目录（默认）
ssf process rename --prefix "new_" --pattern "*.txt" --recursive

# 仅处理当前目录
ssf process rename --prefix "new_" --pattern "*.txt" --no-recursive
```

### 7. 排除文件

```bash
# 排除特定模式的文件
ssf process rename --prefix "new_" --pattern "*.txt" --exclude "temp*,backup*"

# 排除多个模式
ssf process rename --prefix "new_" --pattern "*.txt" --exclude "temp*,backup*,old*"
```

### 8. 组合使用

```bash
# 复杂重命名：前缀+替换+格式化
ssf process rename \
  --prefix "IMG_" \
  --replace "spaces=underscores" \
  --format "{date}_{index}_{name}" \
  --pattern "*.jpg" \
  --recursive \
  --backup \
  --dry-run
```

## 格式化变量

在格式化字符串中可以使用以下变量：

- `{name}` - 原文件名（不含扩展名）
- `{ext}` - 文件扩展名
- `{date}` - 当前日期 (YYYYMMDD)
- `{time}` - 当前时间 (HHMMSS)
- `{datetime}` - 当前日期时间 (YYYYMMDD_HHMMSS)
- `{index}` - 文件索引（从1开始）
- `{stem}` - 当前文件名（不含扩展名）

## 备份功能

- 备份文件存储在 `./backup/` 目录
- 备份文件名格式：`原文件名_backup_时间戳.扩展名`
- 可以通过配置修改备份目录
- 备份功能默认启用，可通过 `--no-backup` 禁用

## 安全特性

1. **预览模式**：使用 `--dry-run` 预览操作结果
2. **自动备份**：所有重命名操作都会自动备份原文件
3. **冲突处理**：自动检测文件名冲突并添加时间戳
4. **错误处理**：详细的错误信息和回滚机制

## 配置选项

可以通过配置文件设置默认行为：

```bash
# 查看当前配置
ssf config show

# 设置默认备份目录
ssf config local backup_dir "./my_backup"

# 设置默认重命名配置
ssf config local rename_config.auto_backup true
```

## 脚本管理

```bash
# 查看所有可用脚本
ssf scripts

# 查看特定脚本信息
ssf process rename --action info

# 查看脚本列表
ssf process list --action info
```

## 实际应用场景

### 1. 照片整理

```bash
# 将手机照片按日期重命名
ssf process rename --format "IMG_{date}_{index}" --pattern "*.jpg" --recursive

# 添加拍摄地点前缀
ssf process rename --prefix "Paris_" --pattern "*.jpg"
```

### 2. 文档管理

```bash
# 为文档添加版本号
ssf process rename --suffix "_v1.0" --pattern "*.pdf"

# 按项目分类
ssf process rename --prefix "ProjectA_" --pattern "*.docx"
```

### 3. 代码文件整理

```bash
# 统一文件命名规范
ssf process rename --replace "UPPER=lower" --pattern "*.py"
ssf process rename --replace "spaces=underscores" --pattern "*.py"
```

### 4. 批量处理

```bash
# 处理多种文件类型
ssf process rename --prefix "processed_" --pattern "*.{txt,pdf,docx}"

# 按文件大小分类
ssf process rename --format "large_{name}" --pattern "*.mp4" --recursive
```

## 注意事项

1. **备份目录**：确保有足够的磁盘空间存储备份文件
2. **权限问题**：确保对目标目录有读写权限
3. **文件名长度**：某些系统对文件名长度有限制
4. **特殊字符**：避免在文件名中使用特殊字符
5. **批量操作**：大量文件操作时建议先使用 `--dry-run` 预览

## 故障排除

### 常见问题

1. **备份失败**：检查磁盘空间和权限
2. **重命名失败**：检查文件是否被其他程序占用
3. **权限错误**：确保对目标目录有写权限
4. **文件名冲突**：系统会自动添加时间戳解决冲突

### 调试技巧

```bash
# 启用详细日志
ssf config local log_level DEBUG

# 查看系统信息
ssf debug

# 检查环境状态
ssf status
``` 