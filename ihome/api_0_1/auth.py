from . import api
from ihome.utils import store_img,commons
from flask import make_response, request,session,g
from ihome import constants
from flask.json import jsonify
from ihome.utils.response_code import RET
from ronglian_sms_sdk import SmsSDK
import random,json
@api.route('/auth')
@commons.check_login
def auth():
    user_id = g.user_id

    from ihome.models import User
    try:
        user = User.query.filter_by(id=user_id).first()
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg="mysql error")
    real_name = user.real_name
    id_card = user.id_card
    if not  all((real_name,id_card)):
        return jsonify(errno=RET.NODATA, errmsg="user not auth")

    return jsonify(errno=RET.OK, errmsg="bingo")


@api.route('/user_auth',methods=["POST"])
@commons.check_login
def user_auth():
    tmp_dict = request.get_json()
    real_name = tmp_dict['real_name']
    id_card = tmp_dict['id_card']

    if not all((real_name,id_card)):
        return jsonify(errno=RET.PARAMERR, errmsg="data not all")

    user_id = g.user_id
    from ihome.models import User
    from ihome import db
    try:
        User.query.filter_by(id=user_id).update({"real_name":str(real_name),
                                                 "id_card":str(id_card)})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="mysql error")

    return jsonify(errno=RET.OK, errmsg="bingo")





