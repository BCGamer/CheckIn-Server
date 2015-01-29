import logging


from network.models import Switch

from django.core.management.base import BaseCommand, CommandError

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    args = ''
    help = 'Does some switch stuffs'

    def handle(self, *args, **options):
        switch = Switch.objects.get(id=1)

        dot1dtpfdbaddress = '1.3.6.1.2.1.17.4.3.1.1'    # MAC address
        dot1dtpfdbport = '1.3.6.1.2.1.17.4.3.1.2'       # Bridge port
        ifindex = '1.3.6.1.2.1.2.2.1.1'                 # Interface index
        ifname = '1.3.6.1.2.1.31.1.1.1.1'               # Interface name

        oid = '1.3.6.1.2.1.17.4.3.1.2.0.31.22.28.76.134'
        mac = '001f.161c.4c86'

        switch.findmac(switch, mac)
