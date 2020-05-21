#encoding:utf-8
import datetime

from flask import Flask
from flask import session
from flask import request
from flask import redirect
from flask import Response
from flask_cors import CORS
from flask_caching import Cache
from flask import jsonify, g
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash # 转换密码用到的库
from flask_security import RoleMixin, UserMixin # 登录和角色需要继承的对象
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from flask_httpauth import HTTPBasicAuth

from local_config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_BINDS, SECRET_KEY
from logger import logger
from gen_dwz import gen_dwz
from sciSpider import Sci
from local_config import PER_PAGE

app = Flask(__name__)
auth = HTTPBasicAuth()
db = SQLAlchemy(app)
# ----------------------------------------------------------------
# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI']= SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_BINDS']= SQLALCHEMY_BINDS
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True 
#设置这一项是每次请求结束后都会自动提交数据库中的变动

# 登录模块配置
app.config['SECRET_KEY'] = SECRET_KEY
app.permanent_session_lifetime = datetime.timedelta(seconds=30*60)
# session.permanent = True


# 跨域配置
CORS(app, supports_credentials=True)
# ----------------------------------------------------------------
# 缓存配置（文件系统缓存）
FILESYSTEM = {
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': './flask_cache',
    # 'CACHE_DEFAULT_TIMEOUT': 2,
    'CACHE_DEFAULT_TIMEOUT': 922337203685477580,
    'CACHE_THRESHOLD': 922337203685477580
}
cache = Cache(app,config=FILESYSTEM)


#角色<-->用户，关联表
roles_users = db.Table(
    'role_user',
    db.Column('user_id',db.Integer(),db.ForeignKey('user.id')),
    db.Column('role_id',db.Integer(),db.ForeignKey('role.id'))
)


#角色表
class Role(db.Model,RoleMixin):
    __bind_key__ = 'user' # 已设置__bind_key__,则采用设置的数据库引擎
    __tablename__ = 'role'
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(80),unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return "<Role_id:{0}>".format(self.id)


class User(db.Model, UserMixin):
    __bind_key__ = 'user' # 已设置__bind_key__,则采用设置的数据库引擎
    __tablename__ = 'user'
    id = db.Column(db.Integer(),primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(100),unique=True, nullable=False, index = True)
    password_hash = db.Column(db.String(128))
    memo = db.Column(db.Text)
    #多对多关联
    roles = db.relationship('Role',secondary='role_user',backref=db.backref('users',lazy='dynamic'))


    def __repr__(self):
        return "<User_id:{0}>".format(self.id)

    @property
    def password(self):
        raise AttributeError("密码不允许读取")

    #转换密码为hash存入数据库
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    #检查密码
    def check_password_hash(self, password):
        return check_password_hash(self.password_hash,password)

    # 获取token，有效时间1天
    def generate_auth_token(self, expiration = 60*60*24):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })

    # 解析token，确认登录的用户身份
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature as e:
            return None # invalid token
        user = User.query.get(data['id'])
        return user

class ShortUrl(db.Model):
    __tablename__ = 'ShortUrl' # 未设置__bind_key__,则采用默认的数据库引擎
    id = db.Column(db.Integer, primary_key=True)
    origin_url = db.Column(db.String(80), unique=True)
    short_url = db.Column(db.String(30), unique=True)


class PoemSongAuthor(db.Model):
    __bind_key__ = 'poem' # 已设置__bind_key__,则采用设置的数据库引擎
    __tablename__ = 'songshiauthor'

    id = db.Column(db.Integer, primary_key=True)
    descb = db.Column(db.Text)
    name = db.Column(db.String(30))


class PoemTangAuthor(db.Model):
    __bind_key__ = 'poem' # 已设置__bind_key__,则采用设置的数据库引擎
    __tablename__ = 'tangshiauthor'

    id = db.Column(db.Integer, primary_key=True)
    descb = db.Column(db.Text)
    name = db.Column(db.String(30))


class PoemTangSong(db.Model):
    __bind_key__ = 'poem' # 已设置__bind_key__,则采用设置的数据库引擎
    __tablename__ = 'tangsongshi'

    id = db.Column(db.Integer, primary_key=True)
    paragraphs = db.Column(db.Text)
    title = db.Column(db.String(30))
    author = db.Column(db.String(30))
    dynasty = db.Column(db.String(10))


