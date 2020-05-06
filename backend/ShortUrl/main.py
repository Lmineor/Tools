#encoding:utf-8

import hashlib
import re

from flask import Flask
from flask import request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask import render_template

from local_config import PASSWORD, SQLALCHEMY_DATABASE_URI
from shorturl import shorturl
from logger import logger

from flask_cors import CORS
app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config['SECRET_KEY'] = PASSWORD
app.config['SQLALCHEMY_DATABASE_URI']= SQLALCHEMY_DATABASE_URI
#这里登陆的是root用户，要填上自己的密码，MySQL的默认端口是3306，填上之前创建的数据库名test
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True 
#设置这一项是每次请求结束后都会自动提交数据库中的变动

#实例化
db = SQLAlchemy(app)
class ShortUrl(db.Model):
    __tablename__ = 'ShortUrl'
    id = db.Column(db.Integer, primary_key=True)
    origin_url = db.Column(db.String(80), unique=True)
    short_url = db.Column(db.String(30), unique=True)
    def __repr__(self):
        return '<Role {}> '.format(self.__tablename__)


@app.route('/shorten', methods=['POST'])
def main():
    url = request.get_json()['url']
    logger.info('输入的url为：' + url)
    if not url:
        return None;
    su = pre_get(url)
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
        su = shorturl(urlid) # 生成短链
        logger.info("短链成功生成")
        shortU.short_url = su
        db.session.add(shortU)
        db.session.flush()
        db.session.commit()
    except Exception as e:
        logger.error(url + ' 重复')
    if not su:
        item = ShortUrl.query.filter(ShortUrl.origin_url == url).first()
        if item:
            su = item.short_url
    return {
        'code': 200,
        'url': su
    }

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


@app.route('/OriginUrl', methods=['POST'])
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


def pre_get(url):
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

