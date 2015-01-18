# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0009_auto_20150118_0121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uplinkport',
            name='switch',
            field=models.ForeignKey(related_name=b'uplink_ports', to='network.Switch'),
        ),
    ]
