import sys
import base64
import random,time
import os
from io import BytesIO

import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QFont

name_list = []
called_name_list = []
text_status = 0

def load_names_from_file(file_path):
    try:
        df = pd.read_excel(file_path, usecols=[0], names=None)
        return [i[0] for i in df.values.tolist()]
    except Exception as e:
        QMessageBox.critical(None, "错误", f"无法读取文件：{e}")
        return []

def load_default_file():
    default_file = "list.xlsx"
    if os.path.exists(default_file):
        global name_list
        name_list = load_names_from_file(default_file)
        if name_list:
            return "默认名单已加载"
        else:
            return "默认名单为空"
    else:
        return "未找到默认名单，请手动导入"

def file_dialog():
    from PyQt5.QtWidgets import QFileDialog
    file_path, _ = QFileDialog.getOpenFileName(None, "导入名单", "", "Excel 文件 (*.xlsx);;All Files (*)")
    if file_path:
        global name_list
        name_list = load_names_from_file(file_path)
        if name_list:
            return "名单已加载"
        else:
            return "名单为空"
    else:
        return "未选择文件"

class RandomCall(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("")
        self.setGeometry(300, 300, 400, 280)
        self.setFixedSize(self.size())
        self.setStyleSheet(
        '''
        QWidget {
            background-color: white;
        }

        QLabel {
            font-family: "黑体";
            font-size: 40px;
            font-weight: bold;
            color: black;
            qproperty-alignment: "AlignCenter";
        }

        QCheckBox {
            font-family: "Microsoft YaHei UI";
            font-size: 16px;
        }

        QPushButton {
            background-color: #A5D6A7;
            height: 40px;
            width: 100px;
            border-radius: 13px;
            font-family: "Microsoft YaHei UI";
            font-size: 20px;
            color: white;
        }

        QPushButton:hover {
            background-color: #81c784;
        }

        QPushButton:pressed {
            background-color: #66bb6a;
        }

        QMenuBar {
            background-color: white;
        }

        QMenu {
            background-color: white;
        }

        QMenuBar::item {
            spacing: 3px;
            padding: 2px 10px;
            background-color: transparent;
        }

        QMenuBar::item:selected {
            background-color: #e0e0e0;
        }

        QMenu::item {
            padding: 2px 20px;
        }

        QMenu::item:selected {
            background-color: #e0e0e0;
        }
        '''
        )

        # 设置窗口图标
        #self.setWindowIcon(QIcon("icon.ico"))

        # 初始化状态
        global text_status
        text_status = 0
        self.status_label = QLabel("准备就绪", self)
        self.status_label.setFont(QFont("黑体", 40, QFont.Bold))
        self.status_label.setAlignment(Qt.AlignCenter)

        # 复选框
        self.allow_repeat_checkbox = QCheckBox("允许重复点名", self)
        self.allow_repeat_checkbox.setChecked(False)

        # 按钮
        self.call_button = QPushButton("点名", self)
        self.call_button.setFont(QFont("黑体", 20))
        
        self.call_button.clicked.connect(self.start)

        self.reset_button = QPushButton("重置", self)
        self.reset_button.setFont(QFont("黑体", 20))
        #self.reset_button.setStyleSheet("background-color: #A5D6A7")
        self.reset_button.clicked.connect(self.reset)

        # 布局
        layout = QVBoxLayout()

        layout.addWidget(self.status_label)
        layout.addWidget(self.allow_repeat_checkbox)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.call_button)
        button_layout.addWidget(self.reset_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        # 菜单栏
        self.main_menu = QMenuBar(self)
        self.file_menu = self.main_menu.addMenu("文件")
        self.help_menu = self.main_menu.addMenu("帮助")

        self.show_called_action = QAction("已点名名单", self)
        self.show_called_action.triggered.connect(self.called_name_list_show)
        self.file_menu.addAction(self.show_called_action)

        self.import_action = QAction("导入", self)
        self.import_action.triggered.connect(self.import_names)
        self.file_menu.addAction(self.import_action)

        self.exit_action = QAction("退出", self)
        self.exit_action.triggered.connect(self.close)
        self.file_menu.addAction(self.exit_action)

        self.help_action = QAction("帮助", self)
        self.help_action.triggered.connect(self.show_help)
        self.help_menu.addAction(self.help_action)

        self.about_action = QAction("关于", self)
        self.about_action.triggered.connect(self.show_about)
        self.help_menu.addAction(self.about_action)

        self.init_status()

    def init_status(self):
        status_text = load_default_file()
        if status_text:
            self.status_label.setText(status_text)
    
    def start(self):
        if not name_list:
            if called_name_list:
                self.status_label.setText("名单已用完")
            else:
                self.status_label.setText("名单为空")
            return
        def show():
            global rmname
            nl=name_list.copy()
            name=random.choice(nl)
            self.status_label.setText(name)
            rmname=name
            QApplication.processEvents()
        for _ in range(10): 
            #self.status_label.setText(name)
            '''t=QTimer(self)
            t.timeout.connect(show)
            t.start(300)'''
            show()
        #t.stop()
        if not self.allow_repeat_checkbox.isChecked():
            called_name_list.append(rmname)
            if not name_list:
                self.status_label.setText("名单已用完")
            else:
                name_list.remove(rmname)

    def reset(self):
        global name_list, called_name_list
        called_name_list.clear()
        load_default_file()
        if name_list:
            self.status_label.setText("准备就绪")
        else:
            self.status_label.setText("名单为空")

    def called_name_list_show(self):
        if not self.allow_repeat_checkbox.isChecked():
            if called_name_list:
                QMessageBox.information(None, "已点名名单", "\n".join(called_name_list))
            else:
                QMessageBox.information(None, "已点名名单", "没有已点名名单")
        else:
            QMessageBox.information(None, "已点名名单", "允许重复点名时，已点名名单不显示")

    def import_names(self):
        status_text = file_dialog()
        if status_text:
            self.status_label.setText(status_text)

    def show_help(self):
        QMessageBox.information(None, "使用说明", "使用说明：\n"
            "1. 程序会尝试加载默认文件 list.xlsx\n"
            "2. 如果未找到默认文件，请点击“文件 -> 导入”选择名单文件\n"
            "3. 可以选择是否允许重复点名\n"
            "4. 点击“点名”按钮进行随机点名\n"
            "5. 点击“重置”按钮清空已点名名单\n"
            "6. 点击“文件 -> 已点名名单”查看已点名名单\n")

    def show_about(self):
        QMessageBox.information(None, "关于", "随机点名器\n"
            "版本 1.1\n"
            "原创：Astral & Colipot\n"
            "Github 开源地址: github.com/Meltide/RandomCall\n"
            "Forked改编仓库：github.com/EricDing618/RandomCall")

if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setWindowTitle("随机点名器")
    win.setGeometry(300, 300, 400, 280)
    win.setFixedSize(win.size())
    #win.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint,False)
    win.setStyleSheet("background-color: white")

    # 设置窗口图标
    win.setWindowIcon(QIcon("icon.ico"))

    random_call_widget = RandomCall()
    win.setCentralWidget(random_call_widget)

    win.show()
    sys.exit(app.exec())
