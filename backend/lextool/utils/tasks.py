import time

from celery import Celery

from .send_email import send_email
from ..config.default import DefaultConfig

app = Celery('tasks', broker='redis://127.0.0.1:6379/8')


@app.task
def send_register_active_email(email, username, token):
    """
    发送激活邮件
    :param email: email address
    :param username: email to who
    :param token: email token
    :return: None
    """
    # 组织邮件信息
    subject = '欢迎注册lex吐司'
    receiver = email
    # html_pattern = """<h2>Hi {}, 欢迎注册lex吐司</h2>请点击下方的链接激活你的账户<br><a href="http://{}/user/active/{}">http://{}/user/active/{}</a>"""
    html_pattern = """
        <h2>Hi {}, </h2>Click the link to active your account
        <a href="http://{}/user/active/{}">http://{}/user/active/{}</a>
    """
    html_message = html_pattern.format(username, DefaultConfig.Domain, token, DefaultConfig.Domain, token)
    send_email(subject, receiver, html_message=html_message)
