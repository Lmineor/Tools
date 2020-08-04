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
    is_useful = db.Column(db.Boolean, default=False)                            # 是否为有效建议
    email = db.Column(db.String(100), nullable=False, index=True)
    create_at = db.Column(db.DateTime, default=datetime.date.today())           # 反馈时间
    is_solved = db.Column(db.Boolean, default=False)                            # 是否操作
    solved_at = db.Column(db.DateTime, nullable=True)                           # 操作时间

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

    @classmethod
    def insert(cls, content, comment_type, email):
        try:
            new_comment = cls(content=content, comment_type=comment_type, email=email)
            db.session.add(new_comment)
            db.session.commit()
            code = 200
            msg = 'success'
        except Exception as e:
            logger.error(e)
            code = 403
            msg = e
        return code, msg

    def save(self, email=None, can_show=None, is_useful=None):
        if self.id:
            try:
                db.session.add(self)
                db.session.commit()
                code = 200
                msg = 'success'
            except Exception as e:
                logger.error(e)
                code = 403
                msg = e
            return code, msg

        if can_show and is_useful:
            self.can_show = can_show
            self.is_useful = is_useful
            self.solved_at = datetime.date.today()

        db.session.add(self)
        db.session.commit()
        return self

    # TODO：完善admin的相关内容
    @classmethod
    def review(cls, comment_id, key):
        try:
            sess = cls.query.get(comment_id)
            if key == "review":
                sess.can_show = True
            else:
                sess.is_solved = True
            db.session.commit()
            msg = 'success'
            code = 200
        except Exception as e:
            logger.error(e)
            msg = e
            code = 400
        return msg, code

    @classmethod
    def get_un_solved_queries(cls):
        try:
            queries = cls.query.filter_by(is_solved=False).all()
            data = [{
                'id': item.id,
                'email': item.email,
                'content': item.content,
                'is_solved': item.is_solved,
                'comment_type': item.comment_type,
                'create_at': str(item.create_at)[:10]
                } for item in queries]
        except Exception as e:
            logger.error(e)
            data = []
        return data
