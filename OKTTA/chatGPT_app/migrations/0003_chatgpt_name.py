# Generated by Django 5.1.3 on 2024-12-19 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatGPT_app', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatgpt',
            name='name',
            field=models.CharField(default='gpt', max_length=255),
        ),
    ]