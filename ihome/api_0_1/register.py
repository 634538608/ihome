from . import api
from ihome.utils.captcha.captcha import captcha
from flask import make_response, request,session
from ihome import constants
from flask.json import jsonify
from ihome.utils.response_code import RET
from ronglian_sms_sdk import SmsSDK
import random,json
# from ihome.models import User

@api.route("/img_code/<img_code_id>")
def img_code(img_code_id):
    name, text, img_data = captcha.generate_captcha()
    from ihome import redis_store
    try:
        redis_store.setex("img_code_%s" % img_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg="redis error")

    resp = make_response(img_data)

    resp.headers["Content-Type"] = 'image/jpg'
    return resp


@api.route("/mobile_code/<re(r'1[35678]\d{9}'):phone_num>", )
def mobile_code(phone_num):
    verify_code = request.args.get("code")
    verify_code_id = request.args.get("codeId")

    print((phone_num, verify_code, verify_code_id))
    if not all((phone_num, verify_code, verify_code_id)):
        return jsonify(errno=RET.NODATA, errmsg="not all data")

    from ihome import redis_store
    try:
        real_code = redis_store.get("img_code_%s" % verify_code_id)
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg="redis error")

    if not real_code:
        return jsonify(errno=RET.NODATA, errmsg="verify_code expire")


    if verify_code.lower() != real_code.decode().lower():
        try:
            redis_store.delete("img_code_%s" % verify_code_id)
        except Exception as e:
            return jsonify(errno=RET.DBERR, errmsg="redis error")
        return jsonify(errno=RET.PARAMERR, errmsg="verify wrong")


    msg_text = "%06d" % random.randint(0, 999999)


    try:
        redis_store.setex("phone_num_%s"%phone_num,constants.MESSAGE_CODE_REDIS_EXPIRES,msg_text)
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg="redis error")



    datas = (msg_text, constants.YunTongXun.EX_TIME)

    sdk = SmsSDK(constants.YunTongXun.ACCID,
                 constants.YunTongXun.ACCTOKEN,
                 constants.YunTongXun.APPID)
    try:
        tmp = sdk.sendMessage(constants.YunTongXun.TID,
                              constants.YunTongXun.MOBILE,
                              datas)
    except Exception as e:
        return jsonify(errno=RET.THIRDERR, errmsg=" message not send")

    if json.loads(tmp)["statusCode"] !="000000":
        return jsonify(errno=RET.THIRDERR, errmsg="send message fail")
    else:
        return jsonify(errno=RET.OK, errmsg="bingo")



@api.route("/register",methods=["POST"])
def register():
    tmp_dict = request.get_json()
    mobile = tmp_dict ["mobile"]
    phoneCode = tmp_dict["phoneCode"]
    pwd = tmp_dict["passwd"]
    pwd2=tmp_dict["passwd2"]

    if not all((mobile,phoneCode,pwd,pwd2)):
        return jsonify(errno=RET.PARAMERR, errmsg="data not all")

    from ihome import redis_store
    try:
        real_code=redis_store.get("phone_num_%s"%mobile)
        print('real_code:',real_code)
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg="redis error")

    if not real_code:
        return jsonify(errno=RET.NODATA, errmsg="code expire")

    if phoneCode != real_code.decode():
        try:
            redis_store.delete("phone_num_%s" % mobile)
        except Exception as e:
            return jsonify(errno=RET.DBERR, errmsg="redis error")
        return jsonify(errno=RET.NODATA, errmsg="code expire")

    if pwd != pwd2:
        return jsonify(errno=RET.PARAMERR, errmsg="The passwords are different")

    from ihome.models import User
    from ihome import db

    user = User(name=mobile,mobile=mobile)
    user.password=pwd


    db.session.add(user)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="mysql error")

    session['user_id']=user.id
    session['user_name']=user.name
    session['mobile'] = mobile
    print(session.keys())

    return jsonify(errno=RET.OK, errmsg="bingo")
























