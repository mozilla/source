from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import smart_str


def send_multipart_email(subject, from_email, to, text_content, html_content):
    text_content = smart_str(text_content)
    html_content = smart_str(html_content)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to,])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
