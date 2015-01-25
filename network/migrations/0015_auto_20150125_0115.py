# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0014_auto_20150124_2258'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vlan',
            options={'verbose_name': 'VLAN', 'verbose_name_plural': 'VLANs'},
        ),
        migrations.AlterField(
            model_name='switch',
            name='switch_vlan_clean',
            field=models.ForeignKey(related_name=b'switch_vlan_clean', verbose_name=b'Clean', blank=b'true', to='network.Vlan', null=b'true'),
        ),
        migrations.AlterField(
            model_name='switch',
            name='switch_vlan_dirty',
            field=models.ForeignKey(related_name=b'switch_vlan_dirty', verbose_name=b'Dirty', blank=b'true', to='network.Vlan', null=b'true'),
        ),
    ]
