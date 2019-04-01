import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont
# QtWidgets模块包含了基本的组件
from PyQt5.QtWidgets import *

import http_file
# 主窗体
from http_request import Requests
from utils import Setting, url_login


# QtCore模块包含了非GUI的功能设计。
def print_info(function_name):
    print("=" * 50 + function_name + "=" * 50)


class Window(QMainWindow):
    # 窗体初始化
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.user_name = None
        self.user_password = None
        self.user = None

        self.ui_file = None
        self.passWordEdit = QLineEdit()  # 密码输入框
        self.passWordEdit.setMinimumHeight(30)
        self.appName = QLabel("字体工具套件")
        self.appName.setAlignment(Qt.AlignHCenter)  # 放中间
        self.appName.setFont(QFont("宋体", 30, QFont.Bold))

        self.userNameEdit = QLineEdit()  # 用户名输入框
        self.userNameEdit.setMinimumHeight(30)
        self.widget = QWidget(parent)
        self.VBoxLayout = QVBoxLayout()  # 垂直排列
        self.hboxLayout = QHBoxLayout()  # 水平排列

        # 设置隐藏密码QRadioButton
        self.btn_check = QRadioButton("显示密码")
        self.btn_check.setStyleSheet('''color: rgb(253,129,53);;''')
        self.btn_check.clicked.connect(self.yanma)

        self.loginBtn = QPushButton("登录")  # 登录按钮
        self.loginBtn.setFixedSize(100, 40)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("登录")
        self.resize(450, 300)  # 设置主窗体大小
        self.setCentralWidget(self.widget)
        self.userNameEdit.setPlaceholderText("用户名")  # 设置文本框显示文字setPlaceholderText()
        self.passWordEdit.setPlaceholderText("密码")
        self.passWordEdit.setEchoMode(QLineEdit.Password)  # 密码输入模式默认
        self.loginBtn.setShortcut('Return')  # enter键触发登录按钮

        # 将所有控件加入垂直Layout中 达到居中
        self.VBoxLayout.addWidget(self.appName)
        self.VBoxLayout.addStretch(1)  # 设置间距平均
        # self.VBoxLayout.setSpacing(15)
        self.VBoxLayout.addWidget(self.userNameEdit)
        self.VBoxLayout.setSpacing(10)
        self.VBoxLayout.addWidget(self.passWordEdit)
        self.VBoxLayout.setSpacing(20)

        self.VBoxLayout.addWidget(self.btn_check)
        self.VBoxLayout.setSpacing(20)

        self.VBoxLayout.addWidget(self.loginBtn, alignment=Qt.AlignHCenter)  # 单元格居中
        # self.VBoxLayout.addWidget(self.loginBtn)
        self.VBoxLayout.addStretch(2)

        # self.VBoxLayout.addWidget(self.registerBtn, alignment=Qt.AlignHCenter)

        # 将垂直Layout加入水平Layout中 达到居中
        self.hboxLayout.addSpacing(80)
        self.hboxLayout.addLayout(self.VBoxLayout)
        self.hboxLayout.addSpacing(80)

        self.loginBtn.clicked.connect(self.login_get)

        self.widget.setLayout(self.hboxLayout)  # 设置窗口总布局

    # 密码隐藏
    def yanma(self):
        if self.btn_check.isChecked():
            # 正常显示所输入的字符，此为默认选项
            self.passWordEdit.setEchoMode(QLineEdit.Normal)
        else:
            # 显示与平台相关的密码掩饰字符，而不是实际输入的字符
            self.passWordEdit.setEchoMode(QLineEdit.Password)

    # 获取用户输入信息
    def login_get(self):
        print_info(sys._getframe().f_code.co_name)

        self.user_name = self.userNameEdit.text()  # 获取用户名
        self.user_password = self.passWordEdit.text()  # 获取用户密码

        setting = Setting()
        setting.select_and_set_user_info(self.user_name, self.user_password)
        self.user = setting.get_user_info()
        print(self.user)
        self.login_request(self.user_name, self.user_password)

    def login_request(self, user_name, user_password):
        print_info(sys._getframe().f_code.co_name)

        data = {"username": user_name, "password": user_password}
        request = Requests()
        request.post_request(url_login, data, None, self.onSuccessRefresh, self.onFail)

    def onFail(self, error_info):
        print_info(sys._getframe().f_code.co_name)

        QMessageBox.warning(self,
                            "错误",
                            error_info,
                            QMessageBox.Yes)
        self.userNameEdit.setFocus()

    def onSuccessRefresh(self, result):
        print_info(sys._getframe().f_code.co_name)

        result = result.json()
        setting = Setting()
        if 'error_code' in result:
            print('fail', result)
            setting.resolve_response_data(result)
            erro_info = setting.get_error_info()
            print(erro_info)
            QMessageBox.warning(self,
                                "警告",
                                erro_info,
                                QMessageBox.Yes)
            self.userNameEdit.setFocus()
        else:
            print('success', result)
            # 根据刷新token 的结果更新数据库中的access_token以及create_time
            if self.user is not None:
                setting.update_existed_user(self.user, result)
            else:
                setting.construct_user_item_and_save(self.user_name, self.user_password, result)
            # 查询更新后的用户信息设置
            setting.select_and_set_user_info(self.user_name, self.user_password)
            self.user = setting.get_user_info()
            self.ui_file = http_file.Window_file()
            self.ui_file.setUser(self.user)
            self.ui_file.show()  # 转移到主界面
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
