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
        cache.set(f'chat_message_count_{user.id}', count, timeout=10)
        print('coount', count)


def chat_count():
    """
    Обновляет количество чатов для каждого пользователя.
    """
    users = User.objects.all()
    for user in users:
        count = user.chat_count()
        cache.set(f'chat_count_{user.id}', count, timeout=60)


def start_scheduler():
    """
    Запуск планировщика.
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(chat_count, 'interval', minutes=1)
    scheduler.add_job(update_chat_message_count, 'interval', seconds=10)
    scheduler.start()

    return scheduler
