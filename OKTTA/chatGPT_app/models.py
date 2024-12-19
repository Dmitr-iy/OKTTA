from django.db import models


class ChatGPT(models.Model):
    CHOICES = (
        ('company', 'Company'),
        ('services', 'Services'),
        ('regulations', 'Regulations'),
    )
    name = models.CharField(max_length=255, default='gpt')
    title = models.CharField(max_length=255, choices=CHOICES)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    instruction_file = models.FileField(upload_to='instructions/', null=True, blank=True)
    user = models.ForeignKey('user_app.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
