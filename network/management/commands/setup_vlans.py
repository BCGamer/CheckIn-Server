import logging
import re
from network.exceptions import MacNotFound

from network.models import Switch, Vlan

from django.core.management.base import BaseCommand, CommandError

logger = logging.getLogger(__name__)


VLANS = [
    {
        'name': 'asdf',
        'num': 20,
        'type': Vlan.CLEAN,
        'desc': 'A clean vlan!'
    },
    {
        'name': 'asdf',
        'num': 30,
        'type': Vlan.CLEAN,
        'desc': 'A clean vlan!'
    },
    {
        'name': 'asdf',
        'num': 40,
        'type': Vlan.CLEAN,
        'desc': 'A clean vlan!'
    },
    {
        'name': 'asdf',
        'num': 50,
        'type': Vlan.DIRTY,
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