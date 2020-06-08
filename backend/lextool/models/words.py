from . import db


class EnWords(db.Model):
    __bind_key__ = 'words'  # 已设置__bind_key__,则采用设置的数据库引擎
    __tablename__ = 'enwords'
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(32))
    translation = db.Column(db.String(512))
