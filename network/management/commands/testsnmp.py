import logging

from network.models import Switch

from django.core.management.base import BaseCommand, CommandError

from pysnmp.entity.rfc3413.oneliner import cmdgen

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = ''
    help = 'Does some switch stuffs'

    def handle(self, *args, **options):

        for switch in Switch.objects.filter(enabled=True):
            self.stdout.write("Testing switch %s : %s" % (switch.id, switch.name))

            switch.get_provider().snmp_device(switch)


            try:
                switch.get_provider().snmp_get('1.3.6.1.2.1.17.4.3.1.1')
                self.stdout.write("Switch %s ok" % switch.name)

            except Exception, e:
                self.stderr.write("error with switch %s: %s" % (switch.name, e))
