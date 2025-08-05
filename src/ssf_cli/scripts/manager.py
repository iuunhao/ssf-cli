"""
脚本管理器
用于管理和执行各种文件处理脚本
"""

import importlib
import inspect
from pathlib import Path
from typing import Any, Dict, List, Optional, Type

from .base import BaseScript
from ..config import SSFConfig


class ScriptManager:
    """脚本管理器"""
    
    def __init__(self, config: SSFConfig, working_dir: Path):
        """
        初始化脚本管理器
        
        Args:
            config: 配置对象
            working_dir: 工作目录
        """
        self.config = config
        self.working_dir = working_dir
        self.scripts = {}
        self._load_scripts()
    
    def _load_scripts(self):
        """加载所有脚本"""
        scripts_dir = Path(__file__).parent
        
        # 遍历scripts目录
        for script_file in scripts_dir.glob("*.py"):
            if script_file.name in ["__init__.py", "base.py", "manager.py"]:
                continue
            
            try:
                # 动态导入脚本模块
                module_name = f"ssf_cli.scripts.{script_file.stem}"
                module = importlib.import_module(module_name)
                
                # 查找脚本类
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and 
                        issubclass(obj, BaseScript) and 
                        obj != BaseScript):
                        
                        script_name = script_file.stem
                        self.scripts[script_name] = obj
                        break
                        
            except Exception as e:
                print(f"加载脚本失败 {script_file.name}: {e}")
    
    def get_available_scripts(self) -> List[str]:
        """获取可用的脚本列表"""
        return list(self.scripts.keys())
    
    def get_script_info(self, script_name: str) -> Optional[Dict[str, Any]]:
        """获取脚本信息"""
        if script_name not in self.scripts:
            return None
        
        script_class = self.scripts[script_name]
        script_instance = script_class(self.config, self.working_dir)
        
        return script_instance.get_script_info()
    
    def execute_script(self, script_name: str, **kwargs) -> Dict[str, Any]:
        """
        执行脚本
        
        Args:
            script_name: 脚本名称
            **kwargs: 脚本参数
            
        Returns:
            执行结果
        """
        if script_name not in self.scripts:
            return {
                "success": False,
                "error": f"脚本不存在: {script_name}",
                "available_scripts": self.get_available_scripts()
            }
        
        try:
            # 创建脚本实例
            script_class = self.scripts[script_name]
            script_instance = script_class(self.config, self.working_dir)
            
            # 执行脚本
            result = script_instance.execute(**kwargs)
            
            # 添加脚本信息
            result["script_name"] = script_name
            result["script_info"] = script_instance.get_script_info()
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": f"执行脚本失败: {e}",
                "script_name": script_name
            }
    
    def list_scripts(self) -> List[Dict[str, Any]]:
        """列出所有脚本信息"""
        scripts_info = []
        
        for script_name in self.scripts:
            info = self.get_script_info(script_name)
            if info:
                scripts_info.append(info)
        
        return scripts_info
    
    def validate_script_params(self, script_name: str, **kwargs) -> bool:
        """验证脚本参数"""
        if script_name not in self.scripts:
            return False
        
        try:
            script_class = self.scripts[script_name]
            script_instance = script_class(self.config, self.working_dir)
            return script_instance.validate_params(**kwargs)
        except Exception:
            return False 