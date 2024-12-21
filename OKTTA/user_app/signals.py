from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Manager
from .views import generate_token


@receiver(post_save, sender=Manager)
def send_confirmation_email(sender, instance, created, **kwargs):
    """
    Отправляет письмо с подтверждением email
    """
    if created:
        token = generate_token(instance)
        subject = 'Подтвердите email'
        message = (f'Для подтверждения email перейдите по ссылке:'
                   f' {settings.BASE_URL}/confirm/{token}/')
        send_mail(subject, message, settings.EMAIL_HOST_USER, [instance.email])

