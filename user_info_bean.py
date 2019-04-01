import time


class UserInfo:
    def __init__(self):
        self.user_id = None
        self.user_name = None
        self.user_password = None
        self.access_token = None
        self.access_token_expires = None
        self.refresh_token = None
        self.refresh_token_expires = None
        self.header_type = None
        self.create_time = None

    def dump_to_list(self):
        user_list = [self.user_id, self.user_name, self.user_password, self.access_token, self.access_token_expires,
                     self.header_type, self.refresh_token, self.refresh_token_expires, self.create_time]
        return user_list

    # 适配数据库item
    def set_info(self, data):
        self.user_id = data[0]
        self.user_name = data[1]
        self.user_password = data[2]
        self.access_token = data[3]
        self.access_token_expires = data[4]
        self.header_type = data[5]
        self.refresh_token = data[6]
        self.refresh_token_expires = data[7]
        self.create_time = data[8]

    def get_user_id(self):
        return self.user_id

    def get_username(self):
        return self.user_name

    def get_password(self):
        return self.user_password

    def get_access_token(self):
        return self.access_token

    def get_access_token_expires(self):
        return self.access_token_expires

    def get_refresh_token(self):
        return self.refresh_token

    def get_refresh_token_expires(self):
        return self.refresh_token_expires

    def get_header_type(self):
        return self.header_type

    def is_access_token_expires(self):
        # return (int(time.time()) - self.create_time) > self.access_token_expires
        return (int(time.time()) - self.create_time) > 24 * 60 * 60
        # return True

    def is_refresh_token_expires(self):
        # return (int(time.time()) - self.create_time) > self.refresh_token_expires
        return (int(time.time()) - self.create_time) > 7 * 24 * 60 * 60

    def get_create_time(self):
        return self.create_time

    def __str__(self):
        return str("user_id : " + str(self.get_user_id()) + "\nusername : " + self.get_username()
                   + "\nuser_password : " + self.get_password() + "\naccess_token : " + self.get_access_token()
                   + "\naccess_token_expires : " + str(
            self.get_access_token_expires()) + "\nrefresh_token : " + self.get_refresh_token()
                   + "\nrefresh_token_expires : " + str(
            self.get_refresh_token_expires()) + "\nheader_type : " + self.get_header_type()
                   + "\ncreate_time : " + str(self.get_create_time()))