class PoemLunyu(db.Model):
    __bind_key__ = 'poem' # 已设置__bind_key__,则采用设置的数据库引擎
    __tablename__ = 'lunyu'

    id = db.Column(db.Integer, primary_key=True)
    paragraphs = db.Column(db.Text)
    chapter = db.Column(db.String(50))


class PoemSongci(db.Model):
    __bind_key__ = 'poem' # 已设置__bind_key__,则采用设置的数据库引擎
    __tablename__ = 'songci'

    id = db.Column(db.Integer, primary_key=True)
    paragraphs = db.Column(db.Text)
    rhythmic = db.Column(db.String(40))
    author = db.Column(db.String(20))


class CiAuthor(db.Model):
    __bind_key__ = 'poem' # 已设置__bind_key__,则采用设置的数据库引擎
    __tablename__ = 'ciauthor'

    id = db.Column(db.Integer, primary_key=True)
    long_desc = db.Column(db.Text)
    short_desc = db.Column(db.Text)
    name = db.Column(db.String(20))


class ShiJing(db.Model):
    __bind_key__ = 'poem' # 已设置__bind_key__,则采用设置的数据库引擎
    __tablename__ = 'shijing'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    chapter = db.Column(db.String(30))
    section = db.Column(db.String(30))
    content = db.Column(db.String(20))

# ----------------------------------------------------------------
# 路由
@app.route("/api/auth/usermemo", methods=['POST', 'GET'])
@auth.login_required
def usermemo():
    memo = g.user.memo
    return jsonify({'memo': memo})


@app.route("/api/auth/saveusermemo", methods=['POST', 'GET'])
@auth.login_required
def saveusermemo():
    id = g.user.id
    memo = request.get_json()['memo']
    currentuser = User.query.get(id)
    currentuser.memo = memo
    db.session.add(currentuser)
    db.session.commit()
    return jsonify({'memo': memo})

@app.route('/api/auth/logout', methods=['DELETE'])
def logout():
    if 'username' in session:
        session.pop('username')
        return jsonify({'code': 200,'description': 'Logout successful.'})
    else:
        return jsonify({'code': 201, 'description': 'No user was found.'})


@app.route('/auth/register', methods=['POST'])
def user_register():
    """
    test
    """
    username = request.get_json()['username']
    email = request.get_json()['email']
    password = request.get_json()['password']
    user = User(username=username,email=email,password=password)
    db.session.add(user)
    db.session.commit()
    res = {
        'code': 200
    }
    return jsonify(res)


@auth.verify_password
def verify_password(email_or_token, password):
    if request.path == "/auth/login":
        # email_or_token = request.get_json()['email']
        # password = request.get_json()['password']
        user = User.query.filter_by(email=email_or_token).first()
        if not user or not user.check_password_hash(password):
            return False
    else:
        user = User.verify_auth_token(email_or_token)
        if not user:
            return False
    g.user = user
    return True


@app.route('/auth/login', methods=['GET'])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    username = g.user.username
    return jsonify({'token': token.decode('ascii'), 'username': username})


















# from poemPage import poem
# app.register_blueprint(poem, url_prefix='/poem')  

@app.route('/poem/getauthor', methods=['POST'])
def get_author():
    """
    得到某个朝代的作者列表
    """
    dynasty = request.get_json()['dynasty']
    page = request.get_json()['page']
    if cache.get(str(page) + dynasty):
        total = cache.get('authors_num' + dynasty)
        authors =  cache.get(str(page) + dynasty)
    else:
        try:
            if dynasty =='唐':
                total = len(PoemTangAuthor.query.all())
                items = PoemTangAuthor.query.paginate(page=page, per_page=PER_PAGE, error_out=False).items
                authors = list(set([item.name for item in items]))
            else:
                total = len(PoemSongAuthor.query.all())
                items = PoemSongAuthor.query.paginate(page=page, per_page=PER_PAGE, error_out=False).items
                authors = list(set([item.name for item in items]))
        except Exception as e:
            authors = []
            total = 0
            logger.error(e)
        cache.set('authors_num' + dynasty, total)
        cache.set(str(page) + dynasty, authors)
    data = {
        'code': 200,
        'total': total,
        'authors': authors
    }
    return jsonify(data)


