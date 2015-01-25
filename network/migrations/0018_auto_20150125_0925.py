# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0017_auto_20150125_0918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='switch',
            name='snmp_auth_type',
            field=models.CharField(default=b'usmNoAuthProtocol', max_length=50, verbose_name=b'Authentication Type', choices=[(b'usmHMACMD5AuthProtocol', b'MD5'), (b'usmHMACSHAAuthProtocol', b'SHA'), (b'usmNoAuthProtocol', b'NONE')]),
        ),
        migrations.AlterField(
            model_name='switch',
            name='snmp_priv_type',
            field=models.CharField(default=b'usmAesCfb256Protocol', max_length=50, verbose_name=b'Privacy Type', choices=[(b'usmAesCfb256Protocol', b'NONE'), (b'usmDESPrivProtocol', b'DES'), (b'usm3DESEDEPrivProtocol', b'3DES'), (b'usmAesCfb128Protocol', b'AES128'), (b'usmAesCfb192Protocol', b'AES192'), (b'usmAesCfb256Protocol', b'AES256')]),
        ),
        migrations.AlterField(
            model_name='switch',
            name='snmp_security',
            field=models.CharField(default=b'noAuthNoPriv', max_length=50, verbose_name=b'Security Type', choices=[(b'noAuthNoPriv', b'No Auth & No Priv'), (b'authNoPriv', b'Auth & No Priv'), (b'AuthPriv', b'Auth & Priv')]),
        ),
    ]
