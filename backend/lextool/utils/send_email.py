import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from ..config.default import DefaultConfig
from ..logger import logger


def send_email(subject, receiver, html_message):
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = DefaultConfig.MAIL_USER
    msg['To'] = receiver
    html_message = MIMEText(html_message, 'html', 'utf-8')
    msg.attach(html_message)

    try:
        smtp_obj = smtplib.SMTP()
        smtp_obj.connect(DefaultConfig.MAIL_HOST, 25)    # 25 为 SMTP 端口号
        smtp_obj.login(DefaultConfig.MAIL_USER, DefaultConfig.MAIL_PASS)
        smtp_obj.sendmail(DefaultConfig.MAIL_USER, receiver, msg.as_string())
        smtp_obj.quit()
        logger.info("邮件发送成功")
    except smtplib.SMTPException as e:
        logger.error("Error: 无法发送邮件")
