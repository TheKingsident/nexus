from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 60})
def send_welcome_email(self, user_email, username):
    """Send welcome email to new user"""
    try:
        subject = 'Welcome to Nexus!'
        message = f'Hi {username},\n\nThank you for registering at Nexus. We are excited to have you on board!'
        
        result = send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            fail_silently=False,
        )
        
        if result:
            logger.info(f"Welcome email sent successfully to {user_email}")
            return f"Email sent to {user_email}"
        else:
            logger.error(f"Failed to send welcome email to {user_email}")
            raise Exception("Email sending failed")
            
    except Exception as exc:
        logger.error(f"Error sending welcome email to {user_email}: {str(exc)}")
        # If we've exceeded retries, don't fail silently
        if self.request.retries >= self.max_retries:
            logger.error(f"Failed to send email to {user_email} after {self.max_retries} retries")
        raise self.retry(exc=exc)
