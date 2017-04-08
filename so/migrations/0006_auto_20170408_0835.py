# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-08 08:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('so', '0005_auto_20170320_0803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='website',
            name='title',
            field=models.CharField(max_length=64, unique=True, verbose_name='标题'),
        ),
        migrations.AlterUniqueTogether(
            name='website',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='website',
            name='user',
        ),
    ]
