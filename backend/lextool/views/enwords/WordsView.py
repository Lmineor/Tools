from flask import request
from flask import Blueprint
from flask import jsonify
from sqlalchemy.sql.expression import func

from ...logger import logger
from ...models.words import EnWords
from ...models import db


words = Blueprint('words', __name__)


@words.route('/daily', methods=['POST', 'GET'])
def get_daily_words():
    """
    短链还原部分
    """
    if request.method == 'GET':
        try:
            items = EnWords.query.order_by(func.rand()).limit(20)
            res = [{'word': item.word, 'translation': item.translation} for item in items]
        except Exception as e:
            res = []
            logger.error(e)
        return jsonify({
            'code': 200,
            'words': res
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

