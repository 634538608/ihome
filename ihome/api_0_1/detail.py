from . import api
from ihome.utils import store_img,commons
from flask import make_response, request,session,g
from ihome import constants
from flask.json import jsonify
from ihome.utils.response_code import RET
from ronglian_sms_sdk import SmsSDK
import random,json


@api.route("/detail<int:house_id>")
def house_detail(house_id):
    user_id = session.get("user_id")

    if not house_id:
        return jsonify(errno=RET.NODATA,errmsg='on data')
    from ihome.models import House
    try:
        house = House.query.filter_by(id=house_id).first()
    except Exception as e:
        return jsonify(errno=RET.DBERR,errmsg='mysql error')
    if not house:
        return jsonify(errno=RET.NODATA, errmsg='on data')
    house_dict = house.to_full_dict()
    print(house_dict)
    return jsonify(errno=RET.OK, errmsg='Bongo',data={"house_detail":house_dict,
                                                      "user_id":user_id})