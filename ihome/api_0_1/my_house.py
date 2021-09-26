from . import api
from ihome.utils import store_img,commons
from flask import make_response, request,session,g
from ihome import constants
from flask.json import jsonify
from ihome.utils.response_code import RET
from ronglian_sms_sdk import SmsSDK
import random,json

@api.route('/my_house')
@commons.check_login
def my_house():
    user_id = g.user_id

    from ihome.models import House
    # try:
    #     user = User.query.filter_by(id=user_id).first()
    # except Exception as e:
    #     return jsonify(errno=RET.DBERR,errmsg='mysql error 1')
    #
    # real_name = user.real_name
    # id_card = user.id_card
    #
    # if not  all((real_name,id_card)):
    #     return jsonify(errno=RET.USERERR, errmsg='user not auth')
    houses_li =[]
    try:
        houses = House.query.filter_by(user_id=user_id).all()

    except Exception as e:
        return jsonify(errno=RET.DBERR,errmsg='mysql error 1')

    for h in houses:
        houses_li.append(h.to_dict())
    print(houses_li)
    return jsonify(errno=RET.OK, errmsg='Bingo',data={"houses":houses_li})
