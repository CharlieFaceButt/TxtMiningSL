# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-02 23:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sentanalyze', '0004_auto_20160502_2319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mostcommonquery',
            name='drift_time',
            field=models.DateTimeField(null=True),
        ),
    ]
