from flask import Blueprint, request
from flask import jsonify

from ...models.comment import Comment
from ...logger import logger

comment = Blueprint('comment', __name__)


# ---------------------------------------------------------------------------------
# memo 相关接口
# ---------------------------------------------------------------------------------


@comment.route("/", methods=['GET', 'POST'])
def get_comment():
    if request.method == 'GET':
        data = Comment.load_show_able_comment()
        return jsonify({'data': data})
    else:
        email = request.get_json()['mail']
        comment_type = request.get_json()['type']
        content = request.get_json()['content']
        create_at = request.get_json()['date']
        logger.info("Insert a new comment {}, {} at {}".format(email, comment_type, create_at))
        code, msg = Comment.save(content, comment_type, email)
        return jsonify({'code': code, 'msg': msg})
