from flask import Blueprint, request
from flask import jsonify, g
from flask import session
from flask import flash
from flask import redirect

from . import auth
from ...models import db
from ...models.user import User, UserConfig, UserMemo
from ...utils.tasks import send_register_active_email
from ...logger import logger
from ...config.default import DefaultConfig

user = Blueprint('user', __name__)


# 路由
@user.route("/memo", methods=['GET'])
@auth.login_required
def get_user_memo():
    memo = g.user.memo.memo
    return jsonify({'memo': memo})


@user.route("/info", methods=['POST', 'GET'])
@auth.login_required
def info():
    """
    获取当前登录用户的信息
    :return:
    """
    email = g.user.email
    words_book = g.user.config.words_book
    return jsonify({'email': email, 'words_book': words_book})


@user.route("/users", methods=['GET'])
@auth.login_required
def get_users():
    """
    获取用户名列表，供admin使用
    """
    if not g.user.config.role:
        res = []
        return jsonify(res)
    users_obj = User.query.all()
    res = [
        {
            'username': item.username,
            'email': item.email,
            'wordbook': UserConfig.query.filter_by(user_id=item.id).first().words_book
         } for item in users_obj
    ]
    return jsonify(res)


@user.route("/memoupdate", methods=['POST', 'GET'])
@auth.login_required
def save_memo():
    memo = request.get_json()['memo']
    memo_obj = UserMemo.query.filter_by(user_id=g.user.id).first()
    memo_obj.memo = memo
    db.session.add(memo_obj)
    db.session.commit()
    return jsonify({'code': 200})


@user.route('/logout', methods=['DELETE'])
def logout():
    if 'username' in session:
        session.pop('username')
        return jsonify({'code': 200, 'description': 'Logout successful.'})
    else:
        return jsonify({'code': 201, 'description': 'No user was found.'})


@user.route('/infoupdate', methods=['POST'])
@auth.login_required
def update():
    """
    用户信息更新
    """
    username = request.get_json()['username']
    email = request.get_json()['email']
    password = request.get_json()['password']
    words_book = request.get_json()['words_book']
    try:
        user_config = UserConfig.query.filter_by(user_id=g.user.id).first()
        user_config.words_book = words_book
        db.session.add(user_config)
        if password:
            g.user.password = password
        g.user.username = username
        db.session.add(g)
        db.session.commit()

        msg = "success"
        code = 200
    except Exception as e:
        msg = "fail"
        code = 400
    res = {
        'code': code,
        'msg': msg
    }
    return jsonify(res)


@user.route('/register', methods=['POST'])
def register():
    """
    用户注册
    """
    username = request.get_json()['username']
    email = request.get_json()['email']
    password = request.get_json()['password']
    try:
        user = User.query.filter_by(email=email).first()
        if user and not user.activate:
            # 用户已经注册，但是未点击激活链接，则重新生成激活链接并发送邮件
            # 先更新密码与用户
            user.password = password
            user.username = username
            db.session.add(user)
            db.session.commit()
            token = user.generate_auth_token(expiration=5*60).decode('ascii')  # 此时token过期时间为5分钟
            send_register_active_email(user.email, user.username, token)
            flash('邮件已经发送！')
            msg = "注册成功,激活链接已发送到你注册时的邮箱，请及时激活"
            res = {
                'code': 200,
                'msg': msg
            }
        elif user and user.activate:
            # 用户已经注册，且已经激活
            msg = "该邮箱已经注册过，换个邮箱试试吧！"
            res = {
                'code': 401,
                'msg': msg
            }
        else:
            # 用户尚未注册
            user = User(username=username, email=email, password=password)
            db.session.add(user)
            db.session.flush()
            config = UserConfig(role=False, user_id=user.id)
            db.session.add(config)
            memo = UserMemo(user_id=user.id)
            db.session.add(memo)
            db.session.commit()
            token = user.generate_auth_token(expiration=5 * 60).decode('ascii')  # 此时token过期时间为5分钟
            send_register_active_email(user.email, user.username, token)
            flash('邮件已经发送！')
            msg = "注册成功,激活链接已发送到你注册时的邮箱，请及时激活"
            res = {
                'code': 200,
                'msg': msg
            }
    except Exception as e:
        logger.error(e)
        msg = "未知错误，请稍后再试，或直接发邮件到luohai2233@163.com"
        res = {
            'code': 404,
            'msg': msg
        }
    return jsonify(res)


@user.route('/active/<token>', methods=['GET'])
def activate(token):
    """
    激活
    :return: None
    """
    if User.check_activate_token(token):
        flash('激活成功')
        return redirect('http://' + DefaultConfig.FrontDomain + '/login')
    else:
        flash('激活失败')
        return jsonify({'code': 401, 'msg': "令牌失效，请重新注册"})


@auth.verify_password
def verify_password(email_or_token, password):
    if request.path == "/user/login":
        user = User.query.filter_by(email=email_or_token).first()
        if not user or not user.check_password_hash(password) or not user.activate:
            return False
    else:
        user = User.verify_auth_token(email_or_token)
        if not user:
            return False
    g.user = user
    return True


@user.route('/login', methods=['GET'])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    username = g.user.username
    return jsonify({'token': token.decode('ascii'), 'username': username})
