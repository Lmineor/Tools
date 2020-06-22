import datetime

from werkzeug.security import generate_password_hash, check_password_hash  # 转换密码用到的库
from flask_security import UserMixin  # 登录和角色需要继承的对象
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from ..config.default import DefaultConfig
from ..models import db


class UserConfig(db.Model):
    __tablename__ = 'config'
    index = db.Column(db.Integer(), primary_key=True)
    words_book = db.Column(db.String(10), default='CET4')  # 1: CET4, 2 CET6, 3: TOEFL 4: GRE
    role = db.Column(db.Boolean, nullable=False)  # True:admin, False: common user
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    create_at = db.Column(db.DateTime, default=datetime.datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class UserMemo(db.Model):
    __tablename__ = 'memo'
    index = db.Column(db.Integer(), primary_key=True)
    memo = db.Column(db.Text(16777216), default="写下你的便签")
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    create_at = db.Column(db.DateTime, default=datetime.datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128))
    activate = db.Column(db.Boolean, default=False)
    create_at = db.Column(db.DateTime, default=datetime.datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    memo = db.relationship("UserMemo", uselist=False, backref="user", cascade="delete")
    config = db.relationship("UserConfig", uselist=False, backref="user", cascade="delete")

    def __repr__(self):
        return "<User_id:{0}>".format(self.id)

    @property
    def password(self):
        raise AttributeError("密码不允许读取")

    # 转换密码为hash存入数据库
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 检查密码
    def check_password_hash(self, password):
        return check_password_hash(self.password_hash, password)

    # 获取token
    def generate_auth_token(self, expiration=DefaultConfig.EXPIRATION):
        s = Serializer(DefaultConfig.SECRET_KEY, expires_in=expiration)
        return s.dumps({'id': self.id})

    # 解析token，确认登录的用户身份
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(DefaultConfig.SECRET_KEY)
        try:
            data = s.loads(token)
        except BadSignature as e:
            return None  # invalid token
        except SignatureExpired as e:
            return None  # token expire
        user = User.query.get(data['id'])
        return user

    @staticmethod
    def check_activate_token(token):
        s = Serializer(DefaultConfig.SECRET_KEY)
        try:
            data = s.loads(token)
        except:
            return False
        u = User.query.get(data['id'])
        if not u:
            # 用户已被删除
            return False
        if not u.activate:
            u.activate = True
            db.session.add(u)
            db.session.commit()
        return True
