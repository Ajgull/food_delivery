from celery import shared_task
from django.core.mail import send_mail

from project import settings


@shared_task(bind=True)
def email_send(self, subject: str, message: str, emails: list) -> None:
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        emails,
        fail_silently=False,
    )


# celery -A project worker -E -l INFO
