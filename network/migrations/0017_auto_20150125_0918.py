# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0016_auto_20150125_0633'),
    ]

    operations = [
        migrations.AddField(
            model_name='switch',
            name='snmp_community',
            field=models.CharField(max_length=50, null=b'true', verbose_name=b'Community', blank=b'true'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='switch',
            name='snmp_security',
            field=models.CharField(default=b'noAuthNoPriv', choices=[(b'noAuthNoPriv', b'No Auth & No Priv'), (b'authNoPriv', b'Auth & No Priv'), (b'AuthPriv', b'Auth & Priv')], max_length=50, blank=b'true', null=b'true', verbose_name=b'Privacy Type'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='switch',
            name='snmp_username',
            field=models.CharField(max_length=50, null=b'true', verbose_name=b'Username', blank=b'true'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='switch',
            name='ip',
            field=models.GenericIPAddressField(verbose_name=b'IP Address'),
        ),
        migrations.AlterField(
            model_name='switch',
            name='provider',
            field=models.CharField(max_length=30, verbose_name=b'Model', choices=[(b'CiscoSwitch', b'Cisco Switch'), (b'HP_Procurve_2524', b'HP Procurve 2524'), (b'HP_Procurve_2626', b'HP Procurve 2626'), (b'HP_Procurve_2650', b'HP Procurve 2650'), (b'MikrotikSwitch', b'Mikrotik Switch')]),
        ),
        migrations.AlterField(
            model_name='switch',
            name='snmp_auth_type',
            field=models.CharField(default=b'usmNoAuthProtocol', choices=[(b'usmHMACMD5AuthProtocol', b'MD5'), (b'usmHMACSHAAuthProtocol', b'SHA'), (b'usmNoAuthProtocol', b'NONE')], max_length=50, blank=b'true', null=b'true', verbose_name=b'Authentication Type'),
        ),
        migrations.AlterField(
            model_name='switch',
            name='snmp_priv_type',
            field=models.CharField(default=b'usmAesCfb256Protocol', choices=[(b'usmAesCfb256Protocol', b'NONE'), (b'usmDESPrivProtocol', b'DES'), (b'usm3DESEDEPrivProtocol', b'3DES'), (b'usmAesCfb128Protocol', b'AES128'), (b'usmAesCfb192Protocol', b'AES192'), (b'usmAesCfb256Protocol', b'AES256')], max_length=50, blank=b'true', null=b'true', verbose_name=b'Privacy Type'),
        ),
    ]
