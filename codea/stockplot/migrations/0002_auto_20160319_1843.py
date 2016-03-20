# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-19 17:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockplot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='QuandlSymbol',
            field=models.CharField(default='Default', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='stock',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]