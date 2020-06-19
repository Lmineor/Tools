from flask import request
from flask import redirect
from flask import Blueprint
from flask import jsonify
from flask import render_template

from ...logger import logger
from ...models.dwz import DWZ
from ...models import db
from ...utils.generate_dwz import generate_dwz


dwz = Blueprint('dwz', __name__)


@dwz.route('/restore', methods=['POST'])
def fetch_origin_url():
    """
    短链还原
    """
    dwz = request.get_json()['dwz']
    if not dwz or len(dwz) != 6:
        return jsonify({
            'code': 200,
            'url': '还原失败,短链不存在'
        })
    logger.info("要还原的短链为：{}".format(dwz))
    try:
        item = DWZ.query.filter_by(dwz=dwz).first()
        url = item.url
    except Exception as e:
        url = '还原失败,短链不存在'
        logger.error(e)
    return jsonify({
        'code': 200,
        'url': url
    })


@dwz.route('/dwz', methods=['POST'])
def main():
    url = request.get_json()['url']
    logger.info('输入的url为：' + url)
    if not url:
        return None
    dwz = __pre_fetch(url)  # 先查库，看是否存在该短链
    if not dwz:
        try:
            obj = DWZ(url=url)
            db.session.add(obj)
            db.session.flush()
            dwz = generate_dwz(obj.id)  # 生成短链
            logger.info("Raw url is {}, After dwz is {}".format(url, dwz))
            obj.dwz = dwz
            db.session.add(obj)
            db.session.commit()
        except Exception as e:
            logger.error("Error is {}".format(e))
    data = {
        'code': 200,
        'url': dwz
    }
    return jsonify(data)


def __pre_fetch(url):
    """
    先去数据库查这个url，若有则返回该url对应的短网址
    :param url: 要转换的网址
    :return: 短网址或空
    """
    res = ''
    try:
        item = DWZ.query.filter_by(url=url).first()
        res = item.dwz if item else ''
    except Exception as e:
        logger.error("Error is {}".format(e))
    return res


@dwz.route('/s/<code>', methods=['GET'])
def redir(code):
    """
    重定向部分
    """
    try:
        item = DWZ.query.filter_by(dwz == str(code)).first()
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