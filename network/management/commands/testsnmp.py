import logging

from network.models import Switch

from django.core.management.base import BaseCommand, CommandError

from pysnmp.entity.rfc3413.oneliner import cmdgen

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    args = ''
    help = 'Does some switch stuffs'

    def handle(self, *args, **options):
        mac = '001f.161c.4c86'

        # vlan = switch.switch_vlan_clean.num
        #switch = Switch.objects.get(id=1)
        #switch.flip_vlan(mac)

        # print switch.snmp_find_port(mac)
        Switch.objects.flip_vlan(mac)