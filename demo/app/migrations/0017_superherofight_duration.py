# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-06 18:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20170606_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='superherofight',
            name='duration',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]