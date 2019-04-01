import os
import sys
from shutil import rmtree

from PyQt5.QtCore import Qt, QDir  # QPoint表示一个平面上整数精度的点坐标
from PyQt5.QtGui import QFontDatabase, QFont  # QPainter绘制各种图形
from PyQt5.QtWidgets import *

# 设置窗体界面的大小, 以及网格的相关属性
import http_login

# 主窗体
from utils import delete_user_info


def print_info(function_name):
    print("=" * 50 + function_name + "=" * 50)


class User(QMainWindow):
    def __init__(self, fontfile, txtfile, parent=None):
        super(User, self).__init__(parent)

        self.ui_login = http_login.Window()

        self.setWindowTitle("字体工具")
        self.ROW_COUNT = 8
        self.COLUMN_COUNT = 10
        self.table = QTableWidget(self.ROW_COUNT, self.COLUMN_COUNT, self)

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        gridLayout = QGridLayout(self)
        centralWidget.setLayout(gridLayout)
        gridLayout.addWidget(self.table, 0, 0)

        self.font_file = fontfile
        self.txt_file = txtfile

        self.user = None
        self.setup_ui()  # 初始化为UI控件


    def setUser(self, user):
        self.user = user

    def setup_ui(self):
        self.resize(800, 600)

        # 菜单栏及事件绑定
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)  # 自定义非系统原生菜单栏
        menubar.setFixedHeight(30)  # 设置固定高度展开菜单
        file_menu = menubar.addMenu('& 文件')
        help_menu = menubar.addMenu('& 帮助')

        save_act = QAction('保存为', self)
        save_act.setShortcut('Ctrl+S')
        save_act.triggered.connect(self.slot_act_save_file)  # 保存文件绑定保存文件Dialog

        logout_act = QAction('注销', self)
        logout_act.triggered.connect(self.slot_act_logout)

        quit_act = QAction('退出', self)
        quit_act.triggered.connect(self.slot_act_close)  # 关闭窗体事件

        # 事件加入菜单栏
        file_menu.addAction(save_act)
        file_menu.addSeparator()  # 分隔符
        file_menu.addAction(quit_act)
        file_menu.addAction(logout_act)

        self.create_table()

    def create_table(self):
        global font
        print_info(sys._getframe().f_code.co_name)

        self.table.verticalHeader().setHidden(True)
        self.table.horizontalHeader().setHidden(True)

        # 设置字体
        fontId = QFontDatabase.addApplicationFont(self.font_file)
        fontFamilies = QFontDatabase.applicationFontFamilies(fontId)
        font = QFont(fontFamilies[0], 75)

        # 设置文字
        character_list = []
        with open(self.txt_file, 'r', encoding="gbk") as f:
            data = f.readlines()
            for line in data:
                for i in list(line.strip("\n")):
                    character_list.append(i)
        print(character_list)

        self.ROW_COUNT = max(self.ROW_COUNT, int(len(character_list) / self.COLUMN_COUNT))
        print("row : %d, column: %d" % (self.ROW_COUNT, self.COLUMN_COUNT))

        for i in range(self.COLUMN_COUNT):
            self.table.setColumnWidth(i, 75)
        for j in range(self.ROW_COUNT):
            self.table.setRowHeight(j, 75)

        t = 0
        for i in range(self.ROW_COUNT):
            for j in range(self.COLUMN_COUNT):
                if t >= len(character_list):
                    break

                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignCenter)
                item.setFont(font)
                item.setText(character_list[t])
                self.table.setItem(i, j, item)
                t = t + 1

            # 将文本框的内容保存到新的文本文件中

    def slot_act_save_file(self):
        print_info(sys._getframe().f_code.co_name)

        filename, filetype = QFileDialog.getSaveFileName(self, '另存为', '')

        if filename == "":
            print("\n取消选择")
            return

        print("\n你选择要保存的文件为:")
        print(filename)
        print(type(filename))
        print("文件筛选器类型: ", filetype)

        with open(self.font_file, 'rb') as f:
            content = f.read()
            with open(filename, 'wb') as f2:
                f2.write(content)

        # 弹出消息框
        msg = QMessageBox(self)
        msg.setInformativeText("保存到: " + filename)
        msg.setWindowTitle("保存文件")
        msg.setDefaultButton(QMessageBox.Ok)
        msg.exec_()

    def closeEvent(self, event):
        # 删除临时文件
        self.delete_temp_files()
        event.accept()

    def slot_act_close(self):
        reply = QMessageBox.question(self, 'Message', '你确认要退出么?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.close()

    def slot_act_logout(self):
        delete_user_info(self.user)
        self.user = None
        self.ui_login.show()
        self.hide()

    def delete_temp_files(self):
        path = QDir.currentPath() + "/tmp/"
        rmtree(path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = User()
    ui.show()
    sys.exit(app.exec_())
