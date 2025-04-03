#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CheckInk应用程序样式
提供美观的现代化界面样式
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor


class AppStyle:
    """应用程序样式类"""
    
    @staticmethod
    def get_dark_style():
        """
        获取深色主题样式表
        
        返回:
            str: 样式表字符串
        """
        return """
        QWidget {
            background-color: #2D2D30;
            color: #F0F0F0;
            font-family: "微软雅黑", "Microsoft YaHei", "Segoe UI", sans-serif;
            font-size: 12px;
        }
        
        QMainWindow {
            background-color: #252526;
        }
        
        QLabel {
            color: #E6E6E6;
            background-color: transparent;
        }
        
        QPushButton {
            background-color: #0078D7;
            color: white;
            border: none;
            border-radius: 3px;
            padding: 8px 16px;
            min-width: 80px;
        }
        
        QPushButton:hover {
            background-color: #1C97EA;
        }
        
        QPushButton:pressed {
            background-color: #00559B;
        }
        
        QPushButton:disabled {
            background-color: #555555;
            color: #999999;
        }
        
        QProgressBar {
            border: 1px solid #444444;
            border-radius: 3px;
            text-align: center;
            background-color: #333333;
        }
        
        QProgressBar::chunk {
            background-color: #0078D7;
            width: 20px;
        }
        
        QListWidget {
            background-color: #1E1E1E;
            border: 1px solid #444444;
            border-radius: 3px;
            padding: 5px;
            outline: none;
        }
        
        QListWidget::item {
            padding: 5px;
            border-radius: 2px;
        }
        
        QListWidget::item:hover {
            background-color: #3E3E40;
        }
        
        QListWidget::item:selected {
            background-color: #0078D7;
            color: white;
        }
        
        QScrollBar:vertical {
            border: none;
            background-color: #2D2D30;
            width: 12px;
            margin: 12px 0px 12px 0px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #686868;
            border-radius: 3px;
            min-height: 20px;
            margin: 0px 2px 0px 2px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #888888;
        }
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }
        
        QFileDialog {
            background-color: #2D2D30;
            color: #F0F0F0;
        }
        
        QMessageBox {
            background-color: #2D2D30;
            color: #F0F0F0;
        }
        
        QMessageBox QPushButton {
            min-width: 60px;
            padding: 6px 12px;
        }
        """
    
    @staticmethod
    def get_light_style():
        """
        获取浅色主题样式表
        
        返回:
            str: 样式表字符串
        """
        return """
        QWidget {
            background-color: #FFFFFF;
            color: #333333;
            font-family: "微软雅黑", "Microsoft YaHei", "Segoe UI", sans-serif;
            font-size: 12px;
        }
        
        QMainWindow {
            background-color: transparent;
            border: none;
        }
        
        QWidget#centralWidget {
            background-color: transparent;
            border: none;
        }
        
        QWidget#contentWidget {
            background-color: #FFFFFF;
            border-bottom-left-radius: 8px;
            border-bottom-right-radius: 8px;
        }
        
        QLabel {
            color: #333333;
            background-color: transparent;
        }
        
        QFrame#title_bar {
            background-color: #4a86e8;
            color: white;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            padding: 0px 5px;
        }
        
        QLabel#title_label {
            color: white;
            font-weight: bold;
            font-size: 14px;
            padding-left: 5px;
        }
        
        QPushButton#min_btn, QPushButton#close_btn {
            color: white;
            font-weight: bold;
            background-color: rgba(255, 255, 255, 0.1);
            border: none;
            border-radius: 3px;
        }
        
        QPushButton#min_btn {
            font-size: 14px;
        }
        
        QPushButton#close_btn {
            font-size: 20px;
        }
        
        QPushButton#min_btn:hover {
            background-color: rgba(255, 255, 255, 0.3);
        }
        
        QPushButton#close_btn:hover {
            background-color: #e81123;
        }
        
        CustomButton {
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            background-color: #4a86e8;
            color: white;
            font-weight: bold;
        }
        
        CustomButton:hover {
            background-color: #3a76d8;
        }
        
        CustomButton:pressed {
            background-color: #2a66c8;
        }
        
        CustomButton:disabled {
            background-color: #c0c0c0;
            color: #808080;
        }
        
        QProgressBar {
            border: 1px solid #CCCCCC;
            border-radius: 3px;
            text-align: center;
            background-color: #F0F0F0;
        }
        
        QProgressBar::chunk {
            background-color: #4a86e8;
            width: 20px;
        }
        
        QListWidget {
            border: 1px solid #dcdcdc;
            border-radius: 3px;
            background-color: white;
            padding: 5px;
            outline: none;
        }
        
        QListWidget::item {
            padding: 8px;
            border-bottom: 1px solid #f0f0f0;
        }
        
        QListWidget::item:hover {
            background-color: #e9f1fd;
        }
        
        QListWidget::item:selected {
            background-color: #d5e5fb;
            color: #333333;
        }
        
        QScrollBar:vertical {
            border: none;
            background-color: #F5F5F5;
            width: 12px;
            margin: 12px 0px 12px 0px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #CCCCCC;
            border-radius: 3px;
            min-height: 20px;
            margin: 0px 2px 0px 2px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #BBBBBB;
        }
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }
        
        QFileDialog {
            background-color: #FFFFFF;
            color: #333333;
        }
        
        QMessageBox {
            background-color: #FFFFFF;
            color: #333333;
        }
        
        QMessageBox QPushButton {
            min-width: 60px;
            padding: 6px 12px;
        }
        
        DropArea {
            border: 2px dashed #4a86e8;
            border-radius: 5px;
            background-color: #e9f1fd;
        }
        
        DropArea:hover {
            background-color: #d5e5fb;
        }
        """
    
    @staticmethod
    def apply_style(app, theme="light"):
        """
        应用样式到应用程序
        
        参数:
            app: QApplication实例
            theme (str): 主题，"dark"或"light"
        """
        # 设置应用程序样式
        app.setStyle("Fusion")
        
        # 应用样式表
        if theme.lower() == "dark":
            app.setStyleSheet(AppStyle.get_dark_style())
            AppStyle._set_dark_palette(app)
        else:
            app.setStyleSheet(AppStyle.get_light_style())
            AppStyle._set_light_palette(app)
    
    @staticmethod
    def _set_dark_palette(app):
        """设置深色调色板"""
        palette = QPalette()
        
        # 基本颜色
        palette.setColor(QPalette.ColorRole.Window, QColor(45, 45, 48))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.Base, QColor(30, 30, 30))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(30, 30, 30))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.Text, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.Button, QColor(45, 45, 48))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        palette.setColor(QPalette.ColorRole.Link, QColor(0, 120, 215))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 120, 215))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        
        # 禁用状态颜色
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, QColor(128, 128, 128))
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor(128, 128, 128))
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor(128, 128, 128))
        
        app.setPalette(palette)
    
    @staticmethod
    def _set_light_palette(app):
        """设置浅色调色板"""
        palette = QPalette()
        
        # 基本颜色
        palette.setColor(QPalette.ColorRole.Window, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(51, 51, 51))
        palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(245, 245, 245))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(51, 51, 51))
        palette.setColor(QPalette.ColorRole.Text, QColor(51, 51, 51))
        palette.setColor(QPalette.ColorRole.Button, QColor(245, 245, 245))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(51, 51, 51))
        palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        palette.setColor(QPalette.ColorRole.Link, QColor(74, 134, 232))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(74, 134, 232))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        
        # 禁用状态颜色
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, QColor(153, 153, 153))
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor(153, 153, 153))
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor(153, 153, 153))
        
        app.setPalette(palette) 