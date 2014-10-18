# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('networkcontrol', '0006_switch_requires_authentication'),
    ]

    operations = [
        migrations.AddField(
            model_name='switch',
            name='port',
            field=models.IntegerField(default=22),
            preserve_default=True,
        ),
    ]
