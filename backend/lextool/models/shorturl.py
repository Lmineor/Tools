from . import db


class ShortUrl(db.Model):
    __tablename__ = 'ShortUrl'  # 未设置__bind_key__,则采用默认的数据库引擎
    id = db.Column(db.Integer, primary_key=True)
    origin_url = db.Column(db.String(80), unique=True)
    short_url = db.Column(db.String(30), unique=True)
