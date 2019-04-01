import sys

import PyQt5.sip
from PyQt5.QtWidgets import QApplication, QMessageBox, QDialog

import http_file
import http_login
from database_util import Database
from http_request import Requests
from utils import Setting, url_refresh_token


def print_info(function_name):
    print("=" * 50 + function_name + "=" * 50)


class App:
    def __init__(self):
        self.user = None

    def start_app(self):
        print_info(sys._getframe().f_code.co_name)

        db = Database()
        self.user = db.select_valid_user()  # 查找refresh_token没过期的用户
        if self.user:
            print('====== login existed user =====')
            # 将会转移到app.py的逻辑
            if not self.user.is_access_token_expires():
                print("access_token valid")
                file = http_file.Window_file()
                file.setUser(self.user)
                file.show()  # 转移到主界面
            elif not self.user.is_refresh_token_expires():
                print("refresh_token valid")

                self.refresh_request(self.user)
            file = http_file.Window_file()
            file.setUser(self.user)
            file.show()
        else:  # refresh_token已经过期，需要重新登录
            print("====== login =====")
            login = http_login.Window()
            login.show()
        sys.exit(app.exec_())

    def refresh_request(self, user):
        print_info(sys._getframe().f_code.co_name)

        header = {"Authorization": user.get_header_type() + " " + user.get_refresh_token()}
        print(header)
        request = Requests()
        request.post_request(url_refresh_token, "", header, self.onSuccessRefresh,
                             self.onFail)

    def onFail(self, error_info):
        print_info(sys._getframe().f_code.co_name)
        print(error_info)
        # QMessageBox.warning(self,
        #                     "错误",
        #                     error_info,
        #                     QMessageBox.Yes)

    def onSuccessRefresh(self, result):
        print_info(sys._getframe().f_code.co_name)

        result = result.json()
        setting = Setting()
        if 'error_code' in result:
            print('fail', result)
            setting.resolve_response_data(result)
            erro_info = setting.get_error_info()
            print(erro_info)
            # QMessageBox.warning(self,
            #                     "警告",
            #                     erro_info,
            #                     QMessageBox.Yes)
        else:
            print('success', result)
            # 根据刷新token 的结果更新数据库中的access_token以及create_time
            setting.select_and_set_user_info(self.user.get_username(), self.user.get_password())
            self.user = setting.get_user_info()
            setting.update_existed_user(self.user, result)

            # 查询更新后的用户信息设置
            setting.select_and_set_user_info(self.user.get_username(), self.user.get_password())
            self.user = setting.get_user_info()
            self.ui_file = http_file.Window_file()
            self.ui_file.setUser(self.user)
            self.ui_file.show()  # 转移到主界面


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mapp = App()
    mapp.start_app()
