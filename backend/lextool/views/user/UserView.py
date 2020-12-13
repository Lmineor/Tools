from flask import Blueprint, request
from flask import jsonify, g


from ...auth import auth
from ...models import db
from ...models.user import User, UserConfig, UserMemo

from ...common.logger import LOG
from ...config.config import Cfg

user = Blueprint('user', __name__)


# ---------------------------------------------------------------------------------
# memo 相关接口
# ---------------------------------------------------------------------------------


@user.route("/memo", methods=['GET'])
@auth.login_required
def show_memo():
    memo = g.user.memo.memo
    return jsonify({'memo': memo})


@user.route("/memo/update", methods=['POST'])
@auth.login_required
def save_memo():
    memo = request.get_json()['memo']
    memo_obj = UserMemo.query.filter_by(user_id=g.user.id).first()
    memo_obj.memo = memo
    db.session.commit()
    return jsonify({'code': 200})


# ---------------------------------------------------------------------------------
# 用户更新自己信息相关接口
# ---------------------------------------------------------------------------------

@user.route("/info", methods=['POST', 'GET'])
@auth.login_required
def show_info():
    """
    获取当前登录用户的信息
    :return:
    """
    email = g.user.email
    words_book = g.user.config.words_book
    words_num = g.user.config.words_num
    return jsonify({'email': email, 'words_book': words_book, 'words_num': str(words_num)})


@user.route('/info/update', methods=['POST'])
@auth.login_required
def update_info():
    """
    用户信息更新
    """
    username = request.get_json()['username']
    email = request.get_json()['email']
    password = request.get_json()['password']
    words_book = request.get_json()['words_book']
    words_num = request.get_json()['words_num']
    words_num = int(words_num) if words_num in ['20', '50', '100', '200'] else 20
    try:
        user_config = UserConfig.query.filter_by(user_id=g.user.id).first()
        user_config.words_book = words_book
        user_config.words_num = words_num
        current_user = User.query.get(g.user.id)
        g.user.password = password
        if password:
            current_user.password = password
        current_user.username = username
        db.session.commit()

        msg = "success"
        code = 200
    except Exception as e:
        LOG.error("info update error {}".format(e))
        msg = "fail"
        code = 400
    res = {
        'code': code,
        'msg': msg
    }
    return jsonify(res)
