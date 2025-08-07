from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_welcome_email(user_email, username):
    subject = 'Welcome to Nexus!'
    message = f'Hi {username},\n\nThank you for registering at Nexus. We are excited to have you on board!'
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )
