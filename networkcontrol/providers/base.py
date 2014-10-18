import paramiko
import interactive

from paramiko import SSHClient


class BaseSwitchBackend(object):

    connected = False

    switch = None

    _client = None

    def connect(self, switch):
        self.switch = switch

        if not self.is_connected():
            self._client = SSHClient()
            self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._client.connect(hostname=switch.ip, port=switch.port, username=switch.username, password=switch.password)

    def disconnect(self):
        if self.is_connected():
            self._client.close()
            self._client = None

    def is_connected(self):
        transport = self._client.get_transport() if self._client else None
        return transport and transport.is_active()

    def get_interactive_shell(self):
        print(repr(self._client.get_transport()))
        print('*** Here we go!\n')

        chan = self._client.invoke_shell()
        interactive.interactive_shell(chan)
        chan.close()

    def invoke_shell(self):
        return self._client.invoke_shell()

    def find_mac_address(self, ip):
        raise NotImplementedError()

    def change_vlan(self, mac_address, vlan_id):
        raise NotImplementedError()