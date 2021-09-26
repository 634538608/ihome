from ihome.api_0_1 import api
from flask import session,request,g,json
from flask.json import jsonify
from ihome.utils.response_code import RET
import re
from ihome import constants
from ihome.utils.commons import check_login


@api.route("/orders")
@check_login
def orders():
    print("orders")
    user_id = g.user_id
    from ihome.models import Order
    try:
        orders = Order.query.filter(Order.user_id==user_id).order_by(Order.update_time.desc()).all()
    except Exception as e:
        return jsonify(errno=RET.DBERR,errmsg="mysql error 1")
    orders_li = []
    if orders:
        for ord in orders:
            orders_li.append(ord.to_dict())
    # orders_json = json.dumps(orders_li)
    # print(jsonify(errno=RET.OK, errmsg="bingo", data={"orders":None }))
    return jsonify(errno=RET.OK, errmsg="bingo", data={"orders":orders_li})



@api.route("/accept_order<int:order_id>",methods=["PUT"])
@check_login
def accept_order(order_id):

    from ihome.models import Order
    from ihome import db
    try:
        order = Order.query.filter(Order.id==order_id).first()
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg="Mysql error 1")
    if not order:
        return jsonify(errno=RET.NODATA, errmsg="the order does nt exist")
    try:
        order.status ="WAIT_PAYMENT"
        db.session.commit()
    except Exception as e:
        db.session.rollack()
        return jsonify(errno=RET.DBERR, errmsg="Mysql error 2")

    return jsonify(errno=RET.OK, errmsg="bingo")


@api.route("/refuse_order<int:order_id>", methods=["PUT"])
@check_login
def refuse_order(order_id):
    refuse_reason = request.get_json().get("refuse_reason")
    if not refuse_reason:
        return jsonify(errno=RET.PARAMERR, errmsg="lack of parameter")

    from ihome.models import Order
    from ihome import db
    try:
        order = Order.query.filter(Order.id == order_id).first()
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg="Mysql error 1")
    if not order:
        return jsonify(errno=RET.NODATA, errmsg="the order does nt exist")
    try:
        order.status = "REJECTED"
        order.comment = refuse_reason
        db.session.commit()
    except Exception as e:
        db.session.rollack()
        return jsonify(errno=RET.DBERR, errmsg="Mysql error 2")

    return jsonify(errno=RET.OK, errmsg="bingo")

