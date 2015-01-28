import logging
import re
from network.exceptions import MacNotFound

import os, sys
import socket
import random
from struct import pack, unpack
from datetime import datetime as dt

from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto.rfc1902 import Integer, IpAddress, OctetString

from network.models import Switch


from django.core.management.base import BaseCommand, CommandError

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    args = ''
    help = 'Does some switch stuffs'

    def handle(self, *args, **options):
        switch = Switch.objects.get(id=1)

        ip = '10.5.11.2'
        securityName = 'bcgamer'
        authKey = 'BCGamer2014!$'
        privKey = 'BCGamer12'

        value = (1,3,6,1,6,3,1,1,5,1)
        #value = ('.1.3.6.1.6.3.1.1.5.1')

        cmdGen = cmdgen.CommandGenerator()
        comm_data = cmdgen.UsmUserData(
            securityName,
            authKey=authKey,
            privKey=privKey,
            authProtocol='usmNoAuthProtocol',
            privProtocol='usmNoPrivProtocol'
        )
        transport = cmdgen.UdpTransportTarget((ip, 161))

        real_fun = getattr(cmdGen, 'nextCmd')
        res = (errorIndication, errorStatus, errorIndex, varBinds)\
            = real_fun(comm_data, transport, value)

        if not errorIndication is None or errorStatus is True:
            print "Error: %s %s %s %s" % res
        else:
            print "%s" % varBinds