# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-29 07:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('so', '0010_auto_20170429_0722'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='spidertask',
            options={'ordering': ['-id']},
        ),
    ]