#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CheckInk - 快捷方式检查工具
作者: 用户
描述: 检查文件夹下所有快捷方式是否可用，并可选择删除无效的快捷方式
"""

import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                            QHBoxLayout, QWidget, QListWidget, QLabel, QFileDialog,
                            QProgressBar, QMessageBox, QListWidgetItem, QFrame,
                            QSizePolicy)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QMimeData, QUrl, QSize, QPoint, QRectF
from PyQt6.QtGui import (QIcon, QDragEnterEvent, QDropEvent, QFont, QPixmap, 
                         QCursor, QColor, QPainter, QBrush, QPainterPath, QPen)

from shortcut_checker import ShortcutChecker
from style import AppStyle


class TitleBar(QWidget):
    """自定义标题栏"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(40)
        self.is_moving = False
        self.last_pos = None
        self.setObjectName("title_bar")
        self.setStyleSheet("""
            #title_bar {
                background-color: #4a86e8;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
        """)
        
        # 设置布局
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        
        # 添加图标和标题
        icon_label = QLabel()
        icon_label.setPixmap(self.parent.load_icon("assets/icon.png", (24, 24)))
        
        title_label = QLabel("CheckInk - 快捷方式检查工具")
        title_label.setStyleSheet("color: #333333; font-weight: bold; font-size: 14px;")
        
        # 最小化按钮 - 确保按钮始终可见
        min_btn = QPushButton("—")
        min_btn.setObjectName("min_btn")
        min_btn.setFixedSize(30, 30)
        min_btn.setStyleSheet("""
            #min_btn {
                background-color: rgba(0, 0, 0, 0.1);
                color: #333333;
                font-weight: bold;
                font-size: 14px;
                border: none;
                border-radius: 3px;
            }
            #min_btn:hover {
                background-color: rgba(0, 0, 0, 0.2);
            }
        """)
        min_btn.clicked.connect(self.parent.showMinimized)
        
        # 关闭按钮 - 确保按钮始终可见
        close_btn = QPushButton("×")
        close_btn.setObjectName("close_btn")
        close_btn.setFixedSize(30, 30)
        close_btn.setStyleSheet("""
            #close_btn {
                background-color: rgba(0, 0, 0, 0.1);
                color: #333333;
                font-weight: bold;
                font-size: 20px;
                border: none;
                border-radius: 3px;
            }
            #close_btn:hover {
                background-color: #e81123;
                color: white;
            }
        """)
        close_btn.clicked.connect(self.parent.close)
        
        # 添加到布局
        layout.addWidget(icon_label)
        layout.addSpacing(5)
        layout.addWidget(title_label)
        layout.addStretch()
        layout.addWidget(min_btn)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
    
    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_moving = True
            self.last_pos = event.globalPosition().toPoint() - self.parent.pos()
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        if self.is_moving:
            self.parent.move(event.globalPosition().toPoint() - self.last_pos)
    
    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        self.is_moving = False


class DropArea(QFrame):
    """自定义拖放区域"""
    
    dropped = pyqtSignal(str)
    folder_click = pyqtSignal()  # 新增信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        
        self.setAcceptDrops(True)
        self.setMinimumHeight(120)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        
        # 设置布局
        layout = QVBoxLayout(self)
        
        # 添加拖放图标
        self.icon_label = QLabel()
        if self.parent:
            self.icon_label.setPixmap(self.parent.load_icon("assets/drop.png", (48, 48)))
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 添加提示文本
        self.text_label = QLabel("将文件夹拖放到此处，或点击选择文件夹")
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(10)
        self.text_label.setFont(font)
        
        # 添加到布局
        layout.addWidget(self.icon_label)
        layout.addWidget(self.text_label)
        
        self.setStyleSheet("""
            DropArea {
                border: 2px dashed #4a86e8;
                border-radius: 5px;
                background-color: #e9f1fd;
            }
            
            DropArea:hover {
                background-color: #d5e5fb;
            }
        """)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """处理拖拽进入事件"""
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if os.path.isdir(url.toLocalFile()):
                    event.acceptProposedAction()
                    self.setStyleSheet("""
                        DropArea {
                            border: 2px solid #4a86e8;
                            border-radius: 5px;
                            background-color: #d5e5fb;
                        }
                    """)
                    return
    
    def dragLeaveEvent(self, event):
        """处理拖拽离开事件"""
        self.setStyleSheet("""
            DropArea {
                border: 2px dashed #4a86e8;
                border-radius: 5px;
                background-color: #e9f1fd;
            }
            
            DropArea:hover {
                background-color: #d5e5fb;
            }
        """)
    
    def dropEvent(self, event: QDropEvent):
        """处理拖拽释放事件"""
        self.setStyleSheet("""
            DropArea {
                border: 2px dashed #4a86e8;
                border-radius: 5px;
                background-color: #e9f1fd;
            }
            
            DropArea:hover {
                background-color: #d5e5fb;
            }
        """)
        
        # 获取第一个文件夹
        for url in event.mimeData().urls():
            folder_path = url.toLocalFile()
            if os.path.isdir(folder_path):
                self.dropped.emit(folder_path)
                break
    
    def mousePressEvent(self, event):
        """鼠标点击事件"""
        self.folder_click.emit()  # 发射点击信号


