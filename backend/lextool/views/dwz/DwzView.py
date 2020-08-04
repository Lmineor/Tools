from threading import Lock

from flask import request
from flask import redirect
from flask import Blueprint
from flask import jsonify
from flask import render_template

from ...logger import logger
from ...models.dwz import DWZ
from ...models import db
from .DWZGenerator import DWZGenerator


dwz = Blueprint('dwz', __name__)


@dwz.route('/restore', methods=['POST'])
def fetch_origin_url():
    """
    短链还原
    """
    d = request.get_json()['dwz']
    if not d or len(d) != 6:
        return jsonify({
            'code': 200,
            'url': '还原失败,短链不存在'
        })
    logger.info("要还原的短链为：{}".format(dwz))
    try:
        item = DWZ.query.filter_by(dwz=dwz).first()
        url = item.url if item else '还原失败,短链不存在'
    except Exception as e:
        url = '还原失败,错误为{}'.format(e)
        logger.error(e)
    return jsonify({
        'code': 200,
        'url': url
    })


@dwz.route('/dwz', methods=['POST'])
def generator():
    url = request.get_json(force=True)['url']
    logger.info('输入的url为：' + url)
    if not url:
        return jsonify({'code': 400, 'msg': 'error'})
    try:
        obj = DWZ(url=str(url))
        db.session.add(obj)
        db.session.flush()
        d = DWZGenerator.generate(obj.id)  # 生成短链
        obj.dwz = d
        db.session.commit()
        code = 200
    except Exception as e:
        d = e
        code = 500
        logger.error("Error is {}".format(e))
    data = {
        'code': code,
        'url': d
    }
    return jsonify(data)


@dwz.route('/s/<code>', methods=['GET'])
def redir(code):
    """
    重定向部分
    """
    try:
        item = DWZ.query.filter_by(dwz=str(code)).first()
        url = item.url
    except Exception as e:
        url = ''
        logger.error("Error is {}".format(e))
    if not url:
        return render_template('404.html')
    elif not url.startswith('http'):
        return redirect('http://' + url)
    else:
        return redirect(url)
