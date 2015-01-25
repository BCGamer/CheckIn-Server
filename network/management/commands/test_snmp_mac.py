import logging
import re
from network.exceptions import MacNotFound


from network.models import Switch


from django.core.management.base import BaseCommand, CommandError

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    args = ''
    help = 'Does some switch stuffs'

    def handle(self, *args, **options):
        self.stdout.write("testing!", self.style_output)

        switch = Switch.objects.get(id=1)

