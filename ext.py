#这步就是调用自己的数据库所用的扩展模块，以防死锁互相调用的问题
from flask_sqlalchemy import SQLAlchemy
#数据库访问对象，应该在app里面和db做链接
db = SQLAlchemy()