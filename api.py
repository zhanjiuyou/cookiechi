# 方便后期爬虫调用，这是接口文件

import json
from flask import Flask,g
from save import *

GENERATOR_MAP = {
    'cf':'https://cf.qq.com/cp/a20210111cattle/pc/index.shtml'
}

__all__ = ['app']

app = Flask(__name__)

@app.route('/')
def index():
    return '<h2>欢迎进入cookie池系统</h2>'
def get_conn():
    for website in GENERATOR_MAP:
        print(website)
        #g是个全局对象,利用setattr给该对象设置方法
        if not hasattr(g,website):
            setattr(g,website+'_cookies',eval('RedisClient'+'("cookies","'+website+'")'))
            setattr(g, website + '_accounts', eval('RedisClient' + '("accounts","' + website + '")'))
        return g

@app.route('/<website>/random')
def random(website):
    '''
    获取随机的cookie,访问地址如/zhihu/random
    :param website:站点
    :return:随机cookie
    '''
    g = get_conn()
    # 调用设置号得方法
    cookies = getattr(g,website+'_cookies').random()
    return cookies

def add(website,username,password):
    '''
    添加用户，访问地址如/mafeng/add/user/password
    :param website: 站点
    :param username: 用户名
    :param password: 密码
    :return:
    '''
    g = get_conn()
    print(username,password)
    getattr(g,website+'_accounts').set(username,password)
    return json.dumps({'status':'1'})

@app.route('/<website>/count')
def count(website):
    '''
    获取cookies总数
    :param website:
    :return:
    '''
    g = get_conn()
    count = getattr(g,website+'_cookies').count()
    return json.dumps({'status': '1', 'count': count})

# app.run(host='127.0.0.1',port=5000)