from network.providers.base import BaseSwitchBackend
from network.providers import registry

class MikrotikSwitchBackend(BaseSwitchBackend):

    id = 'MikrotikSwitch'
    name = 'Mikrotik Switch'

    def connect(self):
        raise NotImplementedError()

    def disconnect(self):
        raise NotImplementedError()

    def login(self):
        raise NotImplementedError()

    def find_mac_address(self, ip):
        raise NotImplementedError()

    def change_vlan(self, mac_address, vlan_id):
        raise NotImplementedError()

    def show_port(self, mac_address):
        raise NotImplementedError()


registry.register(MikrotikSwitchBackend)