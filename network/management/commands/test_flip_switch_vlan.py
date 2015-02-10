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

        # Testing right meow
        # Cisco = 1
        # HP = 2
        switch = Switch.objects.get(id=2)

        switch.flip_switch_vlan(50)
