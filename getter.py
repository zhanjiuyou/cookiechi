# 该文件为cookie获取文件
from selenium import webdriver
from save import RedisClient
from cookies import CfCookies
import json
import time

# 这里我们先写一个通用类，后期不同得网站重新调用父类
class CookiesGenerator(object):
    def __init__(self,website='default'):
        self.website = website
        self.cookies_db = RedisClient('cookies',self.website)
        self.account_db = RedisClient('account',self.website)
        self.init_browser()

    # 当不需要实例得时候我们手动销毁，释放内存
    def __del__(self):
        self.close()

    # 这里对浏览器进行设置，
    def init_browser(self):
        # 如果加上下面两行代码让浏览器在后台静默执行，由于我们要手动验证码所以忽略
        # self.option = webdriver.ChromeOptions()
        # self.option.add_argument('headless')
        self.browser = webdriver.Chrome()

    # 获取cookies，子类到时候自行重写，不然报错
    def new_cookies(self,username,password):
        raise NotImplementedError

    #提取cookies中得name和value重新生产新字典,其他字段无用
    def process_cookies(self,cookies):
        dict = {}
        for cookie in cookies:
            dict[cookie['name']] = cookie['value']
        return dict

    # 运行函数
    def run(self):
        # 导出所有得账号列表
        account_usernames = self.account_db.usernames()
        cookies_usernames = self.cookies_db.usernames()

        # 遍历所有账号，找出没有cookies得账号
        for username in account_usernames:
            if not username in cookies_usernames:
                password = self.account_db.get(username)
                print('正在生成cookies','账号:',username,'密码----')
                result = self.new_cookies(username,password)
                time.sleep(10)
                # 这快利用我们cookies文件生成得状态码判断登录状态,登录正常得获取并保存cookies，错误得则删除账号
                if result.get('status') == 1:
                    cookies = self.process_cookies(result.get('content'))
                    print('成功获取到cookies',cookies)
                    if self.cookies_db.set(username,json.dumps(cookies)):
                        print('成功保存cookies')

                elif result.get('status') == 2:
                    print(result.get('content'))
                    if self.account_db.delete(username):
                        print('成功删除错误账号')

                else:
                    print(result.get('content'))

        else:
            print('所有账号都已成功获取cookies')


    def close(self):
        try:
            print('关闭浏览器')
            self.browser.close()
            del self.browser

        except TypeError:
            print('浏览器关闭失败')

# 继承上面得类，重新子类
class CfCookiesGenerator(CookiesGenerator):
    def __init__(self,website='cf'):
        CookiesGenerator.__init__(self,website)
        self.website = website

    def new_cookies(self,username,password):
        return CfCookies(username,password,self.browser).main()

# a = CfCookiesGenerator()
# a.run()