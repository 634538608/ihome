from . import api
from ihome.utils import store_img,commons
from flask import make_response, request,session,g
from ihome import constants
from flask.json import jsonify
from ihome.utils.response_code import RET
from ronglian_sms_sdk import SmsSDK
import random,json
import qiniu




@api.route('/new_house',methods=['POST'])
@commons.check_login
def new_house():
    user_id =g.user_id
    tmp_dict = request.get_json()
    area_id = tmp_dict.get('area_id')
    title= tmp_dict.get('title')
    price= tmp_dict.get('price')
    address= tmp_dict.get('address')
    room_count= tmp_dict.get('room_count')
    acreage= tmp_dict.get('acreage')
    unit= tmp_dict.get('unit')
    capacity= tmp_dict.get('capacity')
    beds= tmp_dict.get('beds')
    deposit= tmp_dict.get('deposit')
    min_days= tmp_dict.get('min_days')
    max_days= tmp_dict.get('max_days')
    facilities= tmp_dict.get('facilities')
    # print(tmp_dict)
    if not  all((area_id,title,price,address,room_count,acreage,
            unit,capacity,beds,deposit,min_days,max_days,
            facilities)):
        return jsonify(errno=RET.PARAMERR,errmsg='data not all')
    from ihome.models import House,Facility
    from ihome import db


    facilities = Facility.query.filter(Facility.id.in_(facilities)).all()
    try:
        db.session.commit()
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg='mysql error f')

    house = House(user_id=user_id,
                  area_id=area_id,
                  title=title,
                  price=price,
                  address=address,
                  room_count=room_count,
                  acreage=acreage,
                  unit=unit,
                  capacity=capacity,
                  beds=beds,
                  deposit=deposit,
                  min_days=min_days,
                  max_days=max_days,
                  facilities=facilities
                  )
    try:
        db.session.add(house)
        db.session.commit()
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg='mysql error h')



    return jsonify(errno=RET.OK, errmsg='bingo', data={"house_id":house.id})

@api.route('/house_img',methods=['POST'])
@commons.check_login
def house_img():
    file_data = request.files.get("house_image")
    house_id = request.form.get("house_id")
    if not all((file_data,house_id)):
        return jsonify(errno=RET.NODATA, errmsg='not a file')
    img_data = file_data.read()

    from ihome.models import HouseImage,House
    from ihome import db

    try:
        house = House.query.filter_by(id=house_id).first()
    except Exception as e :
        return jsonify(errno=RET.DBERR, errmsg='Mysql error')

    if not house:
        return jsonify(errno=RET.PARAMERR, errmsg='The house does not exist ')

    try:
        img_url = store_img.storage_img(img_data)
    except Exception as e:
        return jsonify(errno=RET.THIRDERR, errmsg='qiqiu error')



    house_img = HouseImage(house_id=house_id,url=img_url)
    try:
        db.session.add(house_img)
        db.session.commit()
    except Exception as e :
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='Mysql error')

    if not house.index_image_url:
        # print("index_image_url,1",house.index_image_url)
        try:
            House.query.filter_by(id=house_id).update({"index_image_url": img_url})
            db.session.commit()
        except Exception as e:
            return jsonify(errno=RET.DBERR, errmsg="mysql error")
    # print("index_image_url,2", house.index_image_url)

    return jsonify(errno=RET.OK, errmsg='Bingo',data={"image_url":constants.QINIU_IMG_PREFIX+img_url})


