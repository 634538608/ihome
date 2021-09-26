from . import api
from ihome.utils import commons
from flask import session,g
from ihome import constants
from flask.json import jsonify
from ihome.utils.response_code import RET



@api.route('/my')
@commons.check_login
def my():
    user_id = g.user_id
    user_name = g.user_name
    mobile = g.mobile
    from ihome.models import User
    try:
       user =  User.query.filter_by(id=user_id).first()
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg="mysql error")
    avatar_url = user.avatar_url
    if avatar_url is not None:
        avatar_url = constants.QINIU_IMG_PREFIX +avatar_url
    return jsonify(errno=RET.OK, errmsg="bingo", data={'user_name': user_name,
                                                       'mobile': mobile,
                                                       'avatar_url':avatar_url})



@api.route('/logout',methods=["DELETE"])
@commons.check_login
def logout():
    session.clear()
    return jsonify(errno=RET.OK, errmsg="bingo")

