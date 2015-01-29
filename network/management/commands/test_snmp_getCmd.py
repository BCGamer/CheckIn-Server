import logging

from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902
from network.models import Switch
from netaddr import *

from django.core.management.base import BaseCommand, CommandError

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    args = ''
    help = 'Does some switch stuffs'

    def handle(self, *args, **options):
        mac_matches = ()
        bridge_matches = ()
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

        # oid_mac = (1,3,6,1,2,1,17,4,3,1,1)
        # oid_ifindex = (1,3,6,1,2,1,2,2,1,1)
        # oid_port = (1,3,6,1,2,1,31,1,1,1,1)
        dot1dtpfdbaddress = '1.3.6.1.2.1.17.4.3.1.1'    # MAC address
        dot1dtpfdbport = '1.3.6.1.2.1.17.4.3.1.2'       # Bridge port
        ifindex = '1.3.6.1.2.1.2.2.1.1'                 # Interface index
        ifname = '1.3.6.1.2.1.31.1.1.1.1'               # Interface name

        # Re-use this as much as possible!!
        comm = cmdgen.CommandGenerator()

        # Find all MAC addresses connected with this device
        errorIndication, errorStatus, errorIndex, varBindTable = comm.nextCmd(
            snmp_user, snmp_target,
            #(1,3,6,1,2,1,17,4,3,1,1)    # dot1dTpFdbAddress - MAC Address
            dot1dtpfdbaddress
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

                        if val == EUI(mac, dialect=mac_cisco):
                            name = str(name).replace(dot1dtpfdbaddress, '')
                            mac_matches += (name, )

        # Find all bridges attached to this device
        for oid in mac_matches:
            print (dot1dtpfdbport + str(oid))
            errorIndication, errorStatus, errorIndex, varBinds = comm.getCmd(
                snmp_user, snmp_target,
                (dot1dtpfdbport + str(oid)),
                lookupNames=True, lookupValues=True
            )
            name, value = varBinds[0]
            print name
            print value