@app.route('/poem/gettitle', methods=['POST'])
def get_title():
    """
    test
    """
    author = request.get_json()['author']
    dynasty = request.get_json()['dynasty']
    logger.info('author' + author)
    if cache.get(author + dynasty):
        titles = cache.get(author + dynasty)
    else:
        try:
            items = PoemTangSong.query.filter_by(author = author, dynasty=dynasty).all()
            titles = list(set([item.title for item in items]))
        except Exception as e:
            titles = []
            logger.error(e)
        cache.set(author + dynasty, titles)
    return jsonify({
        'code': 200,
        'titles': titles
    })


@app.route('/poem/getpoem', methods=['POST'])
def get_poem():
    """
    test
    """
    author = request.get_json()['author']
    dynasty = request.get_json()['dynasty']
    title = request.get_json()['title']
    logger.info('author' + author)
    if cache.get(author + dynasty + title):
        poem = cache.get(author + dynasty + title)
    else:
        try:
            poem = PoemTangSong.query.filter_by(author = author, dynasty=dynasty, title=title).first().paragraphs
        except Exception as e:
            poem = ''
            logger.error(e)
        cache.set(author + dynasty + title, poem)
    return jsonify({
        'code': 200,
        'poem': poem
    })

@app.route('/poem/lunyu', methods=['POST', 'GET'])
def get_lunyu():
    """
    test
    """
    if request.method == 'GET':
        if cache.get('chapters'):
            chapters = cache.get('chapters')
        else:
            try:
                items = PoemLunyu.query.all()
                chapters = list(set([item.chapter for item in items]))
            except Exception as e:
                chapters = []
                logger.error(e)
            cache.set('chapters', chapters)
        return jsonify({
            'code': 200,
            'chapters': chapters
        })
    else:
        chapter = request.get_json()['chapter']
        logger.info('chapter: ' + chapter)
        if cache.get('chapter'):
            paragraphs = cache.get('chapter')
        else:
            try:
                paragraphs = PoemLunyu.query.filter_by(chapter = chapter).first().paragraphs
            except Exception as e:
                paragraphs = ''
                logger.error(e)
            cache.set(chapter, paragraphs)
        return jsonify({
            'code': 200,
            'paragraphs': paragraphs.split('|')
        })


@app.route('/poem/songci', methods=['POST', 'GET'])
def get_songci():
    """
    test
    """
    author = request.get_json()['author']
    rhythmic = request.get_json()['rhythmic']
    page = request.get_json()['page']
    if page: # 获取作者翻页数据
        if cache.get('authors_num' + 'songci'):
            total = int(cache.get('authors_num' + 'songci'))
        else:
            total = len(CiAuthor.query.all())
            cache.set('authors_num' + 'songci', total)
        if cache.get(str(page) + 'songci'):
            authors =  cache.get(str(page) + 'songci')
        else:
            try:
                items = CiAuthor.query.paginate(page=page, per_page=PER_PAGE, error_out=False).items
                authors = list(set([item.name for item in items]))
            except Exception as e:
                authors = []
                logger.error(e)
            cache.set(str(page) + 'songci', authors)
        return jsonify({
            'code': 200,
            'authors': authors,
            'total': total
        })
    elif not rhythmic: # 获取词牌名s
        if cache.get(author + '_ci'):
            rhythmics = cache.get(author + '_ci')
        else:
            try:
                items = PoemSongci.query.filter_by(author = author).all()
                rhythmics = list(set([item.rhythmic for item in items]))
            except Exception as e:
                rhythmics = []
                logger.error(e)
            cache.set(author + '_ci', rhythmics)
        return jsonify({
            'code': 200,
            'rhythmics': rhythmics
        })
    else:
        if cache.get(author + rhythmic + '_ci'):
            paragraphs = cache.get(author + rhythmic + '_ci')
        else:
            try:
                paragraphs = PoemSongci.query.filter_by(author=author, rhythmic=rhythmic).first().paragraphs.split('。')
            except Exception as e:
                paragraphs = ''
                logger.error(e)
            cache.set(author + rhythmic + '_ci', paragraphs)
        return jsonify({
            'code': 200,
            'paragraphs': paragraphs
        })


