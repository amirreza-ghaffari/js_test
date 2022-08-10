from django.conf import settings
from django.core.mail import send_mail
from .models import Block


def custom_send_email(message, to_email_list, subject='BCM Management'):
    send_mail(subject, message, settings.EMAIL_HOST_USER, to_email_list)








