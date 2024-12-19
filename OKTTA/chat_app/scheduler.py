from apscheduler.schedulers.background import BackgroundScheduler
from django.core.cache import cache
from .models import Chat

def message_count():
    chats = Chat.objects.all()
    for chat in chats:
        count = chat.message_count()
        cache.set(f'message_count_{chat.id}', count, timeout=60)


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(message_count, 'interval', minutes=1)
    scheduler.start()

    return scheduler
