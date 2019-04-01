import sys
import time

from database_util import Database


def print_info(function_name):
    print("=" * 50 + function_name + "=" * 50)


def delete_user_info(user):
    id = user.get_user_id()
    db = Database()
    db.delete_user_by_id(id)


url_upload = "http://118.25.130.140/fontgen"
url_login = "http://118.25.130.140/auth/login"
url_refresh_token = "http://118.25.130.140/auth/refresh"


class Setting:
    def __init__(self):
        self.response = None
        self.error_code = None
        self.user = None

    def set_error_code(self):
        if 'error_code' in self.response:
            self.error_code = self.response['error_code']

    def get_error_info(self):
        switcher = {
            "1001": "页面找不到",
            "1002": "方法不被允许",
            "1003": "服务器内部错误",
            "1004": "非法请求",
            "1005": "注册失败",
            "1006": "登录失败",
            "1007": "用户不存在",
            "1008": "令牌过期",
            "1009": "无效令牌",
            "1010": "缺少令牌",
            "1011": "请求体过大",
            "1012": "字体生成失败",
            "1013": "字体发生异常"
        }
        return switcher.get(self.error_code, "未知错误码")

    def resolve_response_data(self, data):
        self.response = data
        self.set_error_code()

    def construct_user_item_and_save(self, user_name, user_password, receive_data):
        print_info(sys._getframe().f_code.co_name)

        user_item = [user_name, user_password]
        for key in receive_data:
            user_item.append(receive_data[key])
        user_item.append(int(time.time()))
        user_tuple = tuple(user_item)

        print(user_tuple)
        db = Database()
        print("insert new user item")
        db.insert_info(user_tuple)

    def update_existed_user(self, old_user, refresh_response):
        print_info(sys._getframe().f_code.co_name)

        db = Database()
        data_list = old_user.dump_to_list()
        data_list[3] = refresh_response['access_token']
        data_list[4] = refresh_response['access_token_expires']
        data_list[7] = refresh_response['header_type']
        data_list[8] = int(time.time())
        data_list = data_list[1:]
        data_tuple = tuple(data_list)
        print(data_tuple)

        db.update_info_by_id(old_user.get_user_id(), data_tuple)

    def select_and_set_user_info(self, user_name=None, user_password=None):
        print_info(sys._getframe().f_code.co_name)

        db = Database()
        if user_name is not None and user_password is not None:
            self.user = db.select_by_username_and_password(user_name, user_password)
        else:  # 查找有效的user
            self.user = db.select_valid_user()

    def get_user_info(self):
        return self.user
