# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-26 01:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stockplot', '0010_auto_20160326_0129'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='stockdata',
            unique_together=set([('symbol', 'date')]),
        ),
    ]