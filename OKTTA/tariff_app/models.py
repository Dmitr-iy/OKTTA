from django.db import models

class Plan(models.Model):
    PLAN_CHOICES = [
        ('basic', 'Базовый'),
        ('premium_light', 'Премиум Лайт'),
        ('premium_hard', 'Премиум Хард'),
    ]

    name = models.CharField(max_length=50, choices=PLAN_CHOICES, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tokens = models.PositiveIntegerField()

    def __str__(self):
        return self.name
