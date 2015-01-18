from network.providers.base import BaseSwitchBackend
from network.providers import registry
from network.exceptions import MacNotFound
from netaddr import *
import re
import time


class HPSwitchBackend(BaseSwitchBackend):
    id = 'HPSwitch'
    name = 'HP Switch'

    def invoke_shell(self):
        # return self._client.invoke_shell()
        self._shell = self._client.invoke_shell()
        # HP has a mandatory welcome screen that must be bypassed
        self.receive_data()
        self._shell.send("\n")
        self.receive_data()

    def find_mac_address(self, mac):
        # Format as 00:00:00:00:00:00
        mac = EUI(mac, dialect=mac_cisco)

        self.run_command("show mac %s" % mac)
        output = self.receive_data()
        output = self.remove_garbage(output)
        port = re.findall(r'Located on Port : (\d+)', output)

        if len(port) == 1:
            if int(port[0]) < int(self.switch.ports):
                return port[0]
            else:
                # There is a problem
                raise MacNotFound()
        else:
            # There is a problem
            raise MacNotFound()

    def change_vlan(self, port, vlan):
        self.run_command("configure")
        self.receive_data()
        self.run_command("vlan %s untagged %s" % (vlan, port))
        self.receive_data()
        self.run_command("interface %s" % port)
        self.receive_data()
        self.run_command("disable")
        self.receive_data()
        time.sleep(1)
        self.run_command("enable")
        self.receive_data()


    def show_port(self, mac_address):
        raise NotImplementedError()

    @staticmethod
    def remove_garbage(message):
        hp_re1 = re.compile(r'(\[\d+[HKJ])|(\[\?\d+[hl])|(\[\d+)|(\;\d+\w?)')
        hp_re2 = re.compile(r'([E]\b)')
        hp_re3 = re.compile(ur'[\u001B]+')

        message = hp_re1.sub("", message)
        message = hp_re2.sub("", message)
        message = hp_re3.sub("", message)

        return message

registry.register(HPSwitchBackend)