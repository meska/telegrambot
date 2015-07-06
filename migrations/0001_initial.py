# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('user_id', models.IntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=100, null=True, blank=True)),
                ('first_name', models.CharField(max_length=100, null=True, blank=True)),
                ('last_name', models.CharField(max_length=100, null=True, blank=True)),
                ('last_message', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='TelegramUserAlert',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('camera', models.CharField(max_length=100)),
                ('receive_alerts', models.BooleanField(default=False)),
                ('receive_alerts_from', models.TimeField(null=True, blank=True)),
                ('receive_alerts_to', models.TimeField(null=True, blank=True)),
                ('user', models.ForeignKey(to='telegrambot.TelegramUser')),
            ],
        ),
    ]
