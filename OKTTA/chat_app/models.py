from django.db import models

from integrations_app.models import Integration
from user_app.models import Manager, User


class Chat(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    integration = models.ForeignKey(Integration, null=True, blank=True, on_delete=models.SET_NULL, related_name='chats')

    def __str__(self):
        return self.title


class ManagerChat(models.Model):
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name='manager_chats')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='manager_chats')

    class Meta:
        unique_together = ('manager', 'chat')

    def __str__(self):
        return f"{self.manager.user.email} in chat {self.chat.title}"


class UserChat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_chats')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='user_chats')

    class Meta:
        unique_together = ('user', 'chat')

    def __str__(self):
        return f"{self.user.email} in chat {self.chat.title}"


class Sender(models.Model):
    SENDER_TYPE_CHOICES = (
        ('user', 'User '),
        ('manager', 'Manager'),
        ('ai', 'AI'),
        ('integration', 'Integration'),
    )

    name = models.CharField(max_length=255)
    sender_type = models.CharField(max_length=20, choices=SENDER_TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.sender_type})"


class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    sender = models.ForeignKey(Sender, on_delete=models.CASCADE, related_name='messages')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    nickname = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.sender.name}: {self.content[:20]}..."
