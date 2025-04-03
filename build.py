#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CheckInk打包脚本
用于将应用程序打包为独立的exe文件
"""

import os
import sys
import platform
import subprocess
import shutil


def check_dependencies():
    """检查是否安装了必要的依赖"""
    try:
        import PyInstaller
        print("PyInstaller 已安装")
    except ImportError:
        print("正在安装 PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    try:
        import PyQt6
        print("PyQt6 已安装")
    except ImportError:
        print("请安装 PyQt6: pip install PyQt6")
        sys.exit(1)
    
    try:
        import win32com
        print("pywin32 已安装")
    except ImportError:
        print("正在安装 pywin32...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32"])


def build_exe():
    """构建独立的exe文件"""
    # 打包命令
    cmd = [
        "pyinstaller",
        "--name=CheckInk",
        "--windowed",
        "--onefile",
        "--clean",
        "--noconfirm",  # 覆盖输出目录
        "--icon=assets/icon.png" if os.path.exists("assets/icon.png") else "",
        "--add-data=assets;assets",
        # 排除不必要的模块和库
        "--exclude-module=_tkinter",
        "--exclude-module=tkinter",
        "--exclude-module=tcl",
        "--exclude-module=unittest",
        "--exclude-module=email",
        "--exclude-module=test",
        "--exclude-module=pydoc_data",
        "--exclude-module=socketserver",
        "--exclude-module=xmlrpc",
        # 优化设置
        "--strip",  # 去除符号表和调试信息
        "main.py"
    ]
    
    # 过滤掉空字符串
    cmd = [item for item in cmd if item]
    
    # 执行打包命令
    print("正在打包应用程序...")
    subprocess.check_call(cmd)
    
    print(f"打包完成! 可执行文件位于: {os.path.join('dist', 'CheckInk.exe')}")


def clean_build_files():
    """清理构建文件"""
    dirs_to_remove = ["build", "__pycache__"]
    files_to_remove = ["CheckInk.spec"]
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    
    for file_name in files_to_remove:
        if os.path.exists(file_name):
            os.remove(file_name)


def main():
    """主函数"""
    # 检查操作系统
    if platform.system() != "Windows":
        print("此打包脚本仅支持Windows系统")
        sys.exit(1)
    
    # 检查依赖
    check_dependencies()
    
    # 构建exe
    build_exe()
    
    # 自动清理构建文件
    clean_build_files()
    print("构建文件已清理")
    
    print("打包过程完成!")


if __name__ == "__main__":
    main() 