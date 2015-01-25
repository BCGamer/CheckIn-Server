# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0011_auto_20150124_2232'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='switch',
            name='password',
        ),
        migrations.RemoveField(
            model_name='switch',
            name='username',
        ),
        migrations.AddField(
            model_name='switch',
            name='snmp_auth_pass',
            field=models.CharField(max_length=50, null=b'true', verbose_name=b'SNMP Authentication Password', blank=b'true'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='switch',
            name='snmp_port',
            field=models.IntegerField(default=161, null=b'true', verbose_name=b'SNMP Port', blank=b'true'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='switch',
            name='snmp_priv_pass',
            field=models.CharField(max_length=50, null=b'true', verbose_name=b'SNMP Privacy Password', blank=b'true'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='switch',
            name='ssh_pass',
            field=models.CharField(max_length=50, null=b'true', verbose_name=b'SSH Password', blank=b'true'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='switch',
            name='ssh_user',
            field=models.CharField(max_length=50, null=b'true', verbose_name=b'SSH Username', blank=b'true'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='switch',
            name='ssh_port',
            field=models.IntegerField(default=22, null=b'true', verbose_name=b'SSH Port', blank=b'true'),
        ),
    ]
