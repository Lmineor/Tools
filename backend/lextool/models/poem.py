from . import db
from ..config.default import DefaultConfig


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)


class PoetIntroduction(Base):
    __tablename__ = 'poem_poet_introduction'  # 诗人简介

    descb = db.Column(db.Text(16777216))
    poet = db.Column(db.String(100), index=True)
    dynasty = db.Column(db.String(8))

    @classmethod
    def search_poet(cls, keyword, page):
        items = cls.query.filter(
                cls.poet.like("%%{}%%".format(keyword)) if keyword is not None else "")\
            .paginate(page=page, per_page=DefaultConfig.PER_PAGE, error_out=False).items
        return [item.poet for item in items]

    @classmethod
    def search_keyword_total(cls, keyword):
        total = len(cls.query.filter(
            cls.poet.like("%%{}%%".format(keyword)) if keyword is not None else "").all())
        return total


class PoemTangSong(Base):
    __tablename__ = 'poem_tang_song_poem'

    paragraphs = db.Column(db.Text)
    poem = db.Column(db.Text(65536))
    poet = db.Column(db.String(100))
    dynasty = db.Column(db.String(8))


class PoemLunyu(Base):
    __tablename__ = 'poem_lun_yu'

    paragraphs = db.Column(db.Text(65536))
    chapter = db.Column(db.String(50))


class PoemSongci(Base):
    __tablename__ = 'poem_song_ci'

    paragraphs = db.Column(db.Text(16777216))
    rhythmic = db.Column(db.String(40))
    poet = db.Column(db.String(100))


class CiAuthor(Base):
    __tablename__ = 'poem_ci_poet'

    long_desc = db.Column(db.Text(16777216))
    short_desc = db.Column(db.Text(65536))
    poet = db.Column(db.String(100))


class ShiJing(Base):
    __tablename__ = 'poem_shi_jing'

    poem = db.Column(db.Text(16777216))
    chapter = db.Column(db.String(30))
    section = db.Column(db.String(30))
    content = db.Column(db.Text(65536))
