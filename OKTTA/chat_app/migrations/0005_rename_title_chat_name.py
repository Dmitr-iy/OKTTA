# Generated by Django 5.1.3 on 2024-12-16 09:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat_app', '0004_alter_userchat_unique_together_remove_userchat_chat_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chat',
            old_name='title',
            new_name='name',
        ),
    ]
