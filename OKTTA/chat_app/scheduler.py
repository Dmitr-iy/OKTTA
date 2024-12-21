from apscheduler.schedulers.background import BackgroundScheduler
from django.core.cache import cache
from .models import Chat

def message_count():
    """
    Обновление количества сообщений в чатах. Запись в кэш
    """
    chats = Chat.objects.all()
    print(chats)
    for chat in chats:
        count = chat.message_count()
        cache.set(f'message_count_{chat.id}', count, timeout=60)

def messages_unread_count():
    """
    Обновление количества непрочитанных сообщений в чатах. Запись в кэш
    """
    chats = Chat.objects.all()
    for chat in chats:
        count = chat.messages_unread_count()
        cache.set(f'messages_unread_count_{chat.id}', count, timeout=60)


def start_scheduler():
    """
    Запуск планировщика
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(message_count, 'interval', minutes=1)
    scheduler.start()
    print("Scheduler started")

    return scheduler
