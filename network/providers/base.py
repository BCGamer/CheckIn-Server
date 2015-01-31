import paramiko
import time

from paramiko import SSHClient
from pysnmp.entity.rfc3413.oneliner import cmdgen
from network.exceptions import SwitchNotConnected, Timeout


class BaseSwitchBackend(object):
    connected = False
    switch = None
    _client = None
    _shell = None
    _snmp = cmdgen.CommandGenerator()
    _snmp_user = None
    _snmp_target = None

    def snmp_device(self, switch):
        self.switch = switch

        self._snmp_user = cmdgen.UsmUserData(
            switch.snmp_username,
            switch.snmp_auth_pass,
            switch.snmp_priv_pass,

            authProtocol=tuple(map(int, switch.snmp_auth_type.split(','))),
            privProtocol=tuple(map(int, switch.snmp_priv_type.split(',')))

            # authProtocol=(1,3,6,1,6,3,10,1,1,3),
            # privProtocol=(1,3,6,1,6,3,10,1,2,2)
            # authProtocol=cmdgen.usmHMACSHAAuthProtocol,
            # privProtocol=cmdgen.usmAesCfb128Protocol
        )

        self._snmp_target = cmdgen.UdpTransportTarget(
            (switch.ip, switch.snmp_port)
        )

    def snmp_walk(self, oid):
        error_indication, error_status, error_index, var_binds = self._snmp.nextCmd(
            self._snmp_user, self._snmp_target,
            oid,
            lookupNames=True, lookupValues=True
        )

        output = ()
        if error_indication:
            print(error_indication)
        else:
            if error_status:
                print '%s at %s' % (
                    error_status, error_index
                )
            else:
                for row in var_binds:
                    for name, val in row:
                        output += ((name, val), )

        return output

    def snmp_get(self, oid):
        # output = ()
        error_indication, error_status, error_index, var_binds = self._snmp.getCmd(
            self._snmp_user, self._snmp_target,
            oid,
            lookupNames=True, lookupValues=True
        )

        output = ()
        if error_indication:
            print(error_indication)
        else:
            if error_status:
                print '%s at %s' % (
                    error_status, error_index
                )
            else:
                for name, val in var_binds:
                    output += ((name, val), )

        return output

    def connect(self, switch):
        self.switch = switch

        if not self.is_connected():
            self._client = SSHClient()
            # If SSH client doesn't contain the key the client will fail
            # The following line automatically adds the missing keys as required
            self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._client.connect(hostname=switch.ip, port=switch.port,
                                 username=switch.username, password=switch.password,
                                 look_for_keys=False, allow_agent=False)

    def disconnect(self):
        if self.is_connected():
            self._client.close()
            self._client = None

    def is_connected(self):
        transport = self._client.get_transport() if self._client else None
        return transport and transport.is_active()

    def invoke_shell(self):
        # return self._client.invoke_shell()
        self._shell = self._client.invoke_shell()

    def find_mac_address(self, ip):
        raise NotImplementedError()

    def change_vlan(self, mac_address, vlan_id):
        raise NotImplementedError()

    def run_command(self, command):
        if not self.is_connected():
            raise SwitchNotConnected("Switch is not connected!")

        command = str(command)

        self._shell.send("%s\n" % command)

    def receive_data(self):
        output = ""
        more_data = True

        while more_data is True:
            '''
            timer_check = 0
            # Wait for the data to arrive
            while not self._shell.recv_ready():
                # Sleep for 50 milliseconds
                time.sleep(0.050)
                timer_check += 1
                # Wait for a maximum of 2 seconds
                if timer_check >= 40:
                    raise Timeout("Data buffer timed out")

            # Wait for client to finish with data (IMPORTANT!)
            time.sleep(0.050)

            output = output + self._shell.recv(1024)


            # Check 5 times to make sure there's no more data
            # Continue looping if there is more data to receive
            for _ in range(5):
                time.sleep(0.050)
                if not self._shell.recv_ready():
                    more_data = False
            '''
            for _ in range(40):
                time.sleep(0.050)
                if self._shell.recv_ready():
                    # Wait for client to finish with data (IMPORTANT!)
                    time.sleep(0.050)
                    output = output + self._shell.recv(1024)
                else:
                    more_data = False

        return output

    '''
    # Removed, not necessary
    def get_interactive_shell(self):
        print(repr(self._client.get_transport()))
        print('*** Here we go!\n')

        chan = self._client.invoke_shell()
        interactive.interactive_shell(chan)
        chan.close()
    '''