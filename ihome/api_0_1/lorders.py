
from ihome.api_0_1 import api
from flask import session,request,g,json
from flask.json import jsonify
from ihome.utils.response_code import RET
import re
from ihome import constants
from ihome.utils.commons import check_login
@api.route("/lorder")
@check_login
def lorder():
    user_id = g.user_id

    from ihome.models import Order,House

    try:
        houses = House.query.filter(House.user_id==user_id).all()
    except Exception as e:
        return jsonify(errno =RET.DBERR,errmsg="mysql error 1")
    if not houses:
        return jsonify(errno=RET.OK, errmsg="bingo", data={"orders": None})

    house_id_li = []
    for house in houses:
        house_id_li.append(house.id)

    try:
        orders = Order.query.filter(Order.house_id.in_(house_id_li)).all()
    except Exception as e:
        return jsonify(errno =RET.DBERR,errmsg="mysql error 1")

    orders_li = []
    if orders:
        for order in orders:
            orders_li.append(order.to_dict())

    print(orders_li)
    return jsonify(errno=RET.OK, errmsg="bingo", data={"orders":orders_li})

