#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
快捷方式检查器模块
提供快捷方式检查功能
"""

import os
import sys
import winreg
import subprocess
from urllib.parse import urlparse
import win32com.client


class ShortcutChecker:
    """快捷方式检查器类"""
    
    def __init__(self):
        # 快捷方式文件扩展名
        self.shortcut_exts = ['.lnk', '.url']
    
    def check_folder(self, folder_path, recursive=True, progress_callback=None):
        """
        检查文件夹中的所有快捷方式
        
        参数:
            folder_path (str): 要检查的文件夹路径
            recursive (bool): 是否递归检查子文件夹
            progress_callback (callable): 进度回调函数，接收当前进度和总数
            
        返回:
            list: 无效快捷方式的路径列表
        """
        invalid_shortcuts = []
        all_shortcuts = []
        
        # 收集所有快捷方式
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                _, ext = os.path.splitext(file_path)
                
                if ext.lower() in self.shortcut_exts:
                    all_shortcuts.append(file_path)
            
            # 如果不递归，则只处理顶层文件夹
            if not recursive:
                break
        
        # 检查每个快捷方式
        total = len(all_shortcuts)
        for i, shortcut_path in enumerate(all_shortcuts):
            # 回调进度信息
            if progress_callback:
                progress_callback(i, total)
            
            # 检查快捷方式是否有效
            if not self.is_shortcut_valid(shortcut_path):
                invalid_shortcuts.append(shortcut_path)
        
        # 确保最终进度达到100%
        if progress_callback and total > 0:
            progress_callback(total, total)
            
        return invalid_shortcuts
    
    def is_shortcut_valid(self, shortcut_path):
        """
        检查快捷方式是否有效
        
        参数:
            shortcut_path (str): 快捷方式文件路径
            
        返回:
            bool: 快捷方式是否有效
        """
        _, ext = os.path.splitext(shortcut_path)
        
        if ext.lower() == '.lnk':
            return self._check_lnk_file(shortcut_path)
        elif ext.lower() == '.url':
            return self._check_url_file(shortcut_path)
        else:
            # 不支持的文件类型
            return True
    
    def _check_lnk_file(self, lnk_path):
        """
        检查.lnk文件是否有效
        
        参数:
            lnk_path (str): .lnk文件路径
            
        返回:
            bool: 快捷方式是否有效
        """
        try:
            # 使用Windows Shell COM对象解析.lnk文件
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(lnk_path)
            
            target_path = shortcut.TargetPath
            
            # 检查目标是否存在
            if not target_path:
                return False
                
            # 如果目标是文件或目录，直接检查是否存在
            if os.path.exists(target_path):
                return True
                
            # 检查是否为特殊的Windows应用
            if target_path.lower().endswith('.exe'):
                # 尝试在PATH中查找
                for path in os.environ["PATH"].split(os.pathsep):
                    exe_path = os.path.join(path, os.path.basename(target_path))
                    if os.path.exists(exe_path):
                        return True
            
            # 检查是否为UWP应用
            if ":" not in target_path and "\\" not in target_path:
                return self._check_uwp_app(target_path)
                
            return False
            
        except Exception as e:
            # 解析错误，视为无效
            return False
    
    def _check_url_file(self, url_path):
        """
        检查.url文件是否有效
        
        参数:
            url_path (str): .url文件路径
            
        返回:
            bool: URL是否有效
        """
        try:
            # 读取.url文件内容
            with open(url_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # 提取URL
            url = None
            for line in content.splitlines():
                if line.startswith('URL='):
                    url = line[4:].strip()
                    break
            
            if not url:
                return False
            
            # 解析URL
            parsed_url = urlparse(url)
            
            # 检查URL格式是否有效
            if not parsed_url.scheme or not parsed_url.netloc:
                return False
                
            # 对于本地文件URL，检查文件是否存在
            if parsed_url.scheme.lower() == 'file':
                file_path = parsed_url.path.replace('/', '\\').lstrip('\\')
                return os.path.exists(file_path)
                
            # 对于网络URL，我们不进行实际连接检查，因为这可能会很慢
            # 只检查URL格式是否正确
            return True
            
        except Exception as e:
            # 解析错误，视为无效
            return False
    
    def _check_uwp_app(self, app_id):
        """
        检查UWP应用是否已安装
        
        参数:
            app_id (str): 应用ID
            
        返回:
            bool: 应用是否已安装
        """
        try:
            # 尝试通过注册表检查UWP应用
            key_path = r"Software\Classes\Extensions\ContractId\Windows.Launch\PackageId"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                # 遍历注册表项
                i = 0
                while True:
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        if app_id.lower() in subkey_name.lower():
                            return True
                        i += 1
                    except WindowsError:
                        break
            return False
        except Exception:
            return False


if __name__ == "__main__":
    # 简单测试
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
        checker = ShortcutChecker()
        invalid_shortcuts = checker.check_folder(folder_path)
        
        print(f"发现 {len(invalid_shortcuts)} 个无效快捷方式:")
        for shortcut in invalid_shortcuts:
            print(f"  - {shortcut}")
    else:
        print("用法: python shortcut_checker.py <文件夹路径>") 