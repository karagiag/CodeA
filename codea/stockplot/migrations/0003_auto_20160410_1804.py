# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-10 16:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stockplot', '0002_auto_20160408_1758'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='depotcontent',
            unique_together=set([]),
        ),
    ]
