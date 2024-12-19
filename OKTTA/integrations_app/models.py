from django.db import models
import uuid


class Integration(models.Model):
    CHOICES = (
        ('VK', 'ВКонтакте'),
        ('Telegram', 'Telegram'),
        ('WhatsApp', 'WhatsApp'),
    )

    id_integration = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, choices=CHOICES, unique=True)
    api_key = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey('user_app.User', on_delete=models.CASCADE, related_name='integrations', null=True, blank=True)

    def __str__(self):
        return f"{self.id_integration}"
