from django.apps import AppConfig


class IntegrationsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'integrations_app'

    def ready(self):
        import integrations_app.signals
        import integrations_app.schema
