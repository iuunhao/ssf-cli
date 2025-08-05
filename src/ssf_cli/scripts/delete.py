"""
文件删除脚本
支持批量删除、模式匹配、安全删除等功能
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..core.base import BaseScript
from ..config import SSFConfig


class DeleteScript(BaseScript):
    """文件删除脚本"""
    
    def __init__(self, config: SSFConfig, working_dir: Path):
        super().__init__(config, working_dir)
        from ..utils import get_logger
        self.logger = get_logger("delete_script")
    
    def validate_params(self, **kwargs) -> bool:
        """
        验证删除参数
        
        Args:
            **kwargs: 删除参数
                - pattern: 文件模式 (可选)
                - dry_run: 是否仅预览 (可选)
                - recursive: 是否递归 (可选)
                - exclude: 排除模式列表 (可选)
                
        Returns:
            参数是否有效
        """
        # 检查是否指定了文件模式
        if 'pattern' not in kwargs or not kwargs['pattern']:
            self.log_error("必须指定文件模式")
            return False
        
        return True
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        执行文件删除
        
        Args:
            **kwargs: 删除参数
                - pattern: 文件模式
                - dry_run: 是否仅预览 (默认: False)
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
        dry_run = kwargs.get('dry_run', False)
        recursive = kwargs.get('recursive', True)
        exclude = kwargs.get('exclude', [])
        
        # 查找文件
        files = self.find_files(pattern, recursive)
        
        # 过滤排除的文件
        if exclude:
            files = self._filter_excluded_files(files, exclude)
        
        if not files:
            self.log_warning(f"未找到匹配的文件: {pattern}")
            return {"success": True, "message": "未找到匹配的文件", "deleted": []}
        
        self.log_info(f"找到 {len(files)} 个文件")
        
        # 执行删除
        deleted_files = []
        errors = []
        
        for file_path in files:
            try:
                result = self._delete_file(file_path, dry_run)
                if result['success']:
                    deleted_files.append(result)
                else:
                    errors.append(result)
            except Exception as e:
                error_result = {
                    'success': False,
                    'file': str(file_path),
                    'error': str(e)
                }
                errors.append(error_result)
                self.log_error(f"删除失败 {file_path}: {e}")
        
        # 返回结果
        result = {
            "success": len(errors) == 0,
            "total_files": len(files),
            "deleted_files": len(deleted_files),
            "errors": len(errors),
            "deleted": deleted_files,
            "error_details": errors
        }
        
        if dry_run:
            result["message"] = f"预览模式: 将删除 {len(deleted_files)} 个文件"
        else:
            result["message"] = f"成功删除 {len(deleted_files)} 个文件"
        
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
    
    def _delete_file(self, file_path: Path, dry_run: bool) -> Dict[str, Any]:
        """删除单个文件"""
        
        file_info = self.get_file_info(file_path)
        
        result = {
            "success": True,
            "file_path": str(file_path),
            "file_name": file_path.name,
            "file_info": file_info
        }
        
        if dry_run:
            result["action"] = "preview"
            self.log_info(f"预览删除: {file_path.name}")
        else:
            try:
                file_path.unlink()
                result["action"] = "deleted"
                self.log_info(f"删除: {file_path.name}")
            except Exception as e:
                result["success"] = False
                result["error"] = str(e)
                self.log_error(f"删除失败: {e}")
        
        return result
    
    def get_supported_extensions(self) -> List[str]:
        """获取支持的文件扩展名"""
        return ["*"]  # 支持所有文件类型
    
    def get_config_keys(self) -> List[str]:
        """获取使用的配置键"""
        return ["output_dir"] 