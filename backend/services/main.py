#encoding:utf-8

import hashlib
import re

from flask import Flask
from flask import request, redirect, Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_caching import Cache

from local_config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_BINDS
from logger import logger
from gen_dwz import gen_dwz


logger = logger(log_filename="app.log")
app = Flask(__name__)
CORS(app, supports_credentials=True)
# ----------------------------------------------------------------
# 缓存配置（文件系统缓存）
FILESYSTEM = {
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': './flask_cache',
    'CACHE_DEFAULT_TIMEOUT': 922337203685477580,
    'CACHE_THRESHOLD': 922337203685477580
}
cache = Cache(app,config=FILESYSTEM)



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


# ----------------------------------------------------------------
# 路由
@app.route('/login', methods=['POST'])
def user_login():
    """
    test
    """
    email = request.get_json()['email']
    password = request.get_json()['password']
    logger.info('email' + email)
    logger.info('password' + password)
    res = {
        'token': 'adfafdfadfafd',
        'code': 200
    }
    return res


@app.route('/register', methods=['POST'])
def user_register():
    """
    test
    """
    email = request.get_json()['email']
    password = request.get_json()['password']
    logger.info('email' + email)
    logger.info('password' + password)
    res = {
        'code': 200
    }
    return res


@app.route('/poem/getauthor', methods=['POST'])
def get_author():
    """
    test
    """
    dynasty = request.get_json()['dynasty']
    logger.info('dynasty' + dynasty)
    if cache.get(dynasty):
        authors =  cache.get(dynasty)
    else:
        try:
            items = PoemTangSong.query.filter_by(dynasty = dynasty).all()
            authors = list(set([item.author for item in items]))
        except Exception as e:
            authors = []
            logger.error(e)
        cache.set(dynasty, authors)
    data = {
        'code': 200,
        'authors': authors
    }
    return data


@app.route('/poem/gettitle', methods=['POST'])
def get_title():
    """
    test
    """
    author = request.get_json()['author']
    dynasty = request.get_json()['dynasty']
    logger.info('author' + author)
    if cache.get(author + dynasty):
        titles = cache.get(author + dynasty)
    else:
        try:
            items = PoemTangSong.query.filter_by(author = author, dynasty=dynasty).all()
            titles = list(set([item.title for item in items]))
        except Exception as e:
            titles = []
            logger.error(e)
        cache.set(author + dynasty, titles)
    return {
        'code': 200,
        'titles': titles
    }


@app.route('/poem/getpoem', methods=['POST'])
def get_poem():
    """
    test
    """
    author = request.get_json()['author']
    dynasty = request.get_json()['dynasty']
    title = request.get_json()['title']
    logger.info('author' + author)
    if cache.get(author + dynasty + title):
        poem = cache.get(author + dynasty + title)
    else:
        try:
            poem = PoemTangSong.query.filter_by(author = author, dynasty=dynasty, title=title).first().paragraphs
        except Exception as e:
            poem = ''
            logger.error(e)
        cache.set(author + dynasty + title, poem)
    return {
        'code': 200,
        'poem': poem
    }


@app.route('/shorturl/shorten', methods=['POST'])
def main():
    url = request.get_json()['url']
    logger.info('输入的url为：' + url)
    if not url:
        return None
    su = __pre_get(url)
    if su:
        return {
            'code': 200,
            'url': su
            }
    try:
        shortU = ShortUrl(origin_url = url)
        db.session.add(shortU)
        db.session.flush()
        urlid = shortU.id # 得到最后一调数据插入的id
        su = gen_dwz(urlid) # 生成短链
        logger.info("短链成功生成")
        shortU.short_url = su
        db.session.add(shortU)
        db.session.flush()
        db.session.commit()
    except Exception as e:
        logger.error(url + ' 重复')
        logger.error(e)
    if not su:
        item = ShortUrl.query.filter(ShortUrl.origin_url == url).first()
        if item:
            su = item.short_url
    data = {
        'code': 200,
        'url': su
    }
    return Response(data)


@app.route('/s/<code>', methods=['GET'])
def redir(code):
    """
    重定向部分
    """
    try:
        item = ShortUrl.query.filter(ShortUrl.short_url == str(code)).first()
        origin_url = item.origin_url
    except Exception as e:
        origin_url = ''
        logger.error(e)
    if not origin_url:
        return render_template('404.html')
    elif not origin_url.startswith('http'):
        return redirect('http://' + origin_url)
    else:
        return redirect(origin_url)


@app.route('/shorturl/OriginUrl', methods=['POST'])
def get_originurl():
    """
    短链还原部分
    """
    shorturl = request.get_json()['shorturl']
    logger.info('输入的shorturl为：' + shorturl)
    if not shorturl:
        return None;
    try:
        item = ShortUrl.query.filter(ShortUrl.short_url == shorturl).first()
        origin_url = item.origin_url
    except Exception as e:
        origin_url = ''
        logger.error(e)
    return {
        'code': 200,
        'OriginUrl': origin_url
    }


def __pre_get(url):
    su = ''
    try:
        item = ShortUrl.query.filter(ShortUrl.origin_url == url).first()
        if item:
            su = item.short_url
    except Exception as e:
        logger.error(e)
    return su


if __name__ == '__main__':
    try:
        db.create_all()
    except Exception as e:
        pass
    app.run()
