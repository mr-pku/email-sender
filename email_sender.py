# -*- coding: UTF-8 -*-


#*************************************************
# Author: Rui Ma
# Email: ma_rui@pku.edu.cn
# Creation Date: 2025-11-29
#*************************************************


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr


def send_mail(
    smtp_server,
    smtp_port,
    smtp_user,
    smtp_pass,
    sender,
    receiver,  # 接收邮件
    subject,
    mail_content,  # 邮件正文内容
    cc_list=[],
    attachments=[],  # 附件
    mail_content_type="html",  # "plain" "html"
    sender_nick=None,
    receiver_nick=None,
):
    message = MIMEMultipart()
    message["From"] = formataddr([sender_nick, sender])
    message["To"] = formataddr([receiver_nick, receiver])
    message["Subject"] = Header(subject, "utf-8")

    all_receivers = [receiver]

    if cc_list:
        message["Cc"] = ";".join(cc_list)
        all_receivers += cc_list

    message.attach(MIMEText(mail_content, mail_content_type, "utf-8"))

    for att in attachments:
        att1 = MIMEText(open(att["file"], "rb").read(), "base64", "utf-8")
        att1["Content-Type"] = "application/octet-stream"
        att1.add_header(
            "content-disposition",
            "attachment",
            filename=("gbk", "", att["attachment_name"]),
        )
        message.attach(att1)

    try:
        smtpObj = smtplib.SMTP_SSL(smtp_server, smtp_port)
        smtpObj.login(smtp_user, smtp_pass)
        smtpObj.sendmail(sender, all_receivers, message.as_string())
        smtpObj.quit()
        return (True, "发送成功")
    except smtplib.SMTPException as e:
        return (False, "发送失败：" + str(e))


class Attachment:
    def __init__(self, file, attachment_name):
        self.file = file
        self.attachment_name = attachment_name

    def to_dict(self):
        return {
            "file": self.file,
            "attachment_name": self.attachment_name,
        }


class MailSender:
    def __init__(
        self,
        smtp_server,
        smtp_port,
        smtp_user,
        smtp_pass,
    ):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_pass = smtp_pass

        self.sender = self.smtp_user
        self.sender_nick = None
        self.receiver = None
        self.receiver_nick = None
        self.cc_list = []
        self.subject = None
        self.mail_content = None
        self.mail_content_type = "html"
        self.attachments = []

    def _handle_attachments(self, attachments=[]):
        _attachments = self.attachments
        if attachments:
            _attachments = attachments

        return map(lambda x: x.to_dict(), _attachments)

    def send(self, subject=None, content=None, attachments=[]):
        args = {
            "sender": self.sender,
            "sender_nick": self.sender_nick,
            "receiver": self.receiver,
            "receiver_nick": self.receiver_nick,
            "cc_list": self.cc_list,
            "subject": subject if subject else self.subject,
            "mail_content": content if content else self.mail_content,
            "mail_content_type": self.mail_content_type,
            "attachments": self._handle_attachments(attachments),
            "smtp_user": self.smtp_user,
            "smtp_pass": self.smtp_pass,
            "smtp_server": self.smtp_server,
            "smtp_port": self.smtp_port,
        }
        return send_mail(**args)


if __name__ == "__main__":
    args = {
        "sender": "ma_rui@pku.edu.cn",
        "sender_nick": "马睿",
        "receiver": "2401112561@stu.pku.edu.cn",
        "receiver_nick": "马同学",
        "subject": "Python SMTP 邮件测试",
        "mail_content": "<h1>测试</h1><p>段落1</p><p>段落2</p>",
        "mail_content_type": "html",
        "attachments": [
            {
                "file": "data/iShot_2024-07-18_14.58.04.png",
                "attachment_name": "ishot.png",
            },
            {
                "file": "data/FIB Discussion 20240701.pptx",
                "attachment_name": "FIB.pptx",
            },
        ],
        "cc_list": [],
        "smtp_server": "smtp.pku.edu.cn",
        "smtp_port": 465,
        "smtp_user": "ma_rui@pku.edu.cn",
        "smtp_pass": "",
    }
    print(send_mail(**args))