@app.route('/poem/shijing', methods=['POST'])
def get_shijing():
    """
    test
    """
    title = request.get_json()['title']
    page = request.get_json()['page']
    if page: # 获取诗名翻页数据
        if cache.get('title_num' + 'shijing'):
            total = int(cache.get('title_num' + 'shijing'))
        else:
            total = len(ShiJing.query.all())
            cache.set('title_num' + 'shijing', total)
        if cache.get(str(page) + 'shijing'):
            titles =  cache.get(str(page) + 'shijing')
        else:
            try:
                items = ShiJing.query.paginate(page=page, per_page=PER_PAGE, error_out=False).items
                titles = list(set([item.title for item in items]))
            except Exception as e:
                titles = []
                logger.error(e)
            cache.set(str(page) + 'shijing', titles)
        return jsonify({
            'code': 200,
            'titles': titles,
            'total': total
        })
    else: # 获取内容
        logger.info(title)
        if cache.get(title + 'shijing'):
            content = cache.get(title + 'shijing')
            chaper = cache.get(title + 'chaper')
            section = cache.get(title + 'section')
        else:
            try:
                query = ShiJing.query.filter_by(title = title).first()
                content = query.content.split('。')
                chapter = query.chapter
                section = query.section
            except Exception as e:
                content = []
                chaper = section = ''
                logger.error(e)
            cache.set(title + 'shijing', content)
            cache.set(title + 'chaper', chapter)
            cache.set(title + 'section', section)
        return jsonify({
            'code': 200,
            'content': content,
            'chapter': chapter,
            'section': section,
        })



@app.route('/shorturl/shorten', methods=['POST'])
def main():
    url = request.get_json()['url']
    logger.info('输入的url为：' + url)
    if not url:
        return None
    su = __pre_get(url)
    if su:
        return {
            'code': 200,
            'url': su
            }
    try:
        shortU = ShortUrl(origin_url = url)
        db.session.add(shortU)
        db.session.flush()
        urlid = shortU.id # 得到最后一调数据插入的id
        su = gen_dwz(urlid) # 生成短链
        logger.info("短链成功生成")
        shortU.short_url = su
        db.session.add(shortU)
        db.session.flush()
        db.session.commit()
    except Exception as e:
        logger.error(e)
    if not su:
        item = ShortUrl.query.filter(ShortUrl.origin_url == url).first()
        if item:
            su = item.short_url
    data = {
        'code': 200,
        'url': su
    }
    return jsonify(data)


@app.route('/s/<code>', methods=['GET'])
def redir(code):
    """
    重定向部分
    """
    try:
        item = ShortUrl.query.filter(ShortUrl.short_url == str(code)).first()
        origin_url = item.origin_url
    except Exception as e:
        origin_url = ''
        logger.error(e)
    if not origin_url:
        return render_template('404.html')
    elif not origin_url.startswith('http'):
        return redirect('http://' + origin_url)
    else:
        return redirect(origin_url)


@app.route('/shorturl/OriginUrl', methods=['POST'])
def get_originurl():
    """
    短链还原部分
    """
    shorturl = request.get_json()['shorturl']
    if not shorturl:
        return None;
    try:
        item = ShortUrl.query.filter(ShortUrl.short_url == shorturl).first()
        origin_url = item.origin_url
    except Exception as e:
        origin_url = '生成失败,该短链不存在'
        logger.error(e)
    return jsonify({
        'code': 200,
        'OriginUrl': origin_url
    })


@app.route('/sci', methods=['GET'])
def get_sci():
    sci_url = Sci()
    urls = sci_url.raw_url()
    data = {
        'code': 200,
        'urls': urls
    }
    return jsonify(data)


def __pre_get(url):
    su = ''
    try:
        item = ShortUrl.query.filter(ShortUrl.origin_url == url).first()
        if item:
            su = item.short_url
    except Exception as e:
        logger.error(e)
    return su


def verify_user(email, password):
    #创建的时候还是使用password字段存入
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password_hash(password):
        return False, ''
    else:
        return True, user.username


if __name__ == '__main__':
    try:
        db.create_all()
    except Exception as e:
        pass
    app.run()
