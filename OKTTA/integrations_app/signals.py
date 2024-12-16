from django.db.models.signals import post_save
from django.dispatch import receiver

from integrations_app.models import Integration
from chat_app.models import Chat

@receiver(post_save, sender=Integration)
def create_chat_for_integration(sender, instance, created, **kwargs):
    if created:
        chat = Chat.objects.create(
            name=instance.name,
            integration=instance,
            user=instance.user
        )
        chat.save()


