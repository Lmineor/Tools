# -*- coding:utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

from ..config.default import DefaultConfig
from ..logger import logger

import traceback
import sys
# sys.setdefaultencoding('utf-8')

def send_email(subject, receiver, html_message):
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = DefaultConfig.MAIL_USER
    msg['To'] = receiver
    html = MIMEText(html_message.encode('utf-8'), 'plain', 'utf-8')
    msg.attach(html)
    try:
        smtp_obj = smtplib.SMTP()
        smtp_obj.connect(DefaultConfig.MAIL_HOST, 25)    # 25 为 SMTP 端口号
        smtp_obj.login(DefaultConfig.MAIL_USER, DefaultConfig.MAIL_PASS)
        smtp_obj.sendmail(DefaultConfig.MAIL_USER, receiver, msg.as_string())
        smtp_obj.quit()
        logger.info("邮件发送成功")
    except smtplib.SMTPException as e:
        logger.error(e)
        logger.error("Error: 无法发送邮件")
    except Exception as e:
        exc_type, exc_value, exc_traceback_obj = sys.exc_info()
        traceback.print_tb(exc_traceback_obj)
