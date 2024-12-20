from django.apps import AppConfig


class ChatgptAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chatGPT_app'

    def ready(self):
        import chatGPT_app.schema
        import chatGPT_app.signals
