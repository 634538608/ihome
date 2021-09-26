from . import api
from ihome.utils import store_img,commons
from flask import make_response, request,session,g
from ihome import constants
from flask.json import jsonify
from ihome.utils.response_code import RET
from ronglian_sms_sdk import SmsSDK
import random,json

@api.route("/profile_photo",methods=["POST"])
@commons.check_login
def profile_photo():
    user_id = g.user_id
    file_data = request.files.get('avatar')

    if not  file_data:
        return jsonify(errno=RET.NODATA,errmsg="no image data")
    # print(file_data)
    img_data = file_data.read()
    # print(img_data)
    try:
        img_url = store_img.storage_img(img_data)
    except Exception as e:
        # print("e",e)
        return jsonify(errno=RET.THIRDERR,errmsg="qiqiu error")

    # print('img_url',img_url)
    from ihome.models import User
    from ihome import db
    try:
        User.query.filter_by(id=user_id).update({"avatar_url":img_url})
        db.session.commit()
    except Exception as e:
        return jsonify(errno=RET.DBERR,errmsg="mysql error")

    img_url = constants.QINIU_IMG_PREFIX+img_url

    # print(img_url)
    return jsonify(errno=RET.OK, errmsg="bingo",data={"avatar":img_url,
                                                      'user_id':user_id})

@api.route('/user_name',methods=["POST"])
@commons.check_login
def user_name():
    user_id = g.user_id
    user_name = request.get_json()['user_name']

    if not  user_name:
        return jsonify(errno=RET.NODATA,errmsg="no user_name")

    from ihome.models import User
    from ihome import db
    try:
        User.query.filter_by(id=user_id).update({"name": user_name})
        db.session.commit()
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg="mysql error")

    return jsonify(errno=RET.OK, errmsg="bingo", data={'user_name':user_name
                                                       })

@api.route('/profile')
@commons.check_login
def profile():
    print('profile')
    user_id = g.user_id
    from ihome.models import User
    try:
       user =  User.query.filter_by(id=user_id).first()
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg="mysql error")
    avatar_url = user.avatar_url
    if avatar_url is not None:
        avatar_url = constants.QINIU_IMG_PREFIX +avatar_url
    data = {'user_name': g.user_name,
            'avatar_url': avatar_url
            }
    print(data)
    return jsonify(errno=RET.OK, errmsg="bingo", data={'user_name':g.user_name,
                                                       'avatar_url':avatar_url
                                                       })

