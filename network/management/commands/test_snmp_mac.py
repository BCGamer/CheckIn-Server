import logging

from pysnmp.entity.rfc3413.oneliner import cmdgen
from network.models import Switch
from netaddr import *

from django.core.management.base import BaseCommand, CommandError

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    args = ''
    help = 'Does some switch stuffs'

    def handle(self, *args, **options):
        mac_matches = {}
        switch = Switch.objects.get(id=1)

        mac = '001f.161c.4c86'
        ip = switch.ip

        snmp_user = cmdgen.UsmUserData(
            switch.snmp_username,
            switch.snmp_auth_pass,
            switch.snmp_priv_pass,
            authProtocol=cmdgen.usmHMACSHAAuthProtocol,
            privProtocol=cmdgen.usmAesCfb128Protocol)

        snmp_target = cmdgen.UdpTransportTarget((ip, 161))

        oid_mac = (1,3,6,1,2,1,17,4,3,1,1)
        oid_ifindex = (1,3,6,1,2,1,2,2,1,1)
        oid_port = (1,3,6,1,2,1,31,1,1,1,1)

        # Re-use this as much as possible!!
        comm = cmdgen.CommandGenerator()

        # Check for MAC addresses that match
        errorIndication, errorStatus, errorIndex, varBindTable = comm.nextCmd(
            snmp_user, snmp_target,
            (1,3,6,1,2,1,17,4,3,1,1)
        )

        if errorIndication:
            print(errorIndication)
        else:
            if errorStatus:
                print('%s at %s' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
                    )
                )
            else:
                # Loop through all
                for varBindTableRow in varBindTable:
                    for name, val in varBindTableRow:
                        val = val.prettyPrint()[2:]
                        val = EUI(val, dialect=mac_cisco)

                        # get oid name (as object instance) like: 1.3.6.1.2.1.17.4.3.1.1.0.20.105.84.18.25
                        # modify name so it doesn't include oid 1.3.6.1.2.1.17.4.3.1.1
                        # return output as tuple
                        name = str(name)[23:]   # Strip 1.3.6.1.2.1.17.4.3.1.1.
                        name = tuple(name.split("."))

                        if val == EUI(mac, dialect=mac_cisco):
                            mac_matches[name] = val
                            print "%s = %s" % (name, val)

        #

    def snmp_locate_bridge(self, comm, snmp_user, snmp_target, oid):
        oid_bridge = (1,3,6,1,2,1,17,4,3,1,2)

        errorIndication, errorStatus, errorIndex, varBindTable = comm.nextCmd(
            snmp_user, snmp_target, oid_bridge
        )

        if errorIndication:
            print(errorIndication)
        else:
            if errorStatus:
                print('%s at %s' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
                    )
                )
            else:
                # Loop through all
                for varBindTableRow in varBindTable:
                    for name, val in varBindTableRow:
                        val = val.prettyPrint()[2:]
                        val = EUI(val, dialect=mac_cisco)
