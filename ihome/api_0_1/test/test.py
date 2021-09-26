# import unittest
#
# class TestClass(unittest.TestCase):
#
#     def setUp(self):
#         current_app.testing = True
#         self.client  = current_app.test_client()
#
#     def tearDown(self):
#         pass
#
#     def test_app_exits(self):
#
#         pass


import json
import unittest
from flask import current_app

# from demo1_login import app


class LoginTest(unittest.TestCase):
    """为登录逻辑编写测试案例"""

    def setUp(self):
        current_app.testing = True
        self.client = current_app.test_client()

    def test_empty_username_password(self):
        """测试用户名与密码为空的情况[当参数不全的话，返回errcode=-2]"""
        response = current_app.test_client().post('/login', data={})
        json_data = response.data
        json_dict = json.loads(json_data)

        self.assertIn('errcode', json_dict, '数据格式返回错误')
        self.assertEqual(json_dict['errcode'], -2, '状态码返回错误')

        # TODO 测试用户名为空的情况

        # TODO 测试密码为空的情况

    def test_error_username_password(self):
        """测试用户名和密码错误的情况[当登录名和密码错误的时候，返回 errcode = -1]"""
        response = current_app.test_client().post('/login', data={"username": "aaaaa", "password": "12343"})
        json_data = response.data
        json_dict = json.loads(json_data)
        self.assertIn('errcode', json_dict, '数据格式返回错误')
        self.assertEqual(json_dict['errcode'], -1, '状态码返回错误')

        # TODO 测试用户名错误的情况

        # TODO 测试密码错误的情况


if __name__ == '__main__':
    unittest.main()