from .base_model import Base, PoetIntroductionMixin, db


class PoetIntroduction(Base, PoetIntroductionMixin):
    __tablename__ = 'poem_poet_introduction'  # 诗人简介
    descb = db.Column(db.Text(16777216))
    poet = db.Column(db.String(100), index=True)
    dynasty = db.Column(db.String(8), index=True)


class PoemTangSong(Base):
    __tablename__ = 'poem_tang_song_poem'
    
    paragraphs = db.Column(db.Text)
    poem = db.Column(db.Text(65536))
    poet = db.Column(db.String(100), index=True)
    dynasty = db.Column(db.String(8), index=True)


class PoemLunyu(Base):
    __tablename__ = 'poem_lun_yu'

    paragraphs = db.Column(db.Text(65536))
    chapter = db.Column(db.String(50), index=True)


class PoemSongci(Base):
    __tablename__ = 'poem_song_ci'

    paragraphs = db.Column(db.Text(16777216))
    rhythmic = db.Column(db.String(40), index=True)
    poet = db.Column(db.String(100), index=True)

    def __str__(self):
        return "<PoemSongci(rhythmic='%s', poet='%s')>" % (
            self.rhythmic, self.poet)


class CiAuthor(Base):
    __tablename__ = 'poem_ci_poet'

    long_desc = db.Column(db.Text(16777216))
    short_desc = db.Column(db.Text(65536))
    poet = db.Column(db.String(100), index=True)


class ShiJing(Base):
    __tablename__ = 'poem_shi_jing'

    poem = db.Column(db.Text(16777216))
    chapter = db.Column(db.String(30), index=True)
    section = db.Column(db.String(30), index=True)
    content = db.Column(db.Text(65536))
