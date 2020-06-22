import datetime

from . import db


class DWZ(db.Model):
    """
    短网址数据库
    """
    __bind_key__ = 'dwz'  # 已设置__bind_key__,则采用设置的数据库引擎
    __tablename__ = 'dwz'  # 未设置__bind_key__,则采用默认的数据库引擎
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(80), unique=True)
    dwz = db.Column(db.String(10), unique=True)
    create_at = db.Column(db.DateTime, default=datetime.datetime.now)
