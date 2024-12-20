# Generated by Django 5.1.3 on 2024-12-19 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('basic', 'Базовый'), ('premium_light', 'Премиум Лайт'), ('premium_hard', 'Премиум Хард')], max_length=50, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tokens', models.PositiveIntegerField()),
            ],
        ),
    ]
