from . import api
from ihome.utils.captcha.captcha import captcha
from flask import make_response, request, session
from ihome import constants
from flask.json import jsonify
from ihome.utils.response_code import RET
from ronglian_sms_sdk import SmsSDK
import random, json
# from ihome.models import User
from datetime import datetime


@api.route("/search_house")
def search_house():
    from ihome.models import House, Order
    from ihome import redis_store
    start_date_str = request.args.get("sd", '')
    end_date_str = request.args.get("ed", '')
    aid = request.args.get("aid", '')
    sort = request.args.get("sort", '')
    page = request.args.get('page', )

    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    except Exception as e:
        start_date = None

    try:
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    except Exception as e:
        end_date = None

    if start_date and end_date and end_date < start_date:
        end_date = start_date

    try:
        page = int(page)
    except Exception as e:
        page = 1

    redis_key = "houses_%s_%s_%s_%s" % (start_date_str, end_date_str, aid, sort)

    try:
        resp_json = redis_store.hget(redis_key, page)
    except Exception as e:
        resp_json = None
    if resp_json:
        return jsonify(errno=RET.OK, errmsg="bingo", data=resp_json.decode())

    filter_li = []
    if aid:
        # try:
        #     area = Area.query.filter(Area.id==aid).first()
        # except Exception as e:
        #     return jsonify(errno=RET.PARAMERR,errmsg='aid is error')
        filter_li.append(House.area_id == aid)

        # 处理时间
    try:
        conflict_orders_li = []
        if start_date and end_date:
            # 从订单表中查询冲突的订单，进而获取冲突的房屋id
            conflict_orders_li = Order.query.filter(Order.begin_date <= end_date, Order.end_date >= start_date).all()
        elif start_date:
            # 从订单表中查询冲突的订单，进而获取冲突的房屋id
            conflict_orders_li = Order.query.filter(Order.end_date >= start_date).all()
        elif end_date:
            # 从订单表中查询冲突的订单，进而获取冲突的房屋id
            conflict_orders_li = Order.query.filter(Order.begin_date <= end_date).all()
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg="数据库异常")

    if conflict_orders_li:
        conflict_house_id_li = [order.house_id for order in conflict_orders_li]
        # 添加条件，查询不冲突的房屋
        filter_li.append(House.id.notin_(conflict_house_id_li))

    # 排序
    if sort == "booking":
        house_li = House.query.filter(*filter_li).order_by(House.order_count.desc())
    elif sort == "price-inc":
        house_li = House.query.filter(*filter_li).order_by(House.price.asc())
    elif sort == "price-desc":
        house_li = House.query.filter(*filter_li).order_by(House.price.desc())
    else:
        house_li = House.query.filter(*filter_li).order_by(House.create_time.desc())

    # 分页
    try:
        house_page = house_li.paginate(page, constants.EVERY_PAGE_NUM, False)
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg="sql_alchemy Error")

    house_li = house_page.items
    total_page = house_page.pages

    houses = []
    for house in house_li:
        houses.append(house.to_dict())

    house_data = {"houses": houses,
             "total_page": total_page,
             'current_page': page}
    # print(type(houses), type(total_page), type(page))
    resp_json = json.dumps(house_data)

    redis_key = "houses_%s_%s_%s_%s" % (start_date_str, end_date_str, aid, sort)
    pipeline = redis_store.pipeline()
    pipeline.multi()
    pipeline.hset(redis_key, page, resp_json)
    pipeline.expire(redis_key, constants.HOUSE_PAGES_EX)
    pipeline.execute()

    return jsonify(errno=RET.OK, errmsg="bingo", data={"houses": houses,
                                                       "total_page": total_page,
                                                       'current_page': page})
