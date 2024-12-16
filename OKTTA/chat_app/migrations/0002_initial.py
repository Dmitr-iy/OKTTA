# Generated by Django 5.1.3 on 2024-12-14 19:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('chat_app', '0001_initial'),
        ('integrations_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='integration',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chats', to='integrations_app.integration'),
        ),
        migrations.AddField(
            model_name='managerchat',
            name='chat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manager_chats', to='chat_app.chat'),
        ),
    ]
