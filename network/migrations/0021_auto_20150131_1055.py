# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0020_auto_20150131_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='switch',
            name='snmp_auth_type',
            field=models.CharField(default=b'1,3,6,1,6,3,10,1,1,1', max_length=50, verbose_name=b'Authentication Type', choices=[(b'1,3,6,1,6,3,10,1,1,2', b'MD5'), (b'1,3,6,1,6,3,10,1,1,3', b'SHA'), (b'1,3,6,1,6,3,10,1,1,1', b'NONE')]),
        ),
        migrations.AlterField(
            model_name='switch',
            name='snmp_priv_type',
            field=models.CharField(default=b'1,3,6,1,4,1,9,12,6,12', max_length=50, verbose_name=b'Privacy Type', choices=[(b'1,3,6,1,4,1,9,12,6,12', b'NONE'), (b'1,3,6,1,6,3,10,1,2,2', b'DES'), (b'1,3,6,1,6,3,10,1,2,3', b'3DES'), (b'1,3,6,1,6,3,10,1,2,4', b'AES128'), (b'1,3,6,1,4,1,9,12,6,1,1', b'AES192'), (b'1,3,6,1,4,1,9,12,6,1,2', b'AES256')]),
        ),
    ]
