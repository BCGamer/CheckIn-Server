# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0012_auto_20150124_2242'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vlan',
            old_name='vlan_name',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='switch',
            name='snmp_auth_pass',
            field=models.CharField(max_length=50, null=b'true', verbose_name=b'Authentication Password', blank=b'true'),
        ),
        migrations.AlterField(
            model_name='switch',
            name='snmp_port',
            field=models.IntegerField(default=161, null=b'true', verbose_name=b'Port', blank=b'true'),
        ),
        migrations.AlterField(
            model_name='switch',
            name='snmp_priv_pass',
            field=models.CharField(max_length=50, null=b'true', verbose_name=b'Privacy Password', blank=b'true'),
        ),
        migrations.AlterField(
            model_name='switch',
            name='ssh_pass',
            field=models.CharField(max_length=50, null=b'true', verbose_name=b'Password', blank=b'true'),
        ),
        migrations.AlterField(
            model_name='switch',
            name='ssh_port',
            field=models.IntegerField(default=22, null=b'true', verbose_name=b'Port', blank=b'true'),
        ),
        migrations.AlterField(
            model_name='switch',
            name='ssh_user',
            field=models.CharField(max_length=50, null=b'true', verbose_name=b'Username', blank=b'true'),
        ),
    ]
