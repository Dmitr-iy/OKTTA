# Generated by Django 5.1.3 on 2024-12-19 13:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tariff_app', '0001_initial'),
        ('user_app', '0003_alter_manager_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='plan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tariff_app.plan'),
        ),
        migrations.AddField(
            model_name='user',
            name='tokens_purchased',
            field=models.PositiveIntegerField(default=0),
        ),
    ]