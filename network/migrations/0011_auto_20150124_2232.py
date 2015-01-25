# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0010_auto_20150118_0334'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='switch',
            name='port',
        ),
        migrations.AddField(
            model_name='switch',
            name='ssh_port',
            field=models.IntegerField(default=22),
            preserve_default=True,
        ),
    ]
