from django.db import models

from user_app.models import User


class Widget(models.Model):
    widget_code = models.TextField()


class AutoMessages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    url = models.URLField()
    time = models.TimeField()
    text_message = models.TextField()

    def __str__(self):
        return self.title
