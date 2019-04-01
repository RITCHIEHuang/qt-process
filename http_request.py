import sys

import requests
from requests import exceptions


def print_info(function_name):
    print("=" * 50 + function_name + "=" * 50)


class Requests:

    def __init__(self):
        self.on_success = None
        self.on_error = None

    def post_request(self, url, data, header, on_success, on_error):
        print_info(sys._getframe().f_code.co_name)

        self.on_success = on_success
        self.on_error = on_error

        try:
            r = requests.post(url, data, headers=header)
            print(r.headers)
        except exceptions.Timeout as e:
            self.on_error('请求超时：' + str(e.message))
        except exceptions.HTTPError as e:
            self.on_error('http请求错误:' + str(e.message))
        else:
            # 通过status_code判断请求结果是否正确
            if r.status_code == 200:
                print(r.request.headers)
                print(str(r.status_code), r.url)
                self.on_success(r)
            else:
                self.on_error('请求错误：' + str(r.status_code) + ',' + str(r.reason))
