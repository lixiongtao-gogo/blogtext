# 倒入蓝图，建立自己的程序文档

import hashlib
import os
from datetime import datetime
from random import randint
from wsgiref import headers

from flask import Blueprint, render_template, request, session, redirect, url_for, flash, make_response
from messagesend import sms
from forms import RegisterForm
from model import *


# 自己的程序文档就是ac
# bluesprint里面有一个路由前缀，这样有各自的路由，这样不交叉
from veirfycode import vc

ac = Blueprint('ac', __name__)


# 这样调用的就是ac的函数，增加一个路由
@ac.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.values.get('username')
        password = request.values.get('password')
        # print(username,password)
        user = User.query.filter(User.u_username == username, User.u_psd == password).first()
        if user:
            session['username'] = username
            return redirect(url_for('ac.index'))
        else:
            flash('用户名或者密码错误')
    return render_template('login.htm', **locals())


@ac.route('/registered/', methods=['GET', 'POST'])
def registered():
    form = RegisterForm()
    if request.method == 'POST':
        # 表单提过的的数据
        if form.validate_on_submit():
            try:
                username = form.nickname.data
                password = form.password.data
                phone = form.phonenum.data
                # print(username)
                user = User(u_username=username, u_psd=password)
                # 密码哈希加密
                # user.u_psd = hashlib.sha1(password.encode('utf8')).hesdigest()
                user.u_phone_number = phone
                # 将数据加载到数据库中
                db.session.add(user)
                # 手动提交
                db.session.commit()
                #重定向就是将地址都删除直接到路由指定的函数页面
                return redirect(url_for('ac.login'))
            except:
                return '数据添加失败'
    return render_template('registered.htm', **locals())


@ac.route('/index/')
def index():
    articles = Article.query.all()
    users = User.query.all()
    three_article = Article.query.order_by(-Article.a_create_time).all()[:3]
    return render_template('index.html', **locals())


@ac.route('/blog/')
@ac.route('/blog/<int:c_id>/')
@ac.route('/blog/<int:c_id>/<int:page>')
def blog(c_id=-1,page=1):
    if c_id < 0:
        category = Category.query.first()
        c_id = category.c_id

    # article_cate = db.session.query(Article, Category).filter(Article.c_id == Category.c_id,
    #                                                           Category.c_id == c_id).all()

    paging = db.session.query(Article, Category).filter(Article.c_id == Category.c_id,Category.c_id == c_id)
    pagination = paging.paginate(page,2)
    # print(pagination.__dict__)
    # print(article_cate)
    # article_num = len(article_cate)
    # print(article_num)
    categories = Category.query.all()
    three_article = Article.query.order_by(-Article.a_create_time).all()[:3]
    return render_template('blog.html', **locals())


# @ac.route('/blog/')
# # @ac.route('/blog/<int:c_id>/')
# def blog():
#     categories = Category.query.all()
#     #这句话没动啥意思？？？？？？？
#     article_cate = Article.query.order_by(Article.c_id).all()
#     print(article_cate)
#     three_article = Article.query.order_by(-Article.a_create_time).all()[:3]
#     return render_template('blog.html', **locals())

@ac.route('/post/',methods=['GET','POST'])
@ac.route('/post/<int:a_id>/',methods=['GET','POST'])
def post(a_id=-1):
    if a_id < 0:
        first_articles = Article.query.first()
        a_id = first_articles.a_id
    articles = Article.query.all()
    article_list = Article.query.filter(Article.a_id == a_id).first()
    if a_id == Article.query.first().a_id:
        article_pro = Article.query.first()
    else:
        article_pro = Article.query.filter(Article.a_id < article_list.a_id).order_by(-Article.a_id)[0]
    if a_id == Article.query.order_by(-Article.a_id).first().a_id:
        article_next = Article.query.order_by(-Article.a_id).first()
    else:
        article_next = Article.query.filter(Article.a_id > article_list.a_id).order_by(Article.a_id)[0]
    #或许当前登录着的名字
    tourists = session.get('username')
    # tourists_message = User.query.filter(.a)
    # print(tourists)
    # print(article_next)
    # print(article_pro)
    comments = Comment.query.all()
    article_comm = db.session.query(Article, Comment).filter(Article.a_id == Comment.a_id, Comment.a_id == a_id).all()
    # print(article_comm)
    comment_num = len(article_comm)
    categories = Category.query.all()
    three_articles = Article.query.order_by(-Article.a_create_time).all()[0:3]

    #评论区的表单验证
    if request.method == 'POST':
        username = request.values.get('username')
        content = request.values.get('usercomment')
        validation = User.query.filter(User.u_username==username).first()
        if validation:
            comment = Comment(c_name=username,c_content=content,a_id=a_id,c_data=datetime.utcnow())
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('ac.post',a_id = article_list.a_id))

    return render_template('post.html', **locals())




@ac.route('/verifycode/')
def verifycode():
    result = vc.generate()
    session['code'] = vc.code
    response = make_response(result)
    response.headers['Content-type'] = 'image/png'
    return response


# @ac.route('/phone_code/',methods= ['GET','POST'])
# def phone_code():
#     phone = request.values.get('phonenum')
#     # print('收到手机号')
#     if phone:
#         num = randint(1000,9999)
#         session['smscode'] = str(num)
#         para = "{'code':'%d'}"%num
#         result = sms.send(phone,para)
#         # print(phone,num)
#         return result
#     return render_template('registered.htm')




