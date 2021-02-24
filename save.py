# 此文件为储存模块，主要是将获取的cookie加载到redis中
# 将redis中hash的用法封装为一个个函数
# 2021.1.10


import redis
import random

# 先设置链接的IP和端口

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None

# 将redis的方法进行封装成类
class RedisClient(object):
    # 实例化类
    def __init__(self,type,website,host=REDIS_HOST,port=REDIS_PORT,password=REDIS_PASSWORD):
        self.db = redis.StrictRedis(host=host,port=port,password=password,decode_responses=True)
        self.type = type  # 这块为储存的类型
        self.website = website  # 这块是网站的名称，例如我们存新浪的，可以命名为xinlang

    # 后期为了相同用户名的密码和cookie等进行映射，这里我们使用redis中hash

    # 写一个名字函数
    def name(self):
        # 生成名字
        return "{type}:{website}".format(type=self.type,website=self.website)

    # 设置键值对，usename为用户名，value为密码或者cookie值
    def set(self,usename,value):
        # 给对应的key赋值用户名和值
        return self.db.hset(self.name(),usename,value)

    # 根据key中的键名获取值
    def get(self,usename):
        return self.db.hget(self.name(),usename)

    # 根据键名删除键值对
    def delete(self,usename):
        return self.db.hdel(self.name(),usename)

    # 获取数目
    def count(self):
        return self.db.hlen(self.name())

    # 随机得到键值，这里我们用来获取cookies
    def random(self):
        # 这里使用random的choice方法随机获取，里面的方法为hash获取所有的值
        return random.choice(self.db.hvals(self.name()))

    # 获取所有账户信息，获取所有的账户名,也就是所有的键
    def usernames(self):
        return self.db.hkeys(self.name())

    # 获取所有的键值对
    def all(self):
        # 获取所有的键值对，可以用来获取账号密码或者账号对应的cookies
        return self.db.hgetall(self.name())


