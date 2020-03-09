# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from ext import db


class Article(db.Model):
    __tablename__ = 'article'

    a_id = db.Column(db.Integer, primary_key=True)
    a_title = db.Column(db.String(255, 'utf8_bin'), nullable=False, info='文章标题')
    a_content = db.Column(db.String(10000, 'utf8_bin'), nullable=False, info='文章内容')
    a_create_time = db.Column(db.DateTime, nullable=False, info='文章创建时间')
    c_id = db.Column(db.ForeignKey('category.c_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True, info='文章标签')
    a_hits = db.Column(db.Integer, info='文章点击量')
    a_comments = db.Column(db.Integer, info='文章评论量')
    a_picture = db.Column(db.String(300, 'utf8_bin'), server_default=db.FetchedValue())

    c = db.relationship('Category', primaryjoin='Article.c_id == Category.c_id', backref='articles')



class Category(db.Model):
    __tablename__ = 'category'

    c_id = db.Column(db.Integer, primary_key=True)
    c_name = db.Column(db.String(20, 'utf8_bin'), nullable=False, unique=True)
    c_number = db.Column(db.Integer)



class Comment(db.Model):
    __tablename__ = 'comment'

    c_id = db.Column(db.Integer, primary_key=True)
    c_content = db.Column(db.String(1000, 'utf8_general_ci'), nullable=False, info='评论的内容')
    c_name = db.Column(db.String(20, 'utf8_general_ci'), nullable=False, index=True, info='哪个用户评论')
    a_id = db.Column(db.Integer, info='评论的文章')
    c_data = db.Column(db.DateTime, info='评论的日期')
    c_portait = db.Column(db.String(255, 'utf8_general_ci'), server_default=db.FetchedValue())



class Title(db.Model):
    __tablename__ = 'title'

    t_id = db.Column(db.Integer, primary_key=True)
    t_name = db.Column(db.String(255, 'utf8_bin'), nullable=False)
    a_id = db.Column(db.ForeignKey('article.a_id'), nullable=False, index=True)

    a = db.relationship('Article', primaryjoin='Title.a_id == Article.a_id', backref='titles')



class User(db.Model):
    __tablename__ = 'user'

    u_id = db.Column(db.Integer, primary_key=True, info='Id')
    u_username = db.Column(db.String(128, 'utf8_general_ci'), nullable=False, info='用户名-昵称')
    u_phone_number = db.Column(db.String(11, 'utf8_general_ci'), nullable=False, info='电话')
    u_psd = db.Column(db.String(50, 'utf8_general_ci'), nullable=False, info='密码')
    u_email = db.Column(db.String(255, 'utf8_general_ci'), info='邮箱')
    u_isforbiden = db.Column(db.String(1), info='是否登陆')
    u_portait = db.Column(db.String(255, 'utf8_general_ci'), server_default=db.FetchedValue(), info='头像')
