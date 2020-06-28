from flask import Blueprint, request
from flask import jsonify

from ...models.comment import Comment
from ...logger import logger

helps = Blueprint('helps', __name__)


# ---------------------------------------------------------------------------------
# memo 相关接口
# ---------------------------------------------------------------------------------


@helps.route("/comment", methods=['GET', 'POST'])
def get_user_memo():
    if request.method == 'GET':
        data = Comment.load_show_able_comment()
        return jsonify({'data': data})
    else:
        mail = request.get_json()['mail']
        type = request.get_json()['type']
        content = request.get_json()['content']
        date = request.get_json()['date']
        data = Comment.save(content, type, mail, date)
        return jsonify(data)
