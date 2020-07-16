from flask import Blueprint, request
from flask import jsonify, g

from ..user import auth
from ...models import db
from ...models.todo import TODO
from ...logger import logger

todo = Blueprint('todo', __name__)


@todo.route('/new', methods=['POST'])
@auth.login_required
def updates():
    """
    用户信息更新
    """
    todo = request.get_json()['todo']  # 1、 chgpsw 修改密码  2、 删除用户 deluser 3、一般更新操作 update
    try:
        TODO(user_id=g.user.id, todo=todo).save()
        code = 200
        msg = 'success'
    except Exception as e:
        logger.error(e)
        code = 400
        msg = 'error'
    return jsonify({'code': code, 'msg': msg})


@todo.route('/todos', methods=['GET'])
@auth.login_required
def get_todos():
    """
    用户信息更新
    """
    try:
        todos = TODO.load_todos(user_id=g.user.id)
        code = 200
        msg = 'success'
    except Exception as e:
        logger.error(e)
        todos = []
        code = 400
        msg = 'error'
    return jsonify({'code': code, 'msg': msg,'todos': todos})


@todo.route('/load_finish', methods=['GET'])
@auth.login_required
def get_finish():
    """
    获取完成的todo
    """
    try:
        finished_todos = TODO.load_finish(user_id=g.user.id)
        code = 200
        msg = 'success'
    except Exception as e:
        logger.error(e)
        finished_todos = []
        code = 400
        msg = 'error'
    return jsonify({'code': code, 'msg': msg, 'finished_todos': finished_todos})


@todo.route('/finish', methods=['POST'])
@auth.login_required
def finish():
    """
    完成todo
    """
    index = request.get_json()['id']
    flag = TODO.finish(index=index)
    if flag:
        code = 200
        msg = 'success'
    else:
        code = 400
        msg = 'error'
    return jsonify({'code': code, 'msg': msg})