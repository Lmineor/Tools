from .base_model import Base, PoetMixin, db
    

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
    
    
class Lunyu(Base):
    __tablename__ = 'lun_yu'
    fields = ('paragraphs', 'chapter')
    paragraphs = db.Column(db.Text(65536))
    chapter = db.Column(db.String(64), index=True)


class Songci(Base):
    __tablename__ = 'song_ci'
    fields = ('paragraphs', 'rhythmic')

    paragraphs = db.Column(db.Text)
    rhythmic = db.Column(db.String(64), index=True)
    poet_id = db.Column(db.Integer, db.ForeignKey('ci_poet.id', ondelete='CASCADE'))
    
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
