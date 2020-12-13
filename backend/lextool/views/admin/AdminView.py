from functools import wraps

from flask import Blueprint, request
from flask import jsonify, g

from ..user import auth
from ...models import db
from ...models.user import User, UserConfig
from ...models.comment import Comment
from ...common.logger import LOG

admin = Blueprint('admin', __name__)


# ---------------------------------------------------------------------------------
# admin模块相关接口
# ---------------------------------------------------------------------------------

def admin_auth_decorator(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not g.user.config.role:
            return jsonify({'msg': 'Permission denied'})
        return f(*args, **kwargs)

    return decorated


@admin.route('/updates', methods=['POST'])
@auth.login_required
@admin_auth_decorator
def updates():
    """
    用户信息更新
    """
    action = request.get_json()['action']  # 1、 chgpsw 修改密码  2、 删除用户 deluser 3、一般更新操作 update
    if action == 'chgpsw':
        psw = request.get_json()['password']
        email = request.get_json()['email']
        try:
            LOG.info("Set email:{} psw as default{}".format(email, psw))
            usr = User.query.filter_by(email=email).first()
            usr.password = psw
            db.session.add(usr)
            db.session.commit()
            code = 200
            msg = 'success'
        except Exception as e:
            LOG.error("Set email:{} psw fail".format(email, psw))
            LOG.error("Error is {}".format(e))
            code = 400
            msg = 'fail'
        return jsonify({'action': action, 'code': code, 'msg': msg})
    elif action == 'deluser':
        email = request.get_json()['email']
        try:
            LOG.info("Del user email:{} ".format(email))
            usr = User.query.filter_by(email=email).first()
            db.session.delete(usr)
            db.session.commit()
            code = 200
            msg = 'success'
        except Exception as e:
            LOG.error("Del user email:{} fail".format(email))
            LOG.error("Error is {}".format(e))
            code = 400
            msg = 'fail'
        return jsonify({'action': action, 'code': code, 'msg': msg})
    else:
        email = request.get_json()['email']
        wordsbook = request.get_json()['wordsbook']
        try:
            LOG.info(" update email:{} set wordsbook {}".format(email, wordsbook))
            usr = User.query.filter_by(email=email).first()
            usr.config.words_book = wordsbook
            db.session.add(usr)
            db.session.commit()
            code = 200
            msg = 'success'
        except Exception as e:
            LOG.error("update user email:{} wordsbook fail".format(email))
            LOG.error("Error is {}".format(e))
            code = 400
            msg = 'fail'
        return jsonify({'action': action, 'code': code, 'msg': msg})


@admin.route("/users", methods=['GET'])
@auth.login_required
@admin_auth_decorator
def get_users():
    """
    获取用户名列表，供admin使用
    """
    if not g.user.config.role:
        users = []
        return jsonify(users)
    users_obj = User.query.all()
    users = [
        {
            'username': item.username,
            'email': item.email,
            'wordsbook': UserConfig.query.filter_by(user_id=item.id).first().words_book
         } for item in users_obj
    ]
    return jsonify(users)


@admin.route("/load_comment", methods=['GET'])
@auth.login_required
@admin_auth_decorator
def load_un_reviewed_comment():
    LOG.info("load comment")
    data = Comment.get_un_solved_queries()
    return jsonify({'data': data})


@admin.route("/review_comment", methods=['POST'])
@auth.login_required
@admin_auth_decorator
def review_comment():
    index = request.get_json()['id']
    key = request.get_json()['key']
    msg, code = Comment.review(index, key)
    return jsonify({'msg': msg, 'code': code})
