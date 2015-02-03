from network.providers.hp.provider import HPSwitchBackend
from network.providers import registry

from pysnmp.entity.rfc3413.oneliner import cmdgen

class HPProcurve2524(HPSwitchBackend):
    # Unsupported model
    # 02/02/2015 - Chris
    # Only supports SSH1.5, implementing fix would require
    # effort be put into SNMP SET command.

    id = 'HP_Procurve_2524'
    name = 'HP Procurve 2524'

    def snmp_device(self, switch):
        self.switch = switch

        self._snmp_user = cmdgen.CommunityData(switch.snmp_community)

        self._snmp_target = cmdgen.UdpTransportTarget(
            (switch.ip, switch.snmp_port)
        )

    # SNMPv2-SMI::mib-2.17.7.1.4.5.1.1.30 u 51
    # 1.3.6.1.4.1.9.2.17.7.1.4.5.1.1.30
    def snmp_change_vlan(self, port, vlan):
        test = self.snmp_set('1.3.6.1.4.1.9.2.17.7.1.4.5.1.1.20', 70)
        print cmdgen.MibVariable('SNMPv2-MIB')
        pass

    def snmp_set(self, property_oid, property_val):
        print cmdgen.MibVariable('SNMPv2-MIB').getOid()
        error_indication, error_status, error_index, var_binds = self._snmp.setCmd(
            self._snmp_user, self._snmp_target,
            (cmdgen.MibVariable('SNMPv2-MIB', 'property_oid'), property_val)
        )

        print var_binds
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

    # Can't use SSH so just bypass these steps
    def ssh_connect(self, switch):
        print cmdgen.MibVariable('SNMPv2-MIB')
        test = self.snmp_set('1.3.6.1.4.1.9.2.17.7.1.4.5.1.1.20', 70)
        print test
        pass

    def ssh_disconnect(self):
        pass

    def ssh_is_connected(self):
        pass

    def ssh_invoke_shell(self):
        pass

    def ssh_receive_data(self):
        pass

    def ssh_change_vlan(self, port, vlan):
        self.snmp_change_vlan(port, vlan)
        pass




#registry.register(HPProcurve2524)