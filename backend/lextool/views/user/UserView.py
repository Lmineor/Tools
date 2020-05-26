from flask import Blueprint, request
from flask import jsonify, g
from flask import session

from . import auth
from ...models import db
from ...models.user import User

user = Blueprint('user', __name__)


# 路由
@user.route("/usermemo", methods=['POST', 'GET'])
@auth.login_required
def usermemo():
    memo = g.user.memo
    return jsonify({'memo': memo})


@user.route("/saveusermemo", methods=['POST', 'GET'])
@auth.login_required
def saveusermemo():
    id = g.user.id
    memo = request.get_json()['memo']
    currentuser = User.query.get(id)
    currentuser.memo = memo
    db.session.add(currentuser)
    db.session.commit()
    return jsonify({'memo': memo})


@user.route('/logout', methods=['DELETE'])
def logout():
    if 'username' in session:
        session.pop('username')
        return jsonify({'code': 200,'description': 'Logout successful.'})
    else:
        return jsonify({'code': 201, 'description': 'No user was found.'})


@user.route('/register', methods=['POST'])
def user_register():
    """
    test
    """
    username = request.get_json()['username']
    email = request.get_json()['email']
    password = request.get_json()['password']
    try:
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        msg = "注册成功"
    except Exception as e:
        code = str(e.__cause__).split(',')[0][1:]
        if code == '1062':
            msg = "该邮箱已经注册过，换个邮箱试试吧！"
        else:
            msg = "未知错误，请稍后再试，或直接发邮件到luohai2233@163.com"
    res = {
        'code': 200,
        'msg': msg
    }
    return jsonify(res)


@auth.verify_password
def verify_password(email_or_token, password):
    if request.path == "/login":
        user = User.query.filter_by(email=email_or_token).first()
        if not user or not user.check_password_hash(password):
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
