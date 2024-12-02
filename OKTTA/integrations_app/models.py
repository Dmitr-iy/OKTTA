from django.db import models
import uuid

from user_app.models import User


class Integration(models.Model):
    CHOICES = (
        ('VK', 'ВКонтакте'),
        ('Whatsapp', 'WhatsApp'),
        ('telegram', 'Telegram'),
    )

    id_integration = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, choices=CHOICES)
    instructions = models.TextField()
    api_key = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='integrations')

    def __str__(self):
        return f"{self.user.email} - {self.name}"
