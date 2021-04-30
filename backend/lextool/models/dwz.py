from .base_model import db, ModelWithCreateAt


class DWZ(ModelWithCreateAt):
    __tablename__ = 'dwz'
    url = db.Column(db.Text(65536))
    dwz = db.Column(db.String(10), unique=True, index=True)
