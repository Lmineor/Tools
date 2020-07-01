import datetime

from . import db
from ..logger import logger
from ..cache import cache


class Comment(db.Model):
    """
    反馈意见数据库
    """
    __tablename__ = 'comment'  # 用户反馈表
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255))                                         # 反馈内容
    solve = db.Column(db.String(100))                                           # 回复内容
    comment_type = db.Column(db.String(10), nullable=False, index=True)         # 类型
    is_show = db.Column(db.Boolean, default=True)                               # 是否评论区可见
    can_show = db.Column(db.Boolean, default=False)                             # 是否通过审核予以展示
    email = db.Column(db.String(100), nullable=False, index=True)
    create_at = db.Column(db.DateTime, default=datetime.date.today())           # 反馈时间
    is_solved = db.Column(db.Boolean, default=False)                            # 是否回复
    solved_at = db.Column(db.DateTime, nullable=True)                           # 回复时间

    @classmethod
    def load_show_able_comment(cls):
        try:
            all_comment = cls.query.order_by(cls.create_at.desc()).limit(30).all()
            data = [{'content': item.content,
                     'is_solved': item.is_solved,
                     'comment_type': item.comment_type,
                     'create_at': str(item.create_at)[:10]
                     } for item in all_comment if (item.is_show and item.can_show)
                    ]
        except Exception as e:
            logger.error('Error : {}'.format(e))
            data = []
        return data

    @staticmethod
    def save(content, comment_type, email):
        try:
            new_comment = Comment(content=content, comment_type=comment_type, email=email)
            db.session.add(new_comment)
            db.session.commit()
            code = 200
            msg = 'success'
        except Exception as e:
            logger.error(e)
            code = 403
            msg = e
        return code, msg
