from apscheduler.schedulers.background import BackgroundScheduler
from django.core.cache import cache
from .models import User

def update_chat_message_count():
    users = User.objects.all()
    for user in users:
        count = user.chat_message_count()
        cache.set(f'chat_message_count_{user.id}', count, timeout=60)


def chat_count():
    users = User.objects.all()
    for user in users:
        count = user.chat_count()
        cache.set(f'chat_count_{user.id}', count, timeout=60)


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(chat_count, 'interval', minutes=1)
    scheduler.add_job(update_chat_message_count, 'interval', minutes=1)
    scheduler.start()

    return scheduler
