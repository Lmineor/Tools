import datetime
from typing import List, Dict

from flask import request
from flask import Blueprint
from flask import jsonify, g
from sqlalchemy.sql.expression import func

from ..user import auth
from ...common.logger import LOG
from ...models.words import *
from ...models import db
from ...common.cache import cache
from ...utils.parseCharacter import parseSpelling

words = Blueprint('words', __name__)


@words.route('/daily', methods=['GET'])
@auth.login_required
def get_daily_words():
    """
    获取每日单词
    思路：如果用户请求的日期与数据库中create_at相同，则直接查库返回，否则重新生成新的单词，并存到数据库当中
    """
    refresh = request.args.get("refresh")  # 若有refresh请求，则刷新

    book = g.user.config.words_book
    words_num = g.user.config.words_num
    current_date = str(datetime.date.today())
    LOG.info("User {} get {} words".format(g.user.username, book))

    if book == 'CET4':
        source = Cet4
    elif book == 'CET6':
        source = Cet6
    elif book == 'TOEFL':
        source = TOEFL
    else:
        source = GRE

    word_items = db.session.query(DailyWords).filter(DailyWords.user_id == g.user.id).all()
    if not word_items:
        data = generate_user_daily_words(source, g.user.id, recited=[], words_num=words_num)
        cache.set(str(g.user.id) + current_date + book, data)
    elif str(word_items[0].create_at)[:10] != current_date or refresh:
        LOG.info("Refresh: {}".format(refresh))
        data = generate_user_daily_words(source, g.user.id, recited=[], words_num=words_num)
        cache.set(str(g.user.id) + current_date + book, data)
    else:
        has_cached = cache.get(str(g.user.id) + current_date + book)
        if has_cached:
            LOG.info('Get from cache')
            data = has_cached
        else:
            data = [{'word': item.word, 'translation': item.translation, 'spellingA': parseSpelling(item.spellingA),
                     'spellingE': parseSpelling(item.spellingE)} for item in word_items]
            cache.set(str(g.user.id) + current_date + book, data)

    return jsonify({
        'code': 200,
        'words': data,
        'book': book
    })


def generate_user_daily_words(source, user_id: int, recited: List, words_num: int) -> List[Dict]:
    try:
        items = source.query.order_by(func.rand()).limit(words_num)
        if recited:
            pass
        data = [{'word': item.word, 'translation': item.translation, 'spellingA': parseSpelling(item.spellingA),
                 'spellingE': parseSpelling(item.spellingE)} for item in items]
        db.session.query(DailyWords).filter(DailyWords.user_id == user_id).delete()  # 删除这个用户之前的所有数据
        for elem in data:
            user_d_w = DailyWords(user_id=user_id, word=elem['word'], translation=elem['translation'],
                                  spellingA=elem['spellingA'], spellingE=elem['spellingE'])
            db.session.add(user_d_w)
        db.session.commit()
    except Exception as e:
        LOG.error("Error is {}".format(e))
        data = []
    return data
