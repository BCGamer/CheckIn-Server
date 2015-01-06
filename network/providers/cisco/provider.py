from network.providers.base import BaseSwitchBackend
from network.providers import registry
from netaddr import *
import re
import time


class CiscoSwitchBackend(BaseSwitchBackend):

    id = 'CiscoSwitch'
    name = 'Cisco Switch'

    def find_mac_address(self, mac):
        # Format as 00:00:00:00:00:00
        mac = EUI(mac, dialect=mac_unix)

        self.run_command("show mac-address-table address %s" % mac)
        output = self.receive_data()
        port = re.findall(r'Fa0/\d+', output)

        if len(port) == 1:
            return port[0]
        else:
            # There is a problem
            raise NotImplementedError()

    def change_vlan(self, port, vlan):
        self.run_command("configure terminal")
        self.run_command("interface %s" % port)
        self.run_command("switchport access vlan %s" % vlan)
        self.run_command("shutdown")
        time.sleep(1)
        self.run_command("no shutdown")
        self.receive_data()

    def override_switch_vlan(self, ports, vlan):
        raise NotImplementedError()

'''
    def show_port(self, mac_address):
        raise NotImplementedError()
'''

registry.register(CiscoSwitchBackend)