from apscheduler.schedulers.background import BackgroundScheduler
from django.core.cache import cache

from .models import User

def update_chat_message_count():
    """
    Обновляет количество сообщений в чате для каждого пользователя.
    """
    users = User.objects.all()
    for user in users:
        count = user.chat_message_count()
        cache.set(f'chat_message_count_{user.id}', count, timeout=60)
        print('coount', count)


def chat_count():
    """
    Обновляет количество чатов для каждого пользователя.
    """
    users = User.objects.all()
    for user in users:
        count = user.chat_count()
        cache.set(f'chat_count_{user.id}', count, timeout=60)


def count_last_week():
    """
    Обновление количества сообщений от sender_type='client' за последнюю неделю. Запись в кэш
    """
    users = User.objects.all()
    for user in users:
        count = user.messages_last_week_clients()
        cache.set(f'messages_last_week_{user.id}', count, timeout=60)
        print(f'Количество сообщений от клиента за последнюю неделю для пользователя {user.id}: {count}')


def messages_last_month():
    """
    Обновление количества сообщений от sender_type='client' за последнюю месяц. Запись в кэш
    """
    users = User.objects.all()
    for user in users:
        count = user.messages_last_month_clients()
        cache.set(f'messages_last_month_{user.id}', count, timeout=60)
        print(f'Количество сообщений от клиента за последнюю месяц для пользователя {user.id}: {count}')


def messages_to_day():
    """
    Обновление количества сообщений от sender_type='client' за последний день. Запись в кэш
    """
    users = User.objects.all()
    for user in users:
        count = user.messages_to_day_clients()
        cache.set(f'messages_to_day_{user.id}', count, timeout=10)
        print(f'Количество сообщений от клиента за последний день для пользователя {user.id}: {count}')


def start_scheduler():
    """
    Запуск планировщика.
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(chat_count, 'interval', minutes=1)
    scheduler.add_job(update_chat_message_count, 'interval', minutes=1)
    scheduler.add_job(count_last_week, 'interval', minutes=1)
    scheduler.add_job(messages_last_month, 'interval', minutes=1)
    scheduler.add_job(messages_to_day, 'interval', minutes=1)
    scheduler.start()

    return scheduler
