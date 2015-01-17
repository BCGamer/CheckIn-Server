# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0005_auto_20140913_0515'),
    ]

    operations = [
        migrations.AddField(
            model_name='registereduser',
            name='age_under_18',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='registereduser',
            name='guardian_name',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='registereduser',
            name='guardian_phone',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='registereduser',
            name='nickname',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='registereduser',
            name='waiver_signed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
