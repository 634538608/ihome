from flask import Blueprint

api = Blueprint("api_v1.0",__name__)

from . import register,index,profile,my,auth,my_house,\
    new_house,detail,search,booking,orders,lorders,pay,search
