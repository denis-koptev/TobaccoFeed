# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-23 15:40
from __future__ import unicode_literals

from django.db import migrations, models
import user_page.models


class Migration(migrations.Migration):

    dependencies = [
        ('user_page', '0002_auto_20170623_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(null=True, upload_to=user_page.models.PathAndRename('user_page/static/user_page/avatars/')),
        ),
    ]
