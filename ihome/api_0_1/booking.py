from ihome.api_0_1 import api
from flask import session,request,g,json
from flask.json import jsonify
from ihome.utils.response_code import RET
import re
from ihome import constants
from ihome.utils.commons import check_login


@api.route("/booking<int:house_id>")
def booking_info(house_id):
    print("booking_info")
    if not house_id:
        return jsonify(errno=RET.PARAMERR,errmsg="no parameter")

    from ihome import redis_store
    try:
        house_dict = redis_store.get("house_dict_"+str(house_id))
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg="redis error 1")
    print("redis_dict",type(house_dict))
    if house_dict:
        house_dict=house_dict.decode()

    else:
        from ihome.models import House
        try:
            house =House.query.filter_by(id=house_id).first()
        except Exception as e:
            return jsonify(errno=RET.DBERR,errmsg="mysql error")

        if not house:
            return jsonify(errno=RET.NODATA,errmsg="no data")

        house_dict = house.to_dict()

        house_dict = json.dumps(house_dict)
        print("json_dump:",type(house_dict))
        try:
            redis_store.setex("house_dict_"+str(house_id),constants.HOUSE_DICT_EX,house_dict)
        except Exception as e:
            return jsonify(errno=RET.DBERR, errmsg="redis error 2")
    return '{"errno": 0, "errmsg": "bingo", "data":{"house": %s}}' % house_dict, 200, {"Content-Type": "application/json"}


@api.route("/real_booking" ,methods=["POST"])
@check_login
def real_booking():
    # print('real_booking')
    user_id = g.user_id
    # print(user_id)
    tmp_dict = request.get_json()
    # print(tmp_dict)
    house_id = tmp_dict.get("house_id")
    start_date = tmp_dict.get("start_date")
    end_date = tmp_dict.get("end_date")
    days = tmp_dict.get("days")
    price = tmp_dict.get("price")
    amount = tmp_dict.get("amount")
    print(tmp_dict)
    if not all((user_id,house_id,start_date,end_date,days,price,amount)):
        return jsonify(errno=RET.PARAMERR, errmsg="parameter error")

    from ihome.models import Order
    from ihome import db

    try:
        count = Order.query.filter(Order.house_id==house_id,
                                      Order.begin_date>=end_date,
                                      Order.end_date<=start_date).count()

    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg="mysql error 1")
    if count >0:
        return jsonify(errno=RET.DATAEXIST, errmsg="the house was booked ")

    order = Order(user_id=user_id,
                  house_id=house_id,
                  begin_date=start_date,
                  end_date=end_date,
                  days=days,
                  house_price=price,
                  amount=amount,
                  status="WAIT_ACCEPT")
    try:
        db.session.add(order)
        db.session.commit()
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg="mysql error 2")
    return jsonify(errno=RET.OK, errmsg="bingo")





