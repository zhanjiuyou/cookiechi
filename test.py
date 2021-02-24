from selenium import webdriver
# 下面这个模块是判断页面加载完毕用的,是显示等待
from selenium.webdriver.support.wait import WebDriverWait
# 该模块用来判断元素是否存在或是否点击，这个和上面的模块一般都是组合使用
from selenium.webdriver.support import expected_conditions as EC
# By是内置的class，定义了很多方法
from selenium.webdriver.common.by import By
import time

brower = webdriver.Chrome()
# 设置一个显示等待浏览器加载完毕，最长等待时间10s
wait = WebDriverWait(brower,10)

# 打开浏览器进入CF官网
brower.get('https://cf.qq.com/cp/a20210111cattle/pc/index.shtml')
# 用显示等待定位并点击登录按钮
dologin = wait.until(EC.presence_of_element_located((By.ID,'dologin')))
dologin.click()

# 点击登录按钮后会弹出QQ登录页面，由于是iframe嵌套的，所以先切换到子页面
brower.switch_to.frame("loginIframe")
# 定位到账号密码登录按钮并点击，此时进入账号密码登录窗口
switcher_plogin = wait.until(EC.presence_of_element_located((By.ID,"switcher_plogin")))
switcher_plogin.click()

# 输入账号密码
usename = wait.until(EC.presence_of_element_located((By.ID,"u"))).send_keys("2759728947")
password = wait.until(EC.presence_of_element_located((By.ID,"p"))).send_keys("2321332131")

# 点击登录
login = wait.until(EC.presence_of_element_located((By.ID,"login_button"))).click()

if wait.until(EC.presence_of_element_located((By.ID,'error_logo'))):
    print('账号或密码错误')

# if wait.until(EC.presence_of_element_located((By.ID,"dologout"))):
#
#     cookies = brower.get_cookies()
#     print(cookies)


