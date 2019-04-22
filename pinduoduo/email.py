# -*- coding:utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from pinduoduo.settings import *
import logging

class EmailSender(object):
    def __init__(self):
        """
        初始化邮箱配置
        """
        self.smtp_host = SMTP_HOST
        self.smtp_user = SMTP_USER
        self.smtp_authcode = SMTP_AUTHCODE      # 授权码
        self.smtp_port = SMTP_PORT
        self.sender = SENDER

    def sendEmail(self, recipient_list, subject, body):
        """
        发送邮件
        """
        # 邮件内容、格式、编码
        message = MIMEText(body, 'plain', 'utf-8')
        # 发件人
        message['From'] = self.sender
        # 收件人列表
        message['To'] = ''.join(recipient_list)
        # 主题
        message['subject'] = subject
        try:
            # 实例化邮件发送对象
            Client = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)
            # 登录
            LoginResult = Client.login(self.smtp_user, self.smtp_authcode)
            if LoginResult and LoginResult[0] == 235:
                Client.sendmail(self.sender, recipient_list, message.as_string())
                logging.debug("Sent successfully!")
            else:
                logging.debug("Failed to send")
        except Exception as e:
            print("Failed to send, Reason:{}".format(e.args))

if __name__ == '__main__':
    email = EmailSender()
    email.sendEmail(RECEIVE_LIST, subject=SUBJECT, body='test')