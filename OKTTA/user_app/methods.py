from django.utils import timezone
from datetime import timedelta
from django.core import signing

from chat_app.models import Message


def messages_to_day(self):
    """
    Возвращает количество сообщений от sender_type='client' за сегодня
    """
    today = timezone.now().date()
    return Message.objects.filter(
        chat__user=self,
        sender_type='client',
        created_at__date=today
    ).count()


def messages_last_week(self):
    """
    Возвращает количество сообщений от sender_type='client' за последнюю неделю
    """
    one_week_ago = timezone.now() - timedelta(weeks=1)
    return Message.objects.filter(
        chat__user=self,
        sender_type='client',
        created_at__gte=one_week_ago
    ).count()


def messages_last_month(self):
    """
    Возвращает количество сообщений от sender_type='client' за последнюю месяц
    """
    one_month_ago = timezone.now() - timedelta(days=30)
    return Message.objects.filter(
        chat__user=self,
        sender_type='client',
        created_at__gte=one_month_ago
    ).count()


def generate_token(manager):
    """
    Генерирует токен для подтверждения почты менеджера
    """
    print(manager.id)
    return signing.dumps(manager.id)