class CustomButton(QPushButton):
    """自定义按钮，带图标"""
    
    def __init__(self, text, icon_path=None, parent=None):
        super().__init__(text, parent)
        self.parent = parent
        
        if icon_path and parent:
            if hasattr(parent, 'load_icon'):
                self.setIcon(QIcon(parent.load_icon(icon_path, (18, 18))))
        
        self.setMinimumHeight(36)
        
        # 设置样式
        self.setStyleSheet("""
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
        """)


class CheckInkApp(QMainWindow):
    """主应用程序窗口"""
    
    def __init__(self):
        super().__init__(None, Qt.WindowType.FramelessWindowHint)
        self.setMinimumSize(800, 600)
        
        # 设置应用程序图标
        app_icon = self.load_icon("assets/icon.png")
        if app_icon:
            self.setWindowIcon(QIcon(app_icon))
        
        # 当前检查的文件夹路径
        self.current_folder = ""
        
        # 无效的快捷方式列表
        self.invalid_shortcuts = []
        
        # 检查器实例
        self.checker = None
        
        # 为了圆角而设置透明背景
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # 初始化UI
        self.init_ui()
    
    def paintEvent(self, event):
        """绘制窗口圆角"""
        # 创建QPainter对象
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 创建圆角矩形路径
        path = QPainterPath()
        rect = QRectF(0, 0, self.width(), self.height())
        path.addRoundedRect(rect, 8.0, 8.0)
        
        # 填充背景色
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawPath(path)
    
    def get_resource_path(self, relative_path):
        """获取资源的绝对路径，兼容开发环境和打包后的环境"""
        if getattr(sys, 'frozen', False):
            # 打包后的环境
            base_path = sys._MEIPASS
        else:
            # 开发环境
            base_path = os.path.abspath(".")
        
        return os.path.join(base_path, relative_path)
    
    def load_icon(self, icon_path, size=None):
        """加载图标并处理可能的错误"""
        full_path = self.get_resource_path(icon_path)
        pixmap = None
        
        if os.path.exists(full_path):
            pixmap = QPixmap(full_path)
            if size:
                pixmap = pixmap.scaled(size[0], size[1], 
                                      Qt.AspectRatioMode.KeepAspectRatio, 
                                      Qt.TransformationMode.SmoothTransformation)
        else:
            # 图标不存在时，创建一个彩色占位符
            pixmap = QPixmap(size[0] if size else 24, size[1] if size else 24)
            pixmap.fill(QColor('#4a86e8'))
        
        return pixmap
    
    def init_ui(self):
        """初始化用户界面"""
        # 创建中央窗口部件
        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        central_widget.setStyleSheet("background: transparent;")
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 添加自定义标题栏
        self.title_bar = TitleBar(self)
        main_layout.addWidget(self.title_bar)
        
        # 内容区域
        content_widget = QWidget()
        content_widget.setObjectName("contentWidget")
        
        # 设置内容区域样式，保证下部有圆角
        content_widget.setStyleSheet("""
            QWidget#contentWidget {
                background-color: white;
                border-bottom-left-radius: 8px;
                border-bottom-right-radius: 8px;
            }
        """)
        
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)
        
        # 添加标题
        title_layout = QHBoxLayout()
        
        logo_label = QLabel()
        logo_label.setPixmap(self.load_icon("assets/logo.png", (48, 48)))
        
        title_label = QLabel("快捷方式检查工具")
        title_font = QFont("微软雅黑", 16, QFont.Weight.Bold)
        title_label.setFont(title_font)
        
        title_layout.addWidget(logo_label)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        content_layout.addLayout(title_layout)
        
        # 说明文本
        desc_label = QLabel("检查文件夹中的无效快捷方式 (.lnk, .url)，并可一键删除")
        desc_label.setStyleSheet("color: #666;")
        content_layout.addWidget(desc_label)
        
        # 添加不检查子文件夹的说明
        note_label = QLabel("注意: 只检查选定文件夹中的快捷方式，不包含子文件夹")
        note_label.setStyleSheet("color: #888; font-style: italic; font-size: 11px;")
        content_layout.addWidget(note_label)
        
        # 拖放区域
        self.drop_area = DropArea(self)
        self.drop_area.dropped.connect(self.set_folder)
        self.drop_area.folder_click.connect(self.select_folder)  # 连接新信号
        content_layout.addWidget(self.drop_area)
        
        # 当前文件夹
        folder_layout = QHBoxLayout()
        
        folder_icon = QLabel()
        folder_icon.setPixmap(self.load_icon("assets/folder.png", (20, 20)))
        
        self.folder_label = QLabel("未选择文件夹")
        self.folder_label.setStyleSheet("color: #444; font-weight: bold;")
        
        folder_layout.addWidget(folder_icon)
        folder_layout.addWidget(self.folder_label, 1)
        
        self.select_btn = CustomButton("选择文件夹", "assets/browse.png", self)
        self.select_btn.clicked.connect(self.select_folder)
        folder_layout.addWidget(self.select_btn)
        
        content_layout.addLayout(folder_layout)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimumHeight(20)
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #c0c0c0;
                border-radius: 3px;
                text-align: center;
                background-color: #f0f0f0;
            }
            
            QProgressBar::chunk {
                background-color: #4a86e8;
            }
        """)
        content_layout.addWidget(self.progress_bar)
        
        # 结果标题
        result_layout = QHBoxLayout()
        
        result_icon = QLabel()
        result_icon.setPixmap(self.load_icon("assets/result.png", (20, 20)))
        
        result_label = QLabel("检查结果:")
        result_label.setStyleSheet("font-weight: bold;")
        
        result_layout.addWidget(result_icon)
        result_layout.addWidget(result_label)
        result_layout.addStretch()
        
        content_layout.addLayout(result_layout)
        
        # 结果列表
        self.result_list = QListWidget()
        self.result_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.result_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #c0c0c0;
                border-radius: 3px;
                background-color: white;
                padding: 5px;
            }
            
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #e0e0e0;
            }
            
            QListWidget::item:hover {
                background-color: #e9f1fd;
            }
            
            QListWidget::item:selected {
                background-color: #d5e5fb;
                color: #333;
            }
        """)
        # 连接点击事件，使点击整行时切换选择状态
        self.result_list.itemClicked.connect(self.toggle_item_check)
        # 禁用默认按键事件
        self.result_list.keyPressEvent = self.list_key_press_event
        content_layout.addWidget(self.result_list)
        
        # 按钮区域
        btn_layout = QHBoxLayout()
        
        btn_layout.addStretch()
        
        self.check_btn = CustomButton("开始检查", "assets/check.png", self)
        self.check_btn.setEnabled(False)
        self.check_btn.clicked.connect(self.start_check)
        btn_layout.addWidget(self.check_btn)
        
        self.select_all_btn = CustomButton("全选/反选", "assets/select_all.png", self)
        self.select_all_btn.setEnabled(False)
        self.select_all_btn.clicked.connect(self.select_all_items)
        btn_layout.addWidget(self.select_all_btn)
        
        self.delete_btn = CustomButton("删除选中项", "assets/delete.png", self)
        self.delete_btn.setEnabled(False)
        self.delete_btn.clicked.connect(self.delete_selected)
        btn_layout.addWidget(self.delete_btn)
        
        content_layout.addLayout(btn_layout)
        
        # 状态信息
        status_layout = QHBoxLayout()
        
        status_icon = QLabel()
        status_icon.setPixmap(self.load_icon("assets/info.png", (16, 16)))
        
        self.status_label = QLabel("就绪")
        self.status_label.setStyleSheet("color: #666;")
        
        status_layout.addWidget(status_icon)
        status_layout.addWidget(self.status_label, 1)
        
        content_layout.addLayout(status_layout)
        
        # 添加内容区域
        main_layout.addWidget(content_widget, 1)
        
        # 设置中央部件
        self.setCentralWidget(central_widget)
    
    def select_folder(self):
        """打开文件夹选择对话框"""
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder_path:
            self.set_folder(folder_path)
    
    def set_folder(self, folder_path):
        """设置当前检查的文件夹"""
        self.current_folder = folder_path
        self.folder_label.setText(folder_path)
        self.check_btn.setEnabled(True)
        self.status_label.setText(f"已选择文件夹: {folder_path}")
    
    def start_check(self):
        """开始检查快捷方式"""
        if not self.current_folder:
            return
        
        # 清空结果列表
        self.result_list.clear()
        self.invalid_shortcuts = []
        
        # 禁用按钮
        self.check_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)
        self.select_all_btn.setEnabled(False)
        
        # 显示进度条
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # 创建并启动检查线程
        self.checker = ShortcutCheckerThread(self.current_folder)
        self.checker.progress_signal.connect(self.update_progress)
        self.checker.result_signal.connect(self.show_results)
        self.checker.finished.connect(self.check_finished)
        self.checker.start()
        
        self.status_label.setText("正在检查快捷方式...")
    
    def update_progress(self, current, total):
        """更新进度条"""
        self.progress_bar.setValue(int(current / total * 100))
    
    def show_results(self, invalid_shortcuts):
        """显示检查结果"""
        self.invalid_shortcuts = invalid_shortcuts
        
        if not invalid_shortcuts:
            item = QListWidgetItem("没有发现无效的快捷方式")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setForeground(QColor("#4a86e8"))
            self.result_list.addItem(item)
            return
        
        # 添加无效快捷方式到列表
        for shortcut in invalid_shortcuts:
            item = QListWidgetItem()
            item.setText(shortcut)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            
            # 添加图标
            if shortcut.lower().endswith('.lnk'):
                item.setIcon(QIcon(self.load_icon("assets/lnk.png", (16, 16))))
            elif shortcut.lower().endswith('.url'):
                item.setIcon(QIcon(self.load_icon("assets/url.png", (16, 16))))
            
            self.result_list.addItem(item)
    
    def check_finished(self):
        """检查完成后的操作"""
        self.progress_bar.setVisible(False)
        self.check_btn.setEnabled(True)
        
        if self.invalid_shortcuts:
            self.select_all_btn.setEnabled(True)
            self.delete_btn.setEnabled(True)
            self.status_label.setText(f"检查完成，发现 {len(self.invalid_shortcuts)} 个无效快捷方式")
        else:
            self.status_label.setText("检查完成，所有快捷方式均有效")
    
    def select_all_items(self):
        """全选/反选列表项"""
        # 检查是否所有项目都已选中
        all_checked = True
        for i in range(self.result_list.count()):
            item = self.result_list.item(i)
            if item.flags() & Qt.ItemFlag.ItemIsUserCheckable:
                if item.checkState() != Qt.CheckState.Checked:
                    all_checked = False
                    break
        
        # 如果全部已选中，则取消选中；否则全选
        new_state = Qt.CheckState.Unchecked if all_checked else Qt.CheckState.Checked
        
        for i in range(self.result_list.count()):
            item = self.result_list.item(i)
            if item.flags() & Qt.ItemFlag.ItemIsUserCheckable:
                item.setCheckState(new_state)
    
    def delete_selected(self):
        """删除选中的快捷方式"""
        selected_items = []
        
        # 收集选中的项
        for i in range(self.result_list.count()):
            item = self.result_list.item(i)
            if item.flags() & Qt.ItemFlag.ItemIsUserCheckable and item.checkState() == Qt.CheckState.Checked:
                selected_items.append((i, item.text()))
        
        if not selected_items:
            QMessageBox.information(self, "提示", "请先选择要删除的快捷方式")
            return
        
        # 确认删除
        reply = QMessageBox.question(
            self, 
            "确认删除", 
            f"确定要删除选中的 {len(selected_items)} 个快捷方式吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # 从后往前删除，避免索引变化
            deleted_count = 0
            for i, shortcut_path in reversed(selected_items):
                try:
                    os.remove(shortcut_path)
                    self.result_list.takeItem(i)
                    deleted_count += 1
                except Exception as e:
                    QMessageBox.warning(self, "删除失败", f"无法删除 {shortcut_path}\n错误: {str(e)}")
            
            self.status_label.setText(f"已删除 {deleted_count} 个无效快捷方式")
            
            # 如果列表为空，禁用按钮
            if self.result_list.count() == 0:
                self.select_all_btn.setEnabled(False)
                self.delete_btn.setEnabled(False)
    
    def toggle_item_check(self, item):
        """点击项目时切换选中状态"""
        if item.flags() & Qt.ItemFlag.ItemIsUserCheckable:
            # 切换选中状态
            if item.checkState() == Qt.CheckState.Checked:
                item.setCheckState(Qt.CheckState.Unchecked)
            else:
                item.setCheckState(Qt.CheckState.Checked)
    
    def list_key_press_event(self, event):
        """自定义列表的按键事件，禁用Ctrl+A全选"""
        # 禁用Ctrl+A
        if event.key() == Qt.Key.Key_A and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            return
        # 其他按键事件交给默认处理
        QListWidget.keyPressEvent(self.result_list, event)


class ShortcutCheckerThread(QThread):
    """快捷方式检查线程"""
    progress_signal = pyqtSignal(int, int)
    result_signal = pyqtSignal(list)
    
    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path
        
    def run(self):
        """执行检查操作"""
        checker = ShortcutChecker()
        invalid_shortcuts = checker.check_folder(
            self.folder_path, 
            recursive=False,  # 不递归搜索子文件夹
            progress_callback=self.progress_signal.emit
        )
        self.result_signal.emit(invalid_shortcuts)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 应用样式
    AppStyle.apply_style(app, "light")  # 使用浅色主题
    
    # 创建并显示主窗口
    window = CheckInkApp()
    window.show()
    
    sys.exit(app.exec()) 