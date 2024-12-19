from django.apps import AppConfig


class UserAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_app'

    def ready(self):
        import user_app.schema
        import user_app.signals

        from .scheduler import start_scheduler
        start_scheduler()
