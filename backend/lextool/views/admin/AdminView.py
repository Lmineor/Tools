from flask import Blueprint, request
from flask import jsonify, g

from ..user import auth
from ...models import db
from ...models.user import User, UserConfig
from ...logger import logger

admin = Blueprint('admin', __name__)


# ---------------------------------------------------------------------------------
# admin模块相关接口
# ---------------------------------------------------------------------------------


@admin.route('/updates', methods=['POST'])
@auth.login_required
def updates():
    """
    用户信息更新
    """
    action = request.get_json()['action']  # 1、 chgpsw 修改密码  2、 删除用户 deluser 3、一般更新操作 update
    if action == 'chgpsw':
        psw = request.get_json()['password']
        email = request.get_json()['email']
        try:
            logger.info("Set email:{} psw as default{}".format(email, psw))
            usr = User.query.filter_by(email=email).first()
            usr.password = psw
            db.session.add(usr)
            db.session.commit()
            code = 200
            msg = 'success'
        except Exception as e:
            logger.error("Set email:{} psw fail".format(email, psw))
            logger.error("Error is {}".format(e))
            code = 400
            msg = 'fail'
        return jsonify({'action': action, 'code': code, 'msg': msg})
    elif action == 'deluser':
        email = request.get_json()['email']
        try:
            logger.info("Del user email:{} ".format(email))
            usr = User.query.filter_by(email=email).first()
            db.session.delete(usr)
            db.session.commit()
            code = 200
            msg = 'success'
        except Exception as e:
            logger.error("Del user email:{} fail".format(email))
            logger.error("Error is {}".format(e))
            code = 400
            msg = 'fail'
        return jsonify({'action': action, 'code': code, 'msg': msg})
    else:
        email = request.get_json()['email']
        wordsbook = request.get_json()['wordsbook']
        try:
            logger.info(" update email:{} set wordsbook {}".format(email, wordsbook))
            usr = User.query.filter_by(email=email).first()
            usr.config.words_book = wordsbook
            db.session.add(usr)
            db.session.commit()
            code = 200
            msg = 'success'
        except Exception as e:
            logger.error("update user email:{} wordsbook fail".format(email))
            logger.error("Error is {}".format(e))
            code = 400
            msg = 'fail'
        return jsonify({'action': action, 'code': code, 'msg': msg})


@admin.route("/users", methods=['GET'])
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
            'wordsbook': UserConfig.query.filter_by(user_id=item.id).first().words_book
         } for item in users_obj
    ]
    return jsonify(res)

