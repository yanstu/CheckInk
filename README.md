# CheckInk - 快捷方式检查工具

![CheckInk Logo](assets/icon.png)

CheckInk是一个用于检查和管理Windows系统中无效快捷方式的工具，可以帮助您轻松找出并删除指向不存在的文件、程序或网址的快捷方式。

## 功能特点

- 🔍 检查文件夹中所有快捷方式是否可用
- 🗑️ 一键删除无效的快捷方式
- 🔗 支持.lnk和.url格式的快捷方式文件
- 🖱️ 支持文件夹拖放操作
- 🌈 美观的用户界面，现代化的浅色主题
- 💻 单一可执行文件，无需安装

## 界面截图

![main](./screenshot/main.png)

*使用CheckInk前，请先备份重要数据。*

## 如何使用

1. 运行CheckInk.exe程序
2. 将要检查的文件夹拖放到程序中，或点击"选择文件夹"按钮
3. 点击"开始检查"按钮，程序会自动检查所有快捷方式
4. 检查完成后，勾选无效的快捷方式并点击"删除选中项"按钮

## 如何构建

### 前提条件

- Python 3.6+
- PyQt6
- pywin32

### 安装依赖

```bash
pip install -r requirements.txt
```

或手动安装各个依赖:

```bash
pip install PyQt6>=6.3.0 pywin32>=228 pyinstaller>=5.1
```

### 构建可执行文件

```bash
python build.py
```

构建完成后，可执行文件将位于`dist`目录下。

## 技术实现

- 使用Python和PyQt6构建GUI界面
- 通过win32com库解析和验证.lnk文件
- 解析.url文件内容以验证URL的有效性
- 自定义窗口标题栏和控件样式
- 使用PyInstaller将应用程序打包为单独的exe文件