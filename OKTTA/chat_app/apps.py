from django.apps import AppConfig


class ChatAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat_app'

    def ready(self):
        import chat_app.schema

        from .scheduler import start_scheduler
        start_scheduler()
