# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-06 21:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_page', '0007_usertobacco'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertobacco',
            name='is_bookmark',
            field=models.BooleanField(default=False),
        ),
    ]
