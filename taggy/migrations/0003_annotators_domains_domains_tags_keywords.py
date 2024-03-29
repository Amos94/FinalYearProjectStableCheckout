# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-28 09:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taggy', '0002_auto_20170328_1028'),
    ]

    operations = [
        migrations.CreateModel(
            name='Annotators_domains',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annotatorId', models.IntegerField()),
                ('domainId', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Annotator domains',
            },
        ),
        migrations.CreateModel(
            name='Domains',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Domains/ Corpus',
            },
        ),
        migrations.CreateModel(
            name='Tags_keywords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tagId', models.IntegerField()),
                ('keywordsList', models.FileField(upload_to='keywords')),
                ('domainId', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Tags keywords',
            },
        ),
    ]
