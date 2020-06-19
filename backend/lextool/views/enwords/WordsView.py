from flask import request
from flask import Blueprint
from flask import jsonify, g
from sqlalchemy.sql.expression import func

from ..user import auth
from ...logger import logger
from ...models.words import Cet4, Cet6
from ...models import db
from ...utils.parseCharacter import parseSpelling

words = Blueprint('words', __name__)


@words.route('/daily', methods=['POST', 'GET'])
@auth.login_required
def get_daily_words():
    """
    获取每日单词
    """
    book = g.user.config.words_book
    if book == 'Cet4':
        DB = Cet4
    else:
        DB = Cet6
    if request.method == 'GET':
        try:
            items = DB.query.order_by(func.rand()).limit(20)
            res = [{'word': item.word, 'translation': item.translation, 'spellingA': parseSpelling(item.spellingA), 'spellingE': parseSpelling(item.spellingE)} for item in items]
        except Exception as e:
            res = []
            logger.error(e)
        return jsonify({
            'code': 200,
            'words': res,
            'book':book
        })
    # else:
    #     chapter = request.get_json()['chapter']
    #     logger.info('chapter: ' + chapter)
    #     if cache.get('chapter'):
    #         paragraphs = cache.get('chapter')
    #     else:
    #         try:
    #             paragraphs = PoemLunyu.query.filter_by(chapter=chapter).first().paragraphs
    #         except Exception as e:
    #             paragraphs = ''
    #             logger.error(e)
    #         cache.set(chapter, paragraphs)
    #     return jsonify({
    #         'code': 200,
    #         'paragraphs': paragraphs.split('|')
    #     })

