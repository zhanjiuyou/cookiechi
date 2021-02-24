#  该文件为总体得调度模块

import time
from tester import *
from save import *
from getter import *
from api import *
from multiprocessing import Process

API_HOST = '127.0.0.1'
API_PORT = 5000
# 产生器和验证器循环周期
CYCLE = 120

# 测试模块，后期将新增拓展可加到里面
TESTER_MAP = {
    'cf':'CfValidTester'
}
# 为了实现扩展性，这里后期将其他cookie池添加进来调用
GENERATE_MAP = {
    'cf':'CfCookiesGenerator'
}
# 产生器开关，模拟登录添加Cookies
GENERATOR_PROCESS = False
# 验证器开关，循环检测数据库中Cookies是否可用，不可用删除
VALID_PROCESS = False
# API接口服务
API_PROCESS = False


class Scheduler(object):
    @staticmethod
    def valid_cookie(cycle=CYCLE):
        while True:
            print('Cookies检测进程开始运行')
            try:
                for website,cls in TESTER_MAP.items():
                    tester = eval(cls + '(website="'+ website +'")')
                    tester.run()
                    print('Cookies检测完成')
                    del tester
                    time.sleep(cycle)
            except Exception as e:
                print(e.args)

    @staticmethod
    def generate_cookie(cycle=CYCLE):
        while True:
            print('Cookies生成进程开始运行')
            try:
                for website, cls in GENERATE_MAP.items():
                    # 这里使用eval函数根据不同得字符组成不用得调用函数。例如CfCookies(website="cf")
                    generator = eval(cls + '(website="' + website + '")')
                    generator.run()
                    time.sleep(20)
                    print('Cookies生成完成')
                    generator.close()
                    time.sleep(cycle)
            except Exception as e:
                print(e.args)

    @staticmethod
    def api():
        print('API接口开始运行')
        app.run(host=API_HOST,port=API_PORT)

    def run(self):
        if API_PROCESS:
            api_process = Process(target=Scheduler.api)
            api_process.start()
        if GENERATOR_PROCESS:
            generate_process = Process(target=Scheduler.generate_cookie)
            generate_process.start()
        if VALID_PROCESS:
            valid_process = Process(target=Scheduler.valid_cookie)
            valid_process.start()



