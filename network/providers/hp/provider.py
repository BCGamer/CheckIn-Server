import logging
import telnetlib


from network.providers.base import BaseSwitchBackend
from network.providers import registry
from network.exceptions import SwitchNotConnected

logger = logging.getLogger(__name__)


class HPSwitchBackend(BaseSwitchBackend):

    id = 'HPSwitch'
    name = 'HP Switch'
    conn = None

    def connect(self, switch):
        """
        Need to get get past silly HP intro screens and enter password on connection.
        Will end up with a cursor ready to accept commands.
        """
        if not self.conn:
            conn = telnetlib.Telnet(switch.ip)

            conn.read_until("Press any key to continue")
            conn.write("\n")

            conn.read_until("Password: ")

            conn.write("%s\n" % switch.password.encode('ascii'))
            output = conn.read_until("# ", 2)

            logger.info("Connected to switch %s at %s" % (switch.name, switch.ip))

            self.conn = conn

        return self.conn

    def run_command(self, command):

        if not self.conn:
            raise SwitchNotConnected("Switch is not connected!")

        command = str(command)

        self.conn.write("%s\n" % command)

        output = self.conn.read_until("# ")

        return output

    def find_mac_address(self, ip):
        raise NotImplementedError()

    def change_vlan(self, mac_address, vlan_id):
        raise NotImplementedError()

    def show_port(self, mac_address):
        raise NotImplementedError()


registry.register(HPSwitchBackend)