# Generated by Django 5.1.3 on 2024-12-19 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0004_user_plan_user_tokens_purchased'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='plan_end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='plan_start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
