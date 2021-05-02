from backend.lextool.models.base_model import db
from backend.lextool.models.base_model import ModelWithCreateAt


class DWZ(ModelWithCreateAt):
    __tablename__ = 'dwz'
    url = db.Column(db.Text(65536))
    dwz = db.Column(db.String(10), unique=True, index=True)
