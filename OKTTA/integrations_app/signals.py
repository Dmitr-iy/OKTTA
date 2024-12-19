from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
import logging

from integrations_app.models import Integration

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Integration)
def create_chat(sender, instance, created, **kwargs):
    if created:
        token = instance.api_key
        webhook_url = settings.WEBHOOK_URL
        telegram_url = settings.TELEGRAM_URL
        id_integration = instance.id_integration
        try:
            response = requests.post(f'{telegram_url}{token}/setWebhook?'
                                     f'url={webhook_url}/webhook/{id_integration}/')
            response.raise_for_status()  # Проверка на ошибки HTTP
            logger.info(f'Установлен webhook: {response.text}')
            print(response.text)

        except requests.exceptions.RequestException as e:
            logger.error(f'Ошибка при установке webhook: {e}')
