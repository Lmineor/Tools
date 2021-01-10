from .base_model import Base, PoetIntroductionMixin, db
    

class Poet(Base, PoetIntroductionMixin):
    """诗人"""
    __tablename__ = 'poets'
    
    poet = db.Column(db.String(32), index=True)
    poet_sim = db.Column(db.String(32), index=True)
    
    dynasty = db.Column(db.String(8), index=True)
    dynasty_sim = db.Column(db.String(8), index=True)

    descb = db.Column(db.Text)
    descb_sim = db.Column(db.Text)

    poems = db.relationship('Poem', backref=db.backref('poems'), lazy='dynamic')


class Poem(Base):
    """诗"""
    __tablename__ = 'poems'
    
    paragraphs = db.Column(db.Text)
    paragraphs_sim = db.Column(db.Text)
    
    poem = db.Column(db.Text)
    poem_sim = db.Column(db.Text)

    poet_id = db.Column(db.Integer, db.ForeignKey('poets.id'))
    
    
class Lunyu(Base):
    __tablename__ = 'lun_yu'

    paragraphs = db.Column(db.Text(65536))
    paragraphs_sim = db.Column(db.Text(65536))

    chapter = db.Column(db.String(64), index=True)
    chapter_sim = db.Column(db.String(64), index=True)


class Songci(Base):
    __tablename__ = 'song_ci'

    paragraphs = db.Column(db.Text)
    paragraphs_sim = db.Column(db.Text)
    
    rhythmic = db.Column(db.String(64), index=True)
    rhythmic_sim = db.Column(db.String(64), index=True)
    
    poet_id = db.Column(db.Integer, db.ForeignKey('ci_poet.id', ondelete='CASCADE'))
    
    def __str__(self):
        return "<PoemSongci(rhythmic='%s', poet='%s')>" % (
            self.rhythmic, self.poet_sim)


class CiPoet(Base):
    __tablename__ = 'ci_poet'

    long_desc = db.Column(db.Text)
    long_desc_sim = db.Column(db.Text)
    
    short_desc = db.Column(db.Text)
    short_desc_sim = db.Column(db.Text)
    
    poet = db.Column(db.String(32), index=True)
    poet_sim = db.Column(db.String(32), index=True)

    ci = db.relationship('Songci', backref=db.backref('poet'))
    

class ShiJing(Base):
    __tablename__ = 'shi_jing'

    poem = db.Column(db.Text)
    poem_sim = db.Column(db.Text)
    
    chapter = db.Column(db.String(64), index=True)
    chapter_sim = db.Column(db.String(64), index=True)
    
    section = db.Column(db.String(64), index=True)
    section_sim = db.Column(db.String(64), index=True)
    
    content = db.Column(db.Text)    
    content_sim = db.Column(db.Text)
