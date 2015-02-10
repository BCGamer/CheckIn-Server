from network.providers.base import BaseSwitchBackend
from network.providers import registry
from network.exceptions import MacNotFound
from netaddr import *
import re
import time


class HPSwitchBackend(BaseSwitchBackend):
    id = 'HPSwitch'
    name = 'HP Switch'

    def ssh_invoke_shell(self):
        # return self._client.invoke_shell()
        self._shell = self._client.invoke_shell()
        # HP has a mandatory welcome screen that must be bypassed
        self.ssh_receive_data()
        self._shell.send("\n")
        self.ssh_receive_data()

    def ssh_find_port(self, mac):
        # Format as 00:00:00:00:00:00
        mac = EUI(mac, dialect=mac_cisco)

        self.ssh_run_command("show mac %s" % mac)
        output = self.ssh_receive_data()
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

    def ssh_change_port_vlan(self, port, vlan):
        self.ssh_run_command("configure")
        self.ssh_receive_data()
        self.ssh_run_command("vlan %s untagged %s" % (vlan, port))
        self.ssh_receive_data()
        self.ssh_run_command("interface %s" % port)
        self.ssh_receive_data()
        self.ssh_run_command("disable")
        self.ssh_receive_data()
        time.sleep(1)
        self.ssh_run_command("enable")
        self.ssh_receive_data()

    def ssh_change_portrange_vlan(self, min_port, max_port, vlan):
        self.ssh_run_command("configure")
        self.ssh_receive_data()
        self.ssh_run_command("vlan %s untagged %s-%s" % (vlan, min_port, max_port))
        self.ssh_receive_data()

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

#registry.register(HPSwitchBackend)