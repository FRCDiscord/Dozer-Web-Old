# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-06 22:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0003_mail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mail',
            name='discord_user',
        ),
        migrations.AddField(
            model_name='mail',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='public.UserInfo'),
        ),
        migrations.AlterField(
            model_name='mail',
            name='content',
            field=models.TextField(max_length=2000),
        ),
    ]