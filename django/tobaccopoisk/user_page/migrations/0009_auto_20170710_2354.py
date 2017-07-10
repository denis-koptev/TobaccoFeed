# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-10 20:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth_page', '0001_initial'),
        ('tobacco_page', '0003_auto_20170623_1755'),
        ('user_page', '0008_usertobacco_is_bookmark'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMix',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating_vote', models.SmallIntegerField(blank=True, null=True)),
                ('is_favorite', models.BooleanField(default=False)),
                ('is_bookmark', models.BooleanField(default=False)),
                ('mix', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tobacco_page.Mix')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth_page.User')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='usertobacco',
            unique_together=set([('user', 'tobacco')]),
        ),
        migrations.AlterUniqueTogether(
            name='usermix',
            unique_together=set([('user', 'mix')]),
        ),
    ]
