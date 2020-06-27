import datetime

from . import db


class WordBase(db.Model):
    __abstract__ = True  # 把__abstract__这个属性设置为True,这个类为基类，不会被创建为表
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(32), index=True)
    translation = db.Column(db.String(512), nullable=False)
    spellingA = db.Column(db.String(64), nullable=True)  # 美音
    spellingE = db.Column(db.String(64), nullable=True)  # 英音


class Cet6(WordBase):
    __tablename__ = 'words_cet6'


class Cet4(WordBase):
    __tablename__ = 'words_cet4'


class GRE(WordBase):
    __tablename__ = 'words_gre'


class TOEFL(WordBase):
    __tablename__ = 'words_toefl'


class DailyWords(WordBase):
    __tablename__ = 'words_daily_words'
    user_id = db.Column(db.Integer(), nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.date.today())
