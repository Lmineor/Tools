from .base_model import Base, PoetMixin, db, Like
    

class Poet(Base, PoetMixin):
    """诗人"""
    __tablename__ = 'poets'
    fields = ('poet', 'dynasty', 'descb')
    
    poet = db.Column(db.String(32), index=True)
    dynasty = db.Column(db.String(8), index=True)
    descb = db.Column(db.Text)
    poems = db.relationship('Poem', backref=db.backref('poems'), lazy='dynamic')


class Poem(Base):
    """诗"""
    __tablename__ = 'poems'
    fields = ('paragraphs', 'poem')
    
    paragraphs = db.Column(db.Text)
    poem = db.Column(db.Text)
    poet_id = db.Column(db.Integer, db.ForeignKey('poets.id'))
    u_id = db.Column(db.String(8), db.ForeignKey('like_poem.uid'))
    
    
class Lunyu(Base):
    __tablename__ = 'lun_yu'
    fields = ('paragraphs', 'chapter')
    paragraphs = db.Column(db.Text(65536))
    chapter = db.Column(db.String(64), index=True)
    u_id = db.Column(db.String(8), db.ForeignKey('like_lunyu.uid'))


class Songci(Base):
    __tablename__ = 'song_ci'
    fields = ('paragraphs', 'rhythmic')

    paragraphs = db.Column(db.Text)
    rhythmic = db.Column(db.String(64), index=True)
    poet_id = db.Column(db.Integer, db.ForeignKey('ci_poet.id', ondelete='CASCADE'))
    u_id = db.Column(db.String(8), db.ForeignKey('like_songci.uid'))

    def __str__(self):
        return "<PoemSongci(rhythmic='%s', poet='%s')>" % (
            self.rhythmic, self.poet_sim)


class CiPoet(Base):
    __tablename__ = 'ci_poet'
    fields = ('long_desc', 'short_desc', 'poet')

    long_desc = db.Column(db.Text)
    short_desc = db.Column(db.Text)
    poet = db.Column(db.String(32), index=True)
    ci = db.relationship('Songci', backref=db.backref('poet'), lazy='dynamic')
    

class ShiJing(Base):
    __tablename__ = 'shi_jing'
    fields = ('poem', 'chapter', 'section', 'content')
    
    poem = db.Column(db.Text)
    chapter = db.Column(db.String(64), index=True)
    section = db.Column(db.String(64), index=True)
    content = db.Column(db.Text)
    u_id = db.Column(db.String(8), db.ForeignKey('like_shijing.uid'))


class LikePoem(Like):
    __tablename__ = 'like_poem'

    content = db.relationship('Poem', backref=db.backref('like_poem'), lazy='dynamic')


class LikeShijing(Like):
    __tablename__ = 'like_shijing'

    content = db.relationship('ShiJing', backref=db.backref('like_shijing'), lazy='dynamic')


class LikeLunyu(Like):
    __tablename__ = 'like_lunyu'

    content = db.relationship('Lunyu', backref=db.backref('like_lunyu'), lazy='dynamic')


class LikeSongci(Like):
    __tablename__ = 'like_songci'

    content = db.relationship('Songci', backref=db.backref('like_songci'), lazy='dynamic')
