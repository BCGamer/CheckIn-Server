# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0015_auto_20150125_0115'),
    ]

    operations = [
        migrations.AddField(
            model_name='switch',
            name='snmp_auth_type',
            field=models.CharField(max_length=50, null=b'true', verbose_name=b'Authentication Type', blank=b'true'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='switch',
            name='snmp_priv_type',
            field=models.CharField(max_length=50, null=b'true', verbose_name=b'Privacy Type', blank=b'true'),
            preserve_default=True,
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
