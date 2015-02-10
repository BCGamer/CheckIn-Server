import logging
import re
from network.exceptions import MacNotFound

from network.models import Switch


from django.core.management.base import BaseCommand, CommandError

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = ''
    help = 'Does some switch stuffs'

    def style_output(self, text):
        return '8==> %s' % text

    def handle(self, *args, **options):
        self.stdout.write("testing!", self.style_output)

        # Testing right meow
        # Cisco = 1
        # HP = 2
        switch = Switch.objects.get(id=1)

        switch.connect()
        self.stdout.write("SSH client connected", self.style_output)

        switch.get_shell()
        self.stdout.write("SSH shell connected", self.style_output)

        mac = '001f.161c.4c86'
        try:
            switch.flip_mac_vlan(mac)
        except MacNotFound:
            self.stderr.write("Could not find mac: %s" % mac)

        switch.disconnect()
        self.stdout.write("SSH client disconnected", self.style_output)

        # lines = output.split('\n')
        # logger.info(output1)
