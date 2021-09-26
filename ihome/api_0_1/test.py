from functools import wraps
from flask import  json
from ihome import redis_store

def a(e):
    def b(*args,**kwargs):
        print('b')
        return e(*args,**kwargs)
    return b

@a
def d(x):
    print(x+1)

# d(1)
# print("{'errnno':{},'errmsg':'bingo','data':{'areas':{}}}".format("111","222"))

