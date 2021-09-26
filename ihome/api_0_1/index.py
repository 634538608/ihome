from ihome.api_0_1 import api
from flask import session,request,g,json
from flask.json import jsonify
from ihome.utils.response_code import RET
import re
from ihome import constants
from ihome.utils.commons import check_login

@api.route('/login',methods=["POST"])
def login():
    tmp_dict = request.get_json()
    mobile =tmp_dict ['mobile']
    passwd = tmp_dict['passwd']

    if not all((mobile,passwd)):
        return jsonify(errno=RET.PARAMERR,
                       errmsg='data not all')

    if not re.match(r"1[34578]\d{9}",mobile):
        return jsonify(errno=RET.DATAERR,
                       errmsg='mobile is wrong')
    from ihome.models import User
    print(mobile)
    try:
        user = User.query.filter_by(mobile=mobile).first()
        print(user)
    except Exception as e:
        return jsonify(errno=RET.DBERR,
                       errmsg='mysql error')

    if not user:
        return jsonify(errno=RET.NODATA,
                       errmsg='this mobile not register')

    if not user.check_password(passwd):
        from ihome import redis_store
        login_count = redis_store.get("login_count_%s"%mobile)

        if login_count :
            login_count+=1
        else:
            login_count=1
        try:
            redis_store.setex("login_count_%s"%mobile,constants.LOGIN_WAIT_TIME,login_count)
        except Exception as e :
            return jsonify(errno=RET.DBERR,
                           errmsg="redis error")

        if login_count>5:
            print("exceed max login times")
            return jsonify(errno=RET.USERERR,
                       errmsg="exceed max login times")


    session['user_id'] = user.id
    session['user_name'] = user.name
    session['mobile'] = mobile

    return jsonify(errno=RET.OK,
                       errmsg='bingo')




@api.route('/check_index_login')
@check_login
def check_index_login():
    user_name = g.get('user_name')
    print('user_name',user_name)
    return jsonify(errno=RET.OK,errmsg='bingo',data={'user_name':user_name})


# @api.route('/areas')
# def areas():
#
#
#     from ihome.models import Area
#     try:
#         all_area = Area.query.all()
#     except Exception as e:
#         return jsonify(errno=RET.DBERR, errmsg='mysql error')
#     areas=[]
#     for a in all_area:
#         areas.append(a.to_dict())
#     return jsonify(errno=RET.OK,errmsg='bingo',data={'areas':areas})


@api.route('/areas')
def areas():

    from ihome import redis_store

    areas = redis_store.get("areas_dict")
    if areas :
        areas=areas.decode()
    else:
        from ihome.models import Area
        try:
            all_area = Area.query.all()
        except Exception as e:
            return jsonify(errno=RET.DBERR, errmsg='mysql error')
        areas_li=[]
        for a in all_area:
            areas_li.append(a.to_dict())


        areas = json.dumps(areas_li)
        print('json')

        try:
            redis_store.setex('areas_dict',constants.AREAS_REDIS_EX,areas)
        except Exception as e:
            return jsonify(errno=RET.DBERR, errmsg='redis error')
        print("mysql_area:",type(areas))
    print("redis_area:",type(areas))
    return '{"errno": 0, "errmsg": "查询城区信息成功", "data":{"areas": %s}}' % areas, 200, {"Content-Type": "application/json"}




@api.route("/index_house")
def index_house():

    from ihome.models import House
    from ihome import redis_store
    try:
        houses = redis_store.get("houses_dict")
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg='redis error 1')
    if houses:
        houses=houses.decode()
    if not houses:

        try:
            houses_m = House.query.order_by(House.order_count.desc()).limit(constants.HOUSE_INDEX_MAX_COUNT)
        except Exception as e :
            return jsonify(errno=RET.DBERR, errmsg='mysql error')

        houses_li = []
        for h in houses_m:
            houses_li.append(h.to_dict())

        houses = json.dumps(houses_li)
        try:
            redis_store.setex("houses_dict",constants.HOUSE_INDEX_REDIS_EX,houses)
        except Exception as e:
            return jsonify(errno=RET.DBERR, errmsg='redis error 2')

    print(type(houses))
    return '{"errno": 0, "errmsg": "bingo", "data":{"houses": %s}}' % houses, 200, {"Content-Type": "application/json"}



