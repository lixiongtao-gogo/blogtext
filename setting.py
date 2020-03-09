'''
author = 李雄涛
data = 2020/3/2
当前py文件的作用：
'''

#倒入数据库
SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:12345678@127.0.0.1:3306/Blog'
#不用跟踪数据库的变化
SQLALCHEMY_TRACK_MODIFICATIONS = False
#设置签名加密，虽然不知道干嘛的？
SECRET_KEY = 'sahdhajnnsandjguegeunejdnsnsdshfuasndkasf'
