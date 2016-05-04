# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-02 23:19
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('sentanalyze', '0003_auto_20160502_2235'),
    ]

    operations = [
        migrations.RenameField(
            model_name='queryresult',
            old_name='query',
            new_name='result_query',
        ),
        migrations.RemoveField(
            model_name='mostcommonquery',
            name='freq',
        ),
        migrations.RemoveField(
            model_name='mostcommonquery',
            name='query',
        ),
        migrations.AddField(
            model_name='mostcommonquery',
            name='drift_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 2, 23, 19, 8, 798335, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='mostcommonquery',
            name='most_common',
            field=models.CharField(default='default', max_length=200),
        ),
    ]
