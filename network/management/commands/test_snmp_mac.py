import logging

from pysnmp.entity.rfc3413.oneliner import cmdgen
from network.models import Switch

from django.core.management.base import BaseCommand, CommandError

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    args = ''
    help = 'Does some switch stuffs'

    def handle(self, *args, **options):
        switch = Switch.objects.get(id=1)

        ip = switch.ip
        security_name = switch.snmp_username
        auth_key = switch.snmp_auth_pass
        privacy_key = switch.snmp_priv_pass

        mac_address_list = (1,3,6,1,2,1,17,4,3,1,1)


        #value = ('.1.3.6.1.6.3.1.1.5.1')

        # Re-use this as much as possible!!
        cmdGen = cmdgen.CommandGenerator()

        errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
            cmdgen.UsmUserData(
                security_name, auth_key, privacy_key,
                authProtocol=cmdgen.usmHMACSHAAuthProtocol,
                privProtocol=cmdgen.usmAesCfb128Protocol
            ),
            cmdgen.UdpTransportTarget((ip, 161)),

            mac_address_list
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
                for varBindTableRow in varBindTable:
                    for name, val in varBindTableRow:
                        print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))