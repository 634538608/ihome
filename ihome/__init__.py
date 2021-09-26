
from flask import Flask
from config import ConfigDict
from flask_sqlalchemy import SQLAlchemy
from ihome.web_html import web_html
from ihome.utils.commons import Regex_url
from ihome.api_0_1 import api
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
import redis



db = SQLAlchemy()
redis_store = None
csrf = CSRFProtect()

def create_app(config_name):
    app = Flask(__name__)

    # set config
    conf = ConfigDict[config_name]
    app.config.from_object(conf)

    db.init_app(app)

    global redis_store
    redis_store =redis.StrictRedis(host=conf.REDIS_HOST,port=conf.REDIS_PORT)

    # csrf.init_app(app)

    Session(app)

    app.url_map.converters['re'] = Regex_url

    app.register_blueprint(web_html)
    app.register_blueprint(api,url_prefix ="/api/v1.0")

    return app