#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

from oocfg import cfg

from backend.lextool.common.logger import LOG


def send_email(subject, receiver, html_message):
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = 'lex吐司管理员'
    msg['To'] = receiver
    u = html_message.encode('utf-8')
    html = MIMEText(html_message.encode('utf-8'), _subtype='html', _charset='utf-8')
    msg.attach(html)
    try:
        smtp_obj = smtplib.SMTP()
        smtp_obj.connect(cfg.CONF.EMAIL.host, 25)    # 25 为 SMTP 端口号
        smtp_obj.login(cfg.CONF.MAIL.username, cfg.CONF.MAIL.password)
        smtp_obj.sendmail(cfg.CONF.MAIL.username, receiver, msg.as_string())
        smtp_obj.quit()
        LOG.info("邮件发送成功")
    except smtplib.SMTPException as e:
        LOG.error(e)
        LOG.error("Error: 无法发送邮件")
    except Exception as e:
        LOG.error(e)
