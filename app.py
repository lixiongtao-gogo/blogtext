#http://pypi.douban.com/simple/
#pip install flask_srcipt pip -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com
#调用flask中的函数Flask
#通过已有的数据库反向生成
#flask-sqlacodegen mysql+pymysql://root:12345678@127.0.0.1:3306/Blog --outfile model.py --flask

from flask import Flask
#调用
from flask_script import Manager
#从views中调用ac
from views import ac
from ext import db
from flask_moment import Moment


app = Flask(__name__)
#倒入设置文件
app.config.from_pyfile('setting.py')
#初始化数据库访问对象
db.init_app(app)
# 实例化管理器对象，负责接受终端传来的参数，并且解释
manager = Manager(app)
#时间模块
moment = Moment(app)
#注册一下自己的ac
app.register_blueprint(ac)


if __name__ == '__main__':
    manager.run()
