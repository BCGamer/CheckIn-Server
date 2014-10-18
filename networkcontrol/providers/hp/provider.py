from networkcontrol.providers.base import BaseSwitchBackend
from networkcontrol.providers import registry


class HPSwitchBackend(BaseSwitchBackend):

    id = 'HPSwitch'
    name = 'HP Switch'

    def run_command(self, command):
        stdin, stdout, stderr = self._client.exec_command(command)
        print(stdout)

    def find_mac_address(self, ip):
        raise NotImplementedError()

    def change_vlan(self, mac_address, vlan_id):
        raise NotImplementedError()

    def show_port(self, mac_address):
        raise NotImplementedError()


registry.register(HPSwitchBackend)