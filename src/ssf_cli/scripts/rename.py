"""
文件重命名脚本
支持批量重命名、模式匹配、前缀后缀等功能
"""

import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..core.base import BaseScript
from ..config import SSFConfig


class RenameScript(BaseScript):
    """文件重命名脚本"""
    
    def __init__(self, config: SSFConfig, working_dir: Path):
        super().__init__(config, working_dir)
        from ..utils import get_logger
        self.logger = get_logger("rename_script")
    
    def validate_params(self, **kwargs) -> bool:
        """
        验证重命名参数
        
        Args:
            **kwargs: 重命名参数
                - pattern: 文件模式 (可选)
                - prefix: 前缀 (可选)
                - suffix: 后缀 (可选)
                - replace: 替换规则 (可选)
                - format: 格式化规则 (可选)
                - dry_run: 是否仅预览 (可选)
                - backup: 是否备份 (可选)
                - recursive: 是否递归 (可选)
                
        Returns:
            参数是否有效
        """
        # 检查是否至少有一个重命名规则
        rename_rules = ['prefix', 'suffix', 'replace', 'format']
        has_rule = any(kwargs.get(rule) for rule in rename_rules)
        
        if not has_rule:
            self.log_error("至少需要指定一个重命名规则 (prefix, suffix, replace, format)")
            return False
        
        # 验证replace参数
        if 'replace' in kwargs and kwargs['replace']:
            replace = kwargs['replace']
            if not isinstance(replace, dict):
                self.log_error("replace参数必须是字典格式")
                return False
        
        # 验证format参数
        if 'format' in kwargs and kwargs['format']:
            format_str = kwargs['format']
            if not isinstance(format_str, str):
                self.log_error("format参数必须是字符串")
                return False
        
        return True
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        执行文件重命名
        
        Args:
            **kwargs: 重命名参数
                - pattern: 文件模式 (默认: "*")
                - prefix: 前缀
                - suffix: 后缀
                - replace: 替换规则 {'old': 'new'}
                - format: 格式化规则 (支持 {name}, {ext}, {date}, {index})
                - dry_run: 是否仅预览 (默认: False)
                - backup: 是否备份 (默认: True)
                - recursive: 是否递归 (默认: True)
                - exclude: 排除模式列表
                
        Returns:
            执行结果
        """
        # 验证参数
        if not self.validate_params(**kwargs):
            return {"success": False, "error": "参数验证失败"}
        
        # 获取参数
        pattern = kwargs.get('pattern', '*')
        prefix = kwargs.get('prefix', '')
        suffix = kwargs.get('suffix', '')
        replace = kwargs.get('replace', {})
        format_str = kwargs.get('format', '')
        dry_run = kwargs.get('dry_run', False)
        output_dir = kwargs.get('output_dir', None)
        recursive = kwargs.get('recursive', True)
        exclude = kwargs.get('exclude', [])
        
        # 查找文件
        files = self.find_files(pattern, recursive)
        
        # 过滤排除的文件
        if exclude:
            files = self._filter_excluded_files(files, exclude)
        
        if not files:
            self.log_warning(f"未找到匹配的文件: {pattern}")
            return {"success": True, "message": "未找到匹配的文件", "renamed": []}
        
        self.log_info(f"找到 {len(files)} 个文件")
        
        # 执行重命名
        renamed_files = []
        errors = []
        
        for index, file_path in enumerate(files, 1):
            try:
                result = self._rename_file(
                    file_path, index, prefix, suffix, replace, format_str, 
                    dry_run, output_dir
                )
                if result['success']:
                    renamed_files.append(result)
                else:
                    errors.append(result)
            except Exception as e:
                error_result = {
                    'success': False,
                    'file': str(file_path),
                    'error': str(e)
                }
                errors.append(error_result)
                self.log_error(f"重命名失败 {file_path}: {e}")
        
        # 返回结果
        result = {
            "success": len(errors) == 0,
            "total_files": len(files),
            "renamed_files": len(renamed_files),
            "errors": len(errors),
            "renamed": renamed_files,
            "error_details": errors
        }
        
        if dry_run:
            result["message"] = f"预览模式: 将重命名 {len(renamed_files)} 个文件"
        else:
            result["message"] = f"成功重命名 {len(renamed_files)} 个文件"
        
        return result
    
    def _filter_excluded_files(self, files: List[Path], exclude: List[str]) -> List[Path]:
        """过滤排除的文件"""
        filtered_files = []
        
        for file_path in files:
            should_exclude = False
            for exclude_pattern in exclude:
                if file_path.match(exclude_pattern):
                    should_exclude = True
                    break
            
            if not should_exclude:
                filtered_files.append(file_path)
        
        return filtered_files
    
    def _rename_file(self, file_path: Path, index: int, prefix: str, suffix: str, 
                    replace: Dict[str, str], format_str: str, dry_run: bool, 
                    output_dir: Optional[str]) -> Dict[str, Any]:
        """重命名单个文件"""
        
        # 获取文件信息
        file_info = self.get_file_info(file_path)
        old_name = file_path.name
        old_stem = file_path.stem
        old_ext = file_path.suffix
        
        # 生成新文件名
        new_stem = old_stem
        
        # 应用替换规则
        if replace:
            for old_str, new_str in replace.items():
                new_stem = new_stem.replace(old_str, new_str)
        
        # 应用前缀和后缀
        if prefix:
            new_stem = prefix + new_stem
        if suffix:
            new_stem = new_stem + suffix
        
        # 应用格式化规则
        if format_str:
            new_stem = self._apply_format(new_stem, old_stem, old_ext, index, format_str)
        
        # 构建新文件名
        new_name = new_stem + old_ext
        new_path = file_path.parent / new_name
        
        # 检查文件名冲突
        if new_path.exists() and new_path != file_path:
            self.log_warning(f"文件名冲突: {new_name}")
            # 添加时间戳避免冲突
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_stem = f"{new_stem}_{timestamp}"
            new_name = new_stem + old_ext
            new_path = file_path.parent / new_name
        
        result = {
            "success": True,
            "old_path": str(file_path),
            "new_path": str(new_path),
            "old_name": old_name,
            "new_name": new_name,
            "file_info": file_info
        }
        
        if dry_run:
            result["action"] = "preview"
            self.log_info(f"预览: {old_name} -> {new_name}")
        else:
            # 复制到新目录而不是重命名
            try:
                # 创建输出目录
                if output_dir:
                    output_path = Path(output_dir)
                else:
                    output_path = Path(self.config.output_dir or "./renamed_files")
                output_path.mkdir(parents=True, exist_ok=True)
                
                # 构建新文件路径
                new_file_path = output_path / new_name
                
                # 检查文件名冲突
                if new_file_path.exists():
                    self.log_warning(f"文件名冲突: {new_name}")
                    # 添加时间戳避免冲突
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    new_stem = f"{new_stem}_{timestamp}"
                    new_name = new_stem + old_ext
                    new_file_path = output_path / new_name
                
                # 复制文件到新目录
                import shutil
                shutil.copy2(file_path, new_file_path)
                
                result["action"] = "copied"
                result["output_path"] = str(new_file_path)
                self.log_info(f"复制: {old_name} -> {new_name}")
                
            except Exception as e:
                result["success"] = False
                result["error"] = str(e)
                self.log_error(f"复制失败: {e}")
        
        return result
    
    def _apply_format(self, new_stem: str, old_stem: str, old_ext: str, 
                     index: int, format_str: str) -> str:
        """应用格式化规则"""
        
        # 获取当前日期
        now = datetime.now()
        
        # 格式化变量
        format_vars = {
            "name": old_stem,
            "ext": old_ext,
            "date": now.strftime("%Y%m%d"),
            "time": now.strftime("%H%M%S"),
            "datetime": now.strftime("%Y%m%d_%H%M%S"),
            "index": str(index).zfill(3),
            "stem": new_stem
        }
        
        # 应用格式化
        try:
            formatted = format_str.format(**format_vars)
            return formatted
        except KeyError as e:
            self.log_warning(f"格式化变量未找到: {e}")
            return new_stem
    
    def get_supported_extensions(self) -> List[str]:
        """获取支持的文件扩展名"""
        return ["*"]  # 支持所有文件类型
    
    def get_config_keys(self) -> List[str]:
        """获取使用的配置键"""
        return ["backup_dir", "output_dir"] 