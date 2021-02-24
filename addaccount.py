# 此文件用来添加我们自己的账号到redis中
# 创建cookie池肯定会用到大量的账号，所以我们这边以txt文件为例，不用我们手动输入了
# 将事先申请好的账号密码保存到txt文件中，格式为：账号---密码，然后直接读取就行
# 默认放到同路径下的account.txt中，

from save import RedisClient

# 先实例化Readis类，参入key名字
conn = RedisClient('account','cf')

def readaccount(sp='----'):
    print('开始读取读取account.txt文件......')
    with open("account.txt","r") as f:
        datas = f.readlines()
        # readlinses方法是将txt文件中的内容以列表形式输出
        for data in datas:
            # 由于txt文件中自带\n，所以我们先去除换行符然后分割账号密码
            account,password=data.strip('\n').split(sp)
            print("正在导入账号:%s   密码:%s" %(account,password))
            # 调用我们实现写好的set方法将账号密码储存到redis中
            result = conn.set(account,password)
            print('导入成功\n' if result else '导入失败')

if __name__ == "__main__":
    readaccount()