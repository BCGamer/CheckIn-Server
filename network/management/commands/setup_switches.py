import logging
import re
from network.exceptions import MacNotFound

from network.models import Switch, Vlan

from django.core.management.base import BaseCommand, CommandError

logger = logging.getLogger(__name__)


VLANS = [
    {
        'name': 'SERVERS / BCG PCs',
        'num': 10,
        'type': Vlan.NONE,
        'desc': 'A clean vlan!'
    },
    {
        'name': 'SWITCHES / NETWORK GEAR',
        'num': 11,
        'type': Vlan.NONE,
        'desc': 'A clean vlan!'
    },
    {
        'name': 'GOTTACON ADMIN',
        'num': 30,
        'type': Vlan.CLEAN,
        'desc': 'A clean vlan!'
    },
    {
        'name': 'DIRTY / PRECHECK',
        'num': 50,
        'type': Vlan.DIRTY,
        'desc': 'A dirty vlan!'
    },
    {
        'name': 'LAN FLOOR',
        'num': 70,
        'type': Vlan.CLEAN,
        'desc': 'A clean vlan!'
    },
    {
        'name': 'VENDOR',
        'num': 90,
        'type': Vlan.CLEAN,
        'desc': 'A clean vlan!'
    },
    {
        'name': 'TOURNAMENT PCs',
        'num': 110,
        'type': Vlan.CLEAN,
        'desc': 'A clean vlan!'
    },
    {
        'name': 'CASTERS',
        'num': 150,
        'type': Vlan.CLEAN,
        'desc': 'A clean vlan!'
    },
]


class Command(BaseCommand):
    args = ''
    help = 'Does some switch stuffs'

    def style_output(self, text):
        return '8==> %s' % text

    def handle(self, *args, **options):

        for vlan in VLANS:

            try:
                existing_vlan = Vlan.objects.get(num=vlan['num'])
                existing_vlan.name = vlan['name']
                existing_vlan.type = vlan['type']
                existing_vlan.desc = vlan['desc']
                existing_vlan.save()

            except Vlan.DoesNotExist:
                Vlan.objects.create(**vlan)