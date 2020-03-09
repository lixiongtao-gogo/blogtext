'''
author = 李雄涛
data = 2020/3/4
当前py文件的作用：
'''
# 导入表单,表单验证已经包装好
import re

from flask import session
from flask_wtf import FlaskForm

# 设置一个表单，继承FlaskForm

from wtforms import StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError

from model import User

def check_phone(self,field):
    if not re.match(r'(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$',field.data):
        raise ValidationError("电话号码不符合规则")
    return field

class RegisterForm(FlaskForm):
    # label是一个表格的名字，DataRequited内容为必填,validators(验证器)是这个表格的属性，必填项，长度，类型等
    #表单注册名
    nickname = StringField(label='用户名', validators=[DataRequired('用户名必须输入')])
    #表单注册密码
    password = PasswordField(label='密码', validators=[DataRequired('密码必须输入'),Length(min=3,max=12,message="密码长度必须在3-12位")])
    #重复输入密码
    pwdagain = PasswordField(label='确认密码',validators=[EqualTo('password',message='两次密码输入不同')])
    #因为表单里面的内容必须为输入项（form.py文件里面有邮箱），但是html里面没有邮箱，所以一直就提交不成功
    # email = EmailField(label='邮箱',validators=[Email('邮箱格式错误')])
    phonenum = StringField(label='电话',validators=[check_phone])
    # phonecode = StringField(label='短信验证码',validators=[DataRequired('验证码必须输入')])
    piccode = StringField(label='验证码',validators=[DataRequired('验证码必须输入')])

    #自己设置密码验证：validate_字段名字,第二个是对象，数据是对象的data
    def validate_nickname(self,field):
        # print(field.data)
        user = User.query.filter(User.u_username==field.data).first()
        if user:
            raise ValidationError('用户名重名')


    def validate_piccode(self,field):
        if field.data != session.get('code'):
            raise ValidationError('验证码匹配失败')


    # def validate_phonecode(self,field):
    #     if field.data != session.get('smscode'):
    #         raise ValidationError('短信验证码匹配失败')
    # def validate_phonenum(self,field):
    #     if not re.match(r'(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$',field.data):
    #         raise ValidationError('电话号码不符合规则')
    #     return field


