import yagmail
from celery import Celery

yag = yagmail.SMTP('raghoram2009@gmail.com', '13811389B1E14')

app = Celery('mail', broker='amqp://localhost//',
             CELERY_IMPORTS=("mail"))


@app.task
def send_with_attachment(to, subject, content, attachment):
    yag.send(
        to=to,
        subject=subject,
        contents=content,
        attachments=attachment,
    )


@app.task
def send_without_attachment(to, subject, content):
    yag.send(
        to=to,
        subject=subject,
        contents=content
    )

