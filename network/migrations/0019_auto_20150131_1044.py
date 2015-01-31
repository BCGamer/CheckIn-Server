# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0018_auto_20150125_0925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='switch',
            name='snmp_auth_type',
            field=models.CharField(default=(1, 3, 6, 1, 6, 3, 10, 1, 1, 1), max_length=50, verbose_name=b'Authentication Type', choices=[((1, 3, 6, 1, 6, 3, 10, 1, 1, 2), b'MD5'), ((1, 3, 6, 1, 6, 3, 10, 1, 1, 3), b'SHA'), ((1, 3, 6, 1, 6, 3, 10, 1, 1, 1), b'NONE')]),
        ),
        migrations.AlterField(
            model_name='switch',
            name='snmp_priv_type',
            field=models.CharField(default=(1, 3, 6, 1, 4, 1, 9, 12, 6, 1, 2), max_length=50, verbose_name=b'Privacy Type', choices=[((1, 3, 6, 1, 4, 1, 9, 12, 6, 1, 2), b'NONE'), ((1, 3, 6, 1, 6, 3, 10, 1, 2, 2), b'DES'), ((1, 3, 6, 1, 6, 3, 10, 1, 2, 3), b'3DES'), ((1, 3, 6, 1, 6, 3, 10, 1, 2, 4), b'AES128'), ((1, 3, 6, 1, 4, 1, 9, 12, 6, 1, 1), b'AES192'), ((1, 3, 6, 1, 4, 1, 9, 12, 6, 1, 2), b'AES256')]),
        ),
    ]
