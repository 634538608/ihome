from functools import wraps
from werkzeug.routing import BaseConverter
from flask import session,jsonify,g
from .response_code import RET
class Regex_url(BaseConverter):
    def __init__(self,url_map,*args):
        super(Regex_url,self).__init__(url_map)
        self.regex = args[0]



def check_login(view_func):
    @wraps(view_func)
    def tmp_func(*args,**kwargs):

        user_id = session.get('user_id')
        user_name = session.get('user_name')
        mobile = session.get('mobile')

        if not all((user_id,user_name,mobile)):
            
            return jsonify(errno=RET.LOGINERR,errmsg='not login')

        else:
            g.user_id = user_id
            g.user_name = user_name
            g.mobile = mobile

            return view_func(*args,**kwargs)
    return tmp_func