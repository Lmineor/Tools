#encoding:utf-8

import hashlib
import re

from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy

from local_config import PASSWORD
from shorturl import shorturl

app = Flask(__name__)
app.config['SECRET_KEY'] = PASSWORD
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:shorturl@localhost:3306/shorturl' 
#这里登陆的是root用户，要填上自己的密码，MySQL的默认端口是3306，填上之前创建的数据库名test
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True 
#设置这一项是每次请求结束后都会自动提交数据库中的变动

@app.route('/shorten', methods=['POST'])
def main():
    origin = 10
    su = shorturl(origin)





print(shorten('http://www.google.com'))


if __name__ == '__main__':
    # app.run()
    test()
