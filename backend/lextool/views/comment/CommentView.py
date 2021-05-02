from flask import (Blueprint, request, jsonify, abort)

from backend.lextool.common.logger import LOG
from backend.lextool.common.cache import cache
from backend.lextool.models.comment import Comment

comment = Blueprint('comment', __name__)


# ---------------------------------------------------------------------------------
# 用户反馈 相关接口
# ---------------------------------------------------------------------------------


@comment.route("/", methods=['GET'])
# @cache.cached(timeout=1000*60, key_prefix='all_comments')
def get_all_comments():
    """
    加载所有可以展示的意见
    """
    data = Comment.load_show_able_comment()
    # abort(404, "Post id doesn't exist.")
    return jsonify({'data': data})


@comment.route("/new/", methods=['POST'])
def add_comment():
    """
    新增意见（评论）
    """
    email = request.get_json()['mail']
    comment_type = request.get_json()['type']
    content = request.get_json()['content']
    create_at = request.get_json()['date']
    LOG.info("Insert a new comment {}, {} at {}".format(email, comment_type, create_at))
    code, msg = Comment.insert(content, comment_type, email)
    return jsonify({'code': code, 'msg': msg})


@comment.route("/update/", methods=['POST'])
def review_comment():
    """
    管理员用， 审核评论
    """
    comment_id = request.get_json()['id']
    can_show = request.get_json()['can_show']
    logger.info("Review a comment id:{}".format(comment_id))
    msg, code = Comment.update(comment_id, can_show)
    return jsonify({'code': code, 'msg': msg})
