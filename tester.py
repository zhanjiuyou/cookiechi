# 此文件为cookies得测试文件

from save import RedisClient
import json
import requests

# 测试URL
TEST_URL_MAP = {
    'cf':'https://cf.qq.com/cp/a20210111cattle/pc/index.shtml',
}

# 写一个测试模块父类
class ValidTester(object):
    def __init__(self,website='default'):
        self.website = website
        self.cookies_db = RedisClient('cookies',self.website)
        self.accounts_db = RedisClient('accounts',self.website)
        self.header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
        }

    # 测试cookies，这块用子类重写
    def test(self,username,cookies):
        raise NotImplementedError

    # 获取所有得cookies进行测试
    def run(self):
        cookies_groups = self.cookies_db.all()
        for username,cookies in cookies_groups.items():
            self.test(username,cookies)

class CfValidTester(ValidTester):
    def __init__(self,website='cf'):
        ValidTester.__init__(self,website)

    def test(self,username,cookies):
        print('开始测试cookies','用户名：',username)
        try:
            cookies = json.loads(cookies)
        except TypeError:
            print('cookie不合法',username)
            self.cookies_db.delete(username)
            print('删除cookies',username)
            return

        try:
            # 调取对应得测试链接
            test_url = TEST_URL_MAP[self.website]
            response = requests.get(test_url,headers=self.header,cookies=cookies,timeout=5,allow_redirects=False)
            if response.status_code == 200:
                print('cookies有效',username)
            else:
                print(response.status_code,response.headers)
                print('cookies已失效',username)
                self.cookies_db.delete(username)
                print('删除cookies',username)

        except ConnectionError as e:
            print('发生异常',e.args)

a = CfValidTester()
a.run()