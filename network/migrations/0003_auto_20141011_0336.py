# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_switch_provider'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='switch',
            name='type',
        ),
        migrations.AlterField(
            model_name='switch',
            name='provider',
            field=models.CharField(max_length=30, verbose_name=b'Type', choices=[(b'CiscoSwitch', b'Cisco Switch'), (b'HPSwitch', b'HP Switch')]),
        ),
    ]
