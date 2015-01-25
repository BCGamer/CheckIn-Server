# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_switch_port'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vlan_name', models.CharField(max_length=50, verbose_name=b'Name')),
                ('vlan_num', models.IntegerField(verbose_name=b'VLAN #')),
                ('vlan_type', models.CharField(default=b'NO', max_length=2, verbose_name=b'Type', choices=[(b'DI', b'Dirty'), (b'CL', b'Clean'), (b'NO', b'None')])),
                ('vlan_desc', models.TextField(null=b'true', verbose_name=b'Description', blank=b'true')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='switch',
            name='enabled',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='switch',
            name='ports',
            field=models.IntegerField(default=24, verbose_name=b'# of Ports'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='switch',
            name='switch_vlan_clean',
            field=models.ForeignKey(related_name=b'switch_vlan_clean', verbose_name=b'Clean', blank=b'true', to='network.Vlan', null=b'true'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='switch',
            name='switch_vlan_dirty',
            field=models.ForeignKey(related_name=b'switch_vlan_dirty', verbose_name=b'Dirty', blank=b'true', to='network.Vlan', null=b'true'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='switch',
            name='provider',
            field=models.CharField(max_length=30, verbose_name=b'Type', choices=[(b'CiscoSwitch', b'Cisco Switch'), (b'HPSwitch', b'HP Switch'), (b'MikrotikSwitch', b'Mikrotik Switch')]),
        ),
    ]
