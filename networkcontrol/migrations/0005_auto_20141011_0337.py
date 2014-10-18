# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('networkcontrol', '0004_auto_20141011_0337'),
    ]

    operations = [
        migrations.AddField(
            model_name='switch',
            name='password',
            field=models.CharField(default='asdf', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='switch',
            name='username',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
