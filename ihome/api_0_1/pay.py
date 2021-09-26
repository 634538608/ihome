from . import api
from ihome.utils.commons import check_login
from flask import g, current_app, jsonify, request
from ihome.utils.response_code import RET
from alipay import AliPay
import os
from ihome import constants


@api.route("/pay_message<int:order_id>")
@check_login
def pay_message(order_id):
    user_id = g.user_id
    from ihome.models import Order
    try:
        order = Order.query.filter(Order.id==order_id, Order.user_id == user_id, Order.status == "WAIT_PAYMENT").first()
        print(order)
    except Exception as e:
        return jsonify(errnno=RET.DBERR,errmsg="mysql_error")
    if not order:
        return jsonify(errnno=RET.NODATA,errmsg="the order does not exit")

    #构造支付宝工具对象
    alipay_client = AliPay(
        appid= constants.ALIPAY_APPID,
        app_notify_url=None,  # 默认支付宝通知url
        app_private_key_string=os.path.join(os.path.dirname(os.getcwd()), "keys/app_private_key.pem"),
        alipay_public_key_string=os.path.join(os.path.dirname(os.getcwd()), "keys/alipay_public_key.pem"),  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False, 如果是沙箱模式，debug=True
    )

    order_string = alipay_client.api_alipay_trade_wap_pay(
        out_trade_no=order_id,  # 我们自己的订单编号
        total_amount=str(order.amount / 100.0),  # 订单总金额
        subject=u"爱家租房-%s" % order_id,  # 展示给用户的订单信息
        return_url="http://127.0.0.1:5000/payComplete.html",  # 支付完成后跳转回的页面路径
        notify_url=None  # 可选, 不填则使用默认notify url
    )

    # 用户要访问的支付宝链接地址
    alipay_url = constants.ALIPAY_PAY_URL_PREFIX + "?" + order_string

    return jsonify(errno=RET.OK, errmsg="OK", data={"alipay_url": alipay_url})



