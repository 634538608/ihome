from flask import  Blueprint,current_app,make_response
from  flask_wtf.csrf import generate_csrf

web_html = Blueprint("web_Html",__name__)

@web_html.route("/<re(r'.*'):file_name>")
def index(file_name):
    if not file_name:
        file_name="index.html"
    if file_name != "favicon.ico":
        file_name = "html/"+ file_name

    resp = make_response(current_app.send_static_file(file_name))
    csrf_token = generate_csrf()
    print(csrf_token)
    resp.set_cookie("csrf_token",csrf_token)





    return resp