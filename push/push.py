import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from configs import configs


def send_alert(message):
    smtp = smtplib.SMTP_SSL(configs.smtp.host)
    smtp.ehlo(configs.smtp.host)
    smtp.login(*configs.smtp.login)
    email = MIMEText(message, 'html', 'utf-8')
    email['From'] = Header('电量告警', 'utf-8')
    email['To'] = Header('User', 'utf-8')
    email['Subject'] = Header('宿舍余电即将不足', 'utf-8')
    smtp.sendmail(configs.smtp.sender, [configs.smtp.receiver], email.as_string())


# images: list[(bytes, id: str)]
def send_report(message, images):
    smtp = smtplib.SMTP_SSL(configs.smtp.host)
    smtp.ehlo(configs.smtp.host)
    smtp.login(*configs.smtp.login)
    email = MIMEMultipart()
    body = MIMEText(message, 'html', 'utf-8')
    email['From'] = Header('用电报告', 'utf-8')
    email['To'] = Header('User', 'utf-8')
    email['Subject'] = Header('点击查看您上个月的用电详情', 'utf-8')
    email.attach(body)
    for image, id_str in images:
        mime = MIMEImage(image)
        mime.add_header('Content-ID', id_str)
        email.attach(mime)
    smtp.sendmail(configs.smtp.sender, [configs.smtp.receiver], email.as_string())
