
import redis


class BaseConfig(object):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@127.0.0.1:3306/my_home4'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SECRET_KEY='FUCK'

    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    SESSION_TYPE='redis'
    SESSION_USE_SIGNER =True
    SESSION_REDIS= redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT)
    PERMANENT_SESSION_LIFETIME= 86400



class DevelopPattern(BaseConfig):
    DEBUG = True



class ProductPattern(BaseConfig):
    pass


ConfigDict = {"develop":DevelopPattern,
              "product":ProductPattern}
