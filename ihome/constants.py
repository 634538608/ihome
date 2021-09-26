
# 图片验证码Redis中存储的时间
IMAGE_CODE_REDIS_EXPIRES = 300
#短信验证码Redis中存储的时间
MESSAGE_CODE_REDIS_EXPIRES = 300
class YunTongXun(object):
    """
    #https://doc.yuntongxun.com/p/5f029ae7a80948a1006e776e
        tid	String	短信模板 ID
        mobile	String	发送手机号，多个以英文逗号分隔，最多 200 个号码
        datas	tuple	替换短信模板占位符的内容变量
        响应参数
        {"statusCode":"000000",
        "templateSMS":{"dateCreated":"20130201155306",
        "smsMessageSid":"ff8080813c373cab013c94b0f0512345"}}
        statusCode	String	状态码，000000 为发送成功,172001	网络错误
        dateCreated	String	短信的创建时间，格式：yyyyMMddHHmmss
        smsMessageSid	tuple	短信唯一标识符

        免费开发测试使用的模板ID为1，具体内容：【云通讯】您的验证码是{1}，请于{2}分钟内正确输入。其中{1}和{2}为短信模板参数。
        """
    ACCID = '8aaf07086f0d2ca0016f1197eef8033f'
    ACCTOKEN = "a5c663c31ce44edda90749fbca8fa84f"
    APPID = "8aaf07086f0d2ca0016f1197ef510345"
    TID = 1
    MOBILE= "13125088778"
    EX_TIME = 5


#密码输入错误超过五次后就跳转到主页 5分钟后再试
MAX_LOGIN_COUNT=5
LOGIN_WAIT_TIME = 300


# 七牛云上传后图片访问前缀
QINIU_IMG_PREFIX="http://qxrhn62fe.hd-bkt.clouddn.com/"
# 七牛云用法：https://developer.qiniu.com/kodo/1242/python
# 上传的空间的名字
QINIU_BUCKET_NAME = "my-home2"



#areas 在redis 中的缓存过期时间
AREAS_REDIS_EX = 300

# from flask import g
#
# print(g.get("user_id"))
#首页上展示房间数量
HOUSE_INDEX_MAX_COUNT=6
#首页上展示的房间数量在redis上缓存过期时间
HOUSE_INDEX_REDIS_EX = 300
#房屋细节展示评论数量
HOUSE_DETAIL_COMMENT_DISPLAY_COUNTS=5

#单个房屋dict 缓存时间
HOUSE_DICT_EX=300

#alipay
# https://opendocs.alipay.com/open/200/105311 沙箱文档
# openssl  //生成公钥私钥
# OpenSSL> genrsa -out app_private_key.pem 2048  # 私钥RSA2
# OpenSSL> rsa -in app_private_key.pem -pubout -out app_public_key.pem # 导出公钥
#
# OpenSSL> exit
#
#安装 alipay sdk   pip install python-alipay-sdk --upgrade

ALIPAY_APPID="2021000118613314"
ALIPAY_PAY_URL_PREFIX="https://openapi.alipaydev.com/gateway.do"


EVERY_PAGE_NUM=2
HOUSE_PAGES_EX= 300