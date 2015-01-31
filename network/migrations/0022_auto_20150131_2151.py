# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0021_auto_20150131_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='switch',
            name='provider',
            field=models.CharField(max_length=30, verbose_name=b'Model', choices=[(b'Cisco_Catalyst_2950', b'HP Catalyst 2950'), (b'HP_Procurve_2524', b'HP Procurve 2524'), (b'HP_Procurve_2626', b'HP Procurve 2626'), (b'HP_Procurve_2650', b'HP Procurve 2650'), (b'MikrotikSwitch', b'Mikrotik Switch')]),
        ),
    ]
