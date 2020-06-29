import requests

from flask import Blueprint, request
from flask import jsonify

from backend.lextool.models.comment import Comment
from backend.lextool.logger import logger

sci = Blueprint('sci', __name__)


# ---------------------------------------------------------------------------------
# memo 相关接口
# ---------------------------------------------------------------------------------


@sci.route("/test", methods=['POST'])
def test_sci():
    url = request.get_json()['url']
    logger.info("Run a {} test of sci".format(url))
    try:
        response = requests.request('GET', url, timeout=5000)
        times = int(response.elapsed.total_seconds()*1000)
        code = 200
    except Exception as e:
        logger.error(e)
        times = -1
        code = 403
    return jsonify({'code': code, 'times': times})
