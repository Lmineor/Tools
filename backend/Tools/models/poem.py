from . import  db


class PoemSongAuthor(db.Model):
    __bind_key__ = 'poem'  # 已设置__bind_key__,则采用设置的数据库引擎
    __tablename__ = 'songshiauthor'

    id = db.Column(db.Integer, primary_key=True)
    descb = db.Column(db.Text)
    name = db.Column(db.String(30))


class PoemTangAuthor(db.Model):
    __bind_key__ = 'poem'  # 已设置__bind_key__,则采用设置的数据库引擎
    __tablename__ = 'tangshiauthor'

    id = db.Column(db.Integer, primary_key=True)
    descb = db.Column(db.Text)
    name = db.Column(db.String(30))


class PoemTangSong(db.Model):
    __bind_key__ = 'poem'  # 已设置__bind_key__,则采用设置的数据库引擎
    __tablename__ = 'tangsongshi'

    id = db.Column(db.Integer, primary_key=True)
    paragraphs = db.Column(db.Text)
    title = db.Column(db.String(30))
    author = db.Column(db.String(30))
    dynasty = db.Column(db.String(10))


class PoemLunyu(db.Model):
    __bind_key__ = 'poem'  # 已设置__bind_key__,则采用设置的数据库引擎
    __tablename__ = 'lunyu'

    id = db.Column(db.Integer, primary_key=True)
    paragraphs = db.Column(db.Text)
    chapter = db.Column(db.String(50))


class PoemSongci(db.Model):
    __bind_key__ = 'poem'  # 已设置__bind_key__,则采用设置的数据库引擎
    __tablename__ = 'songci'

    id = db.Column(db.Integer, primary_key=True)
    paragraphs = db.Column(db.Text)
    rhythmic = db.Column(db.String(40))
    author = db.Column(db.String(20))


class CiAuthor(db.Model):
    __bind_key__ = 'poem'  # 已设置__bind_key__,则采用设置的数据库引擎
    __tablename__ = 'ciauthor'

    id = db.Column(db.Integer, primary_key=True)
    long_desc = db.Column(db.Text)
    short_desc = db.Column(db.Text)
    name = db.Column(db.String(20))


class ShiJing(db.Model):
    __bind_key__ = 'poem'  # 已设置__bind_key__,则采用设置的数据库引擎
    __tablename__ = 'shijing'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    chapter = db.Column(db.String(30))
    section = db.Column(db.String(30))
    content = db.Column(db.String(20))
