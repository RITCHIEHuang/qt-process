import sqlite3
import sys

from user_info_bean import UserInfo


def print_info(function_name):
    print("=" * 50 + function_name + "=" * 50)


class Database:
    def __init__(self):
        self.conn = None
        # self.delete_db() # 清空数据库
        self.create_db()

    # 清空数据库
    def delete_db(self):
        print_info(sys._getframe().f_code.co_name)

        self.connect()
        curs = self.conn.cursor()
        SQL_DELTE_TABLE = '''delete from user_info'''
        curs.execute(SQL_DELTE_TABLE)
        self.close()
        print("TABLE CLEARED")

    def create_db(self):
        print_info(sys._getframe().f_code.co_name)

        self.connect()
        curs = self.conn.cursor()
        SQL_CREATE_TABLE = '''CREATE TABLE IF NOT EXISTS user_info (id INTEGER PRIMARY KEY, user_name TEXT, 
        user_password TEXT, access_token TEXT, access_token_expires INT , header_type TEXT, 
        refresh_token TEXT, refresh_token_expires INT, create_time INT)'''
        curs.execute(SQL_CREATE_TABLE)
        self.close()
        print("TABLE CREATED")

    def insert_info(self, login_data):
        print_info(sys._getframe().f_code.co_name)

        self.connect()
        curs = self.conn.cursor()
        SQL_INSERT_ITEM = '''INSERT INTO user_info (user_name, user_password, access_token, access_token_expires,
        header_type, refresh_token, refresh_token_expires, create_time) values (?, ?, ?, ?, ?, ?, ?, ?)'''
        curs.execute(SQL_INSERT_ITEM, login_data)
        self.close()
        print("ITEM INSERTED")

    def delete_all_users(self):
        print_info(sys._getframe().f_code.co_name)

        self.connect()
        curs = self.conn.cursor()
        SQL_DELTE = "DELETE * FROM user_info"
        curs.execute(SQL_DELTE)
        self.close()
        print("ALL DELETED")

    def delete_user_by_id(self, id):
        print_info(sys._getframe().f_code.co_name)

        self.connect()
        curs = self.conn.cursor()
        SQL_DELTE = "DELETE FROM user_info where id=?"
        uid = [id]
        curs.execute(SQL_DELTE, tuple(uid))
        self.close()
        print("user DELETED")

    def select_all_info(self):
        print_info(sys._getframe().f_code.co_name)

        self.connect()
        curs = self.conn.cursor()
        SQL_SELECT_ITEM = '''SELECT * FROM user_info'''
        cursor = curs.execute(SQL_SELECT_ITEM)
        for row in cursor:
            user = UserInfo()
            user.set_info(row)
            print(user)
        self.close()
        return user

    def select_info_by_id(self, user_id):
        print_info(sys._getframe().f_code.co_name)

        self.connect()
        curs = self.conn.cursor()
        SQL_SELECT_ITEM = '''SELECT * FROM user_info where id = ?'''
        userid = [user_id]
        cursor = curs.execute(SQL_SELECT_ITEM, tuple(userid))
        user = None
        for row in cursor:
            user = UserInfo()
            user.set_info(row)
            print(user)
        self.close()
        return user

    def select_valid_user(self):
        print_info(sys._getframe().f_code.co_name)

        self.connect()
        curs = self.conn.cursor()
        SQL_SELECT_ITEM = '''SELECT * FROM user_info where (select strftime('%s','now') - create_time < refresh_token_expires)'''
        cursor = curs.execute(SQL_SELECT_ITEM)
        user = None
        for row in cursor:
            user = UserInfo()
            user.set_info(row)
            print(user)
        self.close()
        return user

    def select_by_username_and_password(self, u_name, u_password):
        print_info(sys._getframe().f_code.co_name)

        self.connect()
        curs = self.conn.cursor()
        SQL_SELECT_ITEM = '''SELECT * FROM user_info where user_name = ? and user_password = ?'''
        cursor = curs.execute(SQL_SELECT_ITEM, (u_name, u_password))

        user = None
        for row in cursor:
            user = UserInfo()
            user.set_info(row)
            print(user)
            break
        self.close()
        return user

    def is_user_exists(self, u_name, u_password):
        print_info(sys._getframe().f_code.co_name)

        self.connect()
        curs = self.conn.cursor()
        SQL_SELECT_ITEM = '''SELECT * FROM user_info where user_name = ? and user_password = ?'''
        cursor = curs.execute(SQL_SELECT_ITEM, (u_name, u_password))

        u_id = None
        for row in cursor:
            u_id = row[0]
            print("user_id", u_id)
            # user.set_info(row)
            break
        self.close()
        return u_id

    def update_info_by_id(self, u_id, data):
        print_info(sys._getframe().f_code.co_name)

        self.connect()
        curs = self.conn.cursor()
        SQL_UPDATE_ITEM = '''UPDATE user_info SET user_name = ?, user_password = ?, access_token = ?, 
        access_token_expires = ?,
        header_type = ?, refresh_token =?, refresh_token_expires = ?, create_time = ? where id = ?'''

        update_data = list(data)
        update_data.append(u_id)
        update_data = tuple(update_data)
        print(update_data)

        curs.execute(SQL_UPDATE_ITEM, update_data)
        self.close()

    def connect(self):
        # print_info(sys._getframe().f_code.co_name)

        self.conn = sqlite3.connect('user_info.db')
        print("database connected")

    def close(self):
        # print_info(sys._getframe().f_code.co_name)
        self.conn.commit()
        self.conn.close()
        print("database closed")
