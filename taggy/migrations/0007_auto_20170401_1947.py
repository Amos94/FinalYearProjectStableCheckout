# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-01 18:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taggy', '0006_auto_20170401_1945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tags',
            name='provideOrRequest',
            field=models.CharField(max_length=5),
        ),
    ]