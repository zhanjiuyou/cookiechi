# 此文件为我们对应网站的cookie获取
# 使用selenium来动态抓取网页

from selenium import webdriver
# 下面这个模块是判断页面加载完毕用的,是显示等待
from selenium.webdriver.support.wait import WebDriverWait
# 该模块用来判断元素是否存在或是否点击，这个和上面的模块一般都是组合使用
from selenium.webdriver.support import expected_conditions as EC
# By是内置的class，定义了很多方法
from selenium.webdriver.common.by import By
import selenium.common.exceptions as ex
import time

class CfCookies():
    def __init__(self,username,password,browser):
        self.url = 'https://cf.qq.com/cp/a20210111cattle/pc/index.shtml'
        # 这里将brower单独重新定义主要用于不同得浏览器调用
        self.browser = browser
        # 设置浏览器最长等待时间，这里我们设置为10秒
        self.wait = WebDriverWait(browser,10)
        self.username = username
        self.password = password

# 这里开始进行浏览器得操作
    def open(self):
        # 打开浏览器
        self.browser.get(self.url)
        # 用显示等待，定位并点击登录按钮
        self.wait.until(EC.presence_of_element_located((By.ID,'dologin'))).click()
        # 点击登录按钮后，弹出QQ得登录页面，这里iframe嵌套页面，切换到子页面
        self.browser.switch_to.frame('loginIframe')
        # 选择账号密码登录按钮，并点击
        self.wait.until(EC.presence_of_element_located((By.ID,'switcher_plogin'))).click()
        # 定位到账号和密码输入框，并输入账号密码
        self.wait.until(EC.presence_of_element_located((By.ID,'u'))).send_keys(self.username)
        self.wait.until(EC.presence_of_element_located((By.ID,'p'))).send_keys(self.password)
        time.sleep(2)
        # 点击登录
        self.wait.until(EC.presence_of_element_located((By.ID,"login_button"))).click()

        # 点击登录后，会弹出验证码，由于验证码更新换代太快，以往得破解方法不适用，这里我们手动完成

    # 该函数判断密码账号是否输入错误,如果错误或超时返回False
    def password_error(self):
        try:
            # 当密码错误时会弹出一个提示，我们只需捕获这个错误提示就知道是否输入错误
            return bool(self.wait.until(EC.presence_of_element_located((By.ID,'err_m'))))
        except ex.TimeoutException:
            return False

    # 获取cookies
    def get_cookies(self):
        return self.browser.get_cookies()

    # 判断是否登录成功。
    def login_successfully(self):
        # 当登录成功后会出现注销按钮，我们只需判断这个即可
        try:
            return bool(self.wait.until(EC.presence_of_element_located((By.ID,"dologout"))))
        except ex.TimeoutException:
            return False

    # 这里对整个获取流程运行
    def main(self):
        self.open()
        # 登录账号后，记得手动滑动验证码
        time.sleep(10)
        # 判断是否账号密码错误
        if self.password_error():
            return {
                'status':2,
                'content':'用户名或密码错误'
            }
        elif self.login_successfully():
            # 如果登录成功，则获取cookies
            cookies = self.get_cookies()
            return {
                'status':1,
                'content':cookies
            }
        else:
            return {
                'status':3,
                'content':'登录失败'
            }

