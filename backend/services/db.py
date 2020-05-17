#encoding:utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache

from local_config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_BINDS

app = Flask(__name__)
# ----------------------------------------------------------------
# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI']= SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_BINDS']= SQLALCHEMY_BINDS
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True 
#设置这一项是每次请求结束后都会自动提交数据库中的变动
#实例化
db = SQLAlchemy(app)
class ShortUrl(db.Model):
    __tablename__ = 'ShortUrl' # 未设置__bind_key__,则采用默认的数据库引擎
    id = db.Column(db.Integer, primary_key=True)
    origin_url = db.Column(db.String(80), unique=True)
    short_url = db.Column(db.String(30), unique=True)


class PoemSongAuthor(db.Model):
    __bind_key__ = 'poem' # 已设置__bind_key__,则采用设置的数据库引擎
    __tablename__ = 'songshiauthor'

    id = db.Column(db.Integer, primary_key=True)
    descb = db.Column(db.Text)
    name = db.Column(db.String(30))


class PoemTangAuthor(db.Model):
    __bind_key__ = 'poem' # 已设置__bind_key__,则采用设置的数据库引擎
    __tablename__ = 'tangshiauthor'

    id = db.Column(db.Integer, primary_key=True)
    descb = db.Column(db.Text)
    name = db.Column(db.String(30))


class PoemTangSong(db.Model):
    __bind_key__ = 'poem' # 已设置__bind_key__,则采用设置的数据库引擎
    __tablename__ = 'tangsongshi'

    id = db.Column(db.Integer, primary_key=True)
    paragraphs = db.Column(db.Text)
    title = db.Column(db.String(30))
    author = db.Column(db.String(30))
    dynasty = db.Column(db.String(10))


class PoemLunyu(db.Model):
    __bind_key__ = 'poem' # 已设置__bind_key__,则采用设置的数据库引擎
    __tablename__ = 'lunyu'

    id = db.Column(db.Integer, primary_key=True)
    paragraphs = db.Column(db.Text)
    chapter = db.Column(db.String(50))


class PoemSongci(db.Model):
    __bind_key__ = 'poem' # 已设置__bind_key__,则采用设置的数据库引擎
    __tablename__ = 'songci'

    id = db.Column(db.Integer, primary_key=True)
    paragraphs = db.Column(db.Text)
    rhythmic = db.Column(db.String(40))
    author = db.Column(db.String(20))


class CiAuthor(db.Model):
    __bind_key__ = 'poem' # 已设置__bind_key__,则采用设置的数据库引擎
    __tablename__ = 'ciauthor'

    id = db.Column(db.Integer, primary_key=True)
    long_desc = db.Column(db.Text)
    short_desc = db.Column(db.Text)
    name = db.Column(db.String(20))
