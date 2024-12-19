from django.db import models


class Chat(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    integration = models.ForeignKey('integrations_app.Integration', null=True, blank=True, on_delete=models.SET_NULL, related_name='chats')
    manager = models.ForeignKey('user_app.Manager', null=True, blank=True, on_delete=models.SET_NULL, related_name='chat_managers')
    user = models.ForeignKey('user_app.User', on_delete=models.CASCADE, null=True, blank=True, related_name='chats')
    messanger_chat_id = models.CharField(max_length=255, null=True, blank=True, unique=True)

    def __str__(self):
        return f'{self.pk}'

    def message_count(self):
        return self.messages.count()


class Message(models.Model):
    CHOICES = (
        ('gpt', 'gpt'),
        ('manager', 'manager'),
        ('user', 'user'),
        ('admin', 'admin'),
    )
    nickname = models.CharField(max_length=255)
    chat = models.ForeignKey(Chat, related_name='messages', null=True, blank=True, on_delete=models.CASCADE)
    sender_type = models.CharField(max_length=255, choices=CHOICES)
    messages = models.TextField(verbose_name='сообщение')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.pk}'
