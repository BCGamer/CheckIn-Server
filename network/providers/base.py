import paramiko
import time

from paramiko import SSHClient
from pysnmp.entity.rfc3413.oneliner import cmdgen
from netaddr import *

from network.exceptions import SwitchNotConnected
from network.exceptions import MacNotFound
from network.exceptions import Timeout


class BaseSwitchBackend(object):
    connected = False
    switch = None
    _client = None
    _shell = None
    _snmp = None
    _snmp_user = None
    _snmp_target = None

    def snmp_device(self, switch):
        self._snmp = cmdgen.CommandGenerator()

        self.switch = switch

        self._snmp_user = cmdgen.UsmUserData(
            switch.snmp_username,
            switch.snmp_auth_pass,
            switch.snmp_priv_pass,
            authProtocol=tuple(map(int, switch.snmp_auth_type.split(','))),
            privProtocol=tuple(map(int, switch.snmp_priv_type.split(',')))
        )
        # print self._snmp_user

        self._snmp_target = cmdgen.UdpTransportTarget(
            (switch.ip, switch.snmp_port)
        )
        # print self._snmp_target

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

    def snmp_find_port(self, mac):
        matched_macs = ()
        dot1dtpfdbaddress = '1.3.6.1.2.1.17.4.3.1.1'
        device_macs = self.snmp_walk(dot1dtpfdbaddress)

        for val in device_macs:
            # Convert pysnmp crap returns to proper strings
            val_oid = str(val[0])
            val_mac = str(val[1].prettyPrint())[2:]

            # Does this mac address match the one we're looking for?
            if EUI(val_mac, dialect=mac_cisco) == EUI(mac, dialect=mac_cisco):
                matched_macs += (val_oid.replace('1.3.6.1.2.1.17.4.3.1.1.', ''), )

        if matched_macs == ():
            # Nothing found
            raise MacNotFound()

        # We found match(es), find bridge port(s)
        # This can have multiple results, loop through them
        for oid in matched_macs:
            dot1dtpfdbport = '1.3.6.1.2.1.17.4.3.1.2.' + str(oid)
            bridge = self.snmp_get(dot1dtpfdbport)

            if bridge == ():
                break

            # We found a bridge, find interface index - 1 result
            ifindex = '1.3.6.1.2.1.2.2.1.1.' + str(bridge[0][1])
            interface = self.snmp_get(ifindex)

            if interface == ():
                break

            # We found an interface, find if valid - 1 result
            # If valid, find interface name
            # Pre-set 'name' in case we need it to fail properly
            name = ()
            if interface[0][1] < self.switch.ports and interface[0][1] not in (self.switch.uplink_ports.values_list('port')):
                ifname = '1.3.6.1.2.1.31.1.1.1.1.' + str(interface[0][1])
                name = self.snmp_get(ifname)

            if name == ():
                break

            # We found the interface name, return it
            return name[0][1]

        # Nothing valid found
        raise MacNotFound()

    def ssh_connect(self, switch):
        self.switch = switch

        if not self.ssh_is_connected():
            self._client = SSHClient()
            # If SSH client doesn't contain the key the client will fail
            # The following line automatically adds the missing keys as required
            self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._client.connect(hostname=switch.ip, port=switch.ssh_port,
                                 username=switch.ssh_user, password=switch.ssh_pass,
                                 look_for_keys=False, allow_agent=False)

    def ssh_disconnect(self):
        if self.ssh_is_connected():
            self._client.close()
            self._client = None

    def ssh_is_connected(self):
        transport = self._client.get_transport() if self._client else None
        return transport and transport.is_active()

    def ssh_invoke_shell(self):
        # return self._client.invoke_shell()
        self._shell = self._client.invoke_shell()

    def ssh_find_port(self, ip):
        # Different based on make (and model)
        raise NotImplementedError()

    def ssh_change_vlan(self, mac_address, vlan_id):
        raise NotImplementedError()

    def ssh_run_command(self, command):
        if not self.ssh_is_connected():
            raise SwitchNotConnected("Switch is not connected!")

        command = str(command)

        self._shell.send("%s\n" % command)

    def ssh_receive_data(self):
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
