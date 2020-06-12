from . import db


class EnWords(db.Model):
    __bind_key__ = 'words'  # 已设置__bind_key__,则采用设置的数据库引擎
    __tablename__ = 'enwords'
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(32), index=True)
    translation = db.Column(db.String(512), nullable=False)
    spellingA = db.Column(db.String(64), nullable=True)  # 美音
    spellingE = db.Column(db.String(64), nullable=True)  # 英音


class Cet6(db.Model):
    __bind_key__ = 'words'  # 已设置__bind_key__,则采用设置的数据库引擎
    __tablename__ = 'cet6'
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(32), index=True)
    translation = db.Column(db.String(512), nullable=False)
    spellingA = db.Column(db.String(64), nullable=True)  # 美音
    spellingE = db.Column(db.String(64), nullable=True)  # 英音


class Cet4(db.Model):
    __bind_key__ = 'words'  # 已设置__bind_key__,则采用设置的数据库引擎
    __tablename__ = 'cet4'
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(32), index=True)
    translation = db.Column(db.String(512), nullable=False)
    spellingA = db.Column(db.String(64), nullable=True)  # 美音
    spellingE = db.Column(db.String(64), nullable=True)  # 英音
