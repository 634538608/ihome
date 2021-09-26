# -*- coding: utf-8 -*-
# flake8: noqa
"""
# https://developer.qiniu.com/kodo/1242/python
pip install qiniu
AK:WU5oLXGQpI50lzyH9Fzd1vZybLR0nYWOibRWXrkn
SK:UVEOnq0CKPMoVVY4HoocEsHz_8jlx42ajqUHFMBW
AK:MQYsXJ6K2femAgUAlwsqNfqYEaYQw2obdf71A2dx
SK:3CTDGXh0KEga1L8xW7nU6F9wuSlq2IwdELj5e_Z7

"""
from qiniu import Auth, put_data, etag
import qiniu.config
from ihome.constants import QINIU_BUCKET_NAME
# 需要填写你的 Access Key 和 Secret Key
access_key = 'WU5oLXGQpI50lzyH9Fzd1vZybLR0nYWOibRWXrkn'
secret_key = 'UVEOnq0CKPMoVVY4HoocEsHz_8jlx42ajqUHFMBW'
qiqiu_img_prefix="qxrhn62fe.hd-bkt.clouddn.com/"
# 构建鉴权对象

def storage_img(file_data):
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = QINIU_BUCKET_NAME
    # 上传后保存的文件名
    # key = 'my-python-logo.png'
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, None, 3600)
    # 要上传文件的本地路径
    # localfile = './sync/bbb.jpg'
    try:
        ret, info = put_data(token, None, file_data)
    except Exception as e :
        raise   e
    # print(info.status_code,ret)
    if info.status_code ==200:
        print('nfo.status_code',info.status_code)
        print(ret["key"])
        return ret["key"]



#
# if __name__ == '__main__':
#     with open("./12.jpeg","rb") as f:
#         data = f.read()
#     storage_img(data)
