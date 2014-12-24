import logging

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


        switch = Switch.objects.get(id=1)

        switch.connect()

        output = switch.run_cmd("show vlan")

        # lines = output.split('\n')

        logger.info(output)





