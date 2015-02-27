import logging

from django.db import models
from network.exceptions import MacNotFound
from network.providers import registry
from netaddr import *

from network.exceptions import TooManyUplinks

logger = logging.getLogger(__name__)


class SwitchManager(models.Manager):

    def flip_vlan(self, mac, vlan_number=None):

        logger.info("Flipping Vlan for mac %s to %s" % (mac, vlan_number))

        found_mac = False
        enabled_switches = super(SwitchManager, self).get_queryset().filter(enabled=True)

        for switch in enabled_switches:

            try:
                logger.info("Trying switch %s" % switch)
                switch.flip_mac_vlan(mac, vlan_number)

            except MacNotFound, e:
                continue

            found_mac = True

        return found_mac


class UplinkPort(models.Model):
    port = models.IntegerField()
    switch = models.ForeignKey('network.Switch', related_name='uplink_ports')

    class Meta:
        unique_together = (
            ('port', 'switch'),
        )

    def __unicode__(self):
        return '%s' % self.port


class Switch(models.Model):

    # Types of SNMP Authentication
    SNMP_AUTH_NONE = '1,3,6,1,6,3,10,1,1,1'       # usmNoAuthProtocol
    SNMP_AUTH_MD5 = '1,3,6,1,6,3,10,1,1,2'        # usmHMACMD5AuthProtocol
    SNMP_AUTH_SHA = '1,3,6,1,6,3,10,1,1,3'        # usmHMACSHAAuthProtocol
    TYPES_OF_SNMP_AUTHENTICATION = (
        (SNMP_AUTH_MD5, 'MD5'),
        (SNMP_AUTH_SHA, 'SHA'),
        (SNMP_AUTH_NONE, 'NONE'),
    )

    # Types of SNMP Privacy
    SNMP_PRIV_DES = '1,3,6,1,6,3,10,1,2,2'        # usmDESPrivProtocol
    SNMP_PRIV_AES128 = '1,3,6,1,6,3,10,1,2,4'     # usmAesCfb128Protocol
    SNMP_PRIV_3DES = '1,3,6,1,6,3,10,1,2,3'       # usm3DESEDEPrivProtocol
    SNMP_PRIV_AES192 = '1,3,6,1,4,1,9,12,6,1,1'   # usmAesCfb192Protocol
    SNMP_PRIV_AES256 = '1,3,6,1,4,1,9,12,6,1,2'   # usmAesCfb256Protocol
    SNMP_PRIV_NONE = '1,3,6,1,4,1,9,12,6,12'     # usmAesCfb256Protocol
    TYPES_OF_SNMP_PRIVACY = (
        (SNMP_PRIV_NONE, 'NONE'),
        (SNMP_PRIV_DES, 'DES'),
        (SNMP_PRIV_3DES, '3DES'),
        (SNMP_PRIV_AES128, 'AES128'),
        (SNMP_PRIV_AES192, 'AES192'),
        (SNMP_PRIV_AES256, 'AES256'),
    )

    # Types of SNMP Security Level
    SNMP_SEC_NONE = 'noAuthNoPriv'
    SNMP_SEC_AUTH_NOPRIV = 'authNoPriv'
    SNMP_SEC_AUTH_PRIV = 'AuthPriv'
    TYPES_OF_SNMP_SECURITY = (
        (SNMP_SEC_NONE, 'No Auth & No Priv'),
        (SNMP_SEC_AUTH_NOPRIV, 'Auth & No Priv'),
        (SNMP_SEC_AUTH_PRIV, 'Auth & Priv'),
    )

    name = models.CharField(max_length=50)
    ip = models.GenericIPAddressField(verbose_name='IP Address')

    ssh_port = models.IntegerField(default=22, verbose_name='Port', blank='true', null='true')
    ssh_user = models.CharField(max_length=50, verbose_name='Username', blank='true', null='true')
    ssh_pass = models.CharField(max_length=50, verbose_name='Password', blank='true', null='true')

    snmp_port = models.IntegerField(default=161, verbose_name='Port', blank='true', null='true')
    snmp_auth_pass = models.CharField(max_length=50, verbose_name='Authentication Password', blank='true', null='true')
    snmp_priv_pass = models.CharField(max_length=50, verbose_name='Privacy Password', blank='true', null='true')
    snmp_community = models.CharField(max_length=50, verbose_name='Community', blank='true', null='true')
    snmp_username = models.CharField(max_length=50, verbose_name='Username', blank='true', null='true')
    snmp_auth_type = models.CharField(max_length=50, verbose_name='Authentication Type', choices=TYPES_OF_SNMP_AUTHENTICATION, default=SNMP_AUTH_NONE)
    snmp_priv_type = models.CharField(max_length=50, verbose_name='Privacy Type', choices=TYPES_OF_SNMP_PRIVACY, default=SNMP_PRIV_NONE)
    snmp_security = models.CharField(max_length=50, verbose_name='Security Type', choices=TYPES_OF_SNMP_SECURITY, default=SNMP_SEC_NONE)

    switch_vlan_dirty = models.ForeignKey('network.Vlan', verbose_name='Dirty',
                                          blank='true', null='true',
                                          related_name='switch_vlan_dirty',
                                          limit_choices_to={'type': 'DI'})

    switch_vlan_clean = models.ForeignKey('network.Vlan', verbose_name='Clean',
                                          blank='true', null='true',
                                          related_name='switch_vlan_clean',
                                          limit_choices_to={'type': 'CL'},)

    ports = models.IntegerField(default=24, verbose_name='# of Ports')

    requires_authentication = models.BooleanField(default=True)

    provider = models.CharField(max_length=30, choices=registry.as_choices(), verbose_name='Model')

    enabled = models.BooleanField(default=False)

    objects = SwitchManager()

    _provider_cache = None

    class Meta:
        verbose_name_plural = 'Switches'

    def __unicode__(self):
        return '{0} ({1})'.format(self.id, self.name)

    def get_provider(self):
        if not self._provider_cache:
            return registry.by_id(self.provider)
        return self._provider_cache

    '''
    def snmp_find_port(self, mac):
        provider = self.get_provider()
        provider.snmp_device(self)
        return provider.snmp_find_port(mac)
    '''

    def connect(self):
        provider = self.get_provider()
        provider.ssh_connect(self)

    def get_shell(self):
        provider = self.get_provider()
        provider.ssh_invoke_shell()
        # Clean the initial data buffer
        provider.ssh_receive_data()

    def run_cmd(self, cmd, response=True):
        provider = self.get_provider()
        provider.ssh_run_command(cmd)
        if response:
            # Wait for SSH buffer to return data
            output = provider.ssh_receive_data()
            return output
        else:
            # Don't wait for SSH buffer to return data
            return None

    def set_vlan(self, vlan_number):
        pass

    def set_port_vlan(self, vlan_number):
        ports = self.uplink_ports.values_list('port', flat=True)

    def flip_mac_vlan(self, mac, vlan_number=None):
        if not vlan_number:
            logger.info("No vlan specified, using %s" % self.switch_vlan_clean.num)
            vlan_number = self.switch_vlan_clean.num

        provider = self.get_provider()

        logger.info("Getting snmp device")
        provider.snmp_device(self)
        logger.info("Got snmp device")

        try:
            logger.info("Attempting to find port for mac")
            port = provider.snmp_find_port(mac)
            logger.info("Got port %s" % port)
            self.connect()
            self.get_shell()
            logger.info("Found mac, changing port vlan")
            provider.ssh_change_port_vlan(port, vlan_number)

        except MacNotFound, e:
            self.disconnect()
            logger.warn("Mac not found in switch %s" % self)
            raise MacNotFound()

        except Exception, e:
            logger.error(e)
            pass

        finally:
            # Squelch the stupid SNMP cmd generator
            # If this isn't done 1 error is generated for
            # each switch object
            provider._snmp = None
            self.disconnect()

    def flip_port_vlan(self, port, vlan_number=None):
        if not vlan_number:
            vlan_number = self.switch_vlan_clean.num

        provider = self.get_provider()
        provider.snmp_device(self)

        try:
            self.connect()
            self.get_shell()
            provider.ssh_change_port_vlan(port, vlan_number)

        except Exception, e:
            print e
            pass

        finally:
            provider._snmp = None
            self.disconnect()

    def get_port_ranges(self):
        uplink_ports = self.uplink_ports.values_list('port', flat=True)
        ranges = []

        if len(uplink_ports) > 2:
            raise TooManyUplinks

        if len(uplink_ports) == 1:
            ranges.append(range(1, uplink_ports[0]))
            ranges.append(range(uplink_ports[0]+1, self.ports+1))
        elif len(uplink_ports) == 2:
            ranges.append(range(1, min(uplink_ports)))
            ranges.append(range(min(uplink_ports)+1, (max(uplink_ports))))

            if(max(uplink_ports) < self.ports):
                ranges.append(range(max(uplink_ports)+1, self.ports+1))

        return ranges

    def flip_switch_vlan(self, vlan_number=None):
        if not vlan_number:
            vlan_number = self.switch_vlan_clean.num

        provider = self.get_provider()
        provider.snmp_device(self)

        ranges = self.get_port_ranges()

        try:
            self.connect()
            self.get_shell()

            for range in ranges:
                if range:
                    if len(range) > 1:
                        provider.ssh_change_portrange_vlan(min(range), max(range), vlan_number)
                    else:
                        provider.ssh_change_port_vlan(str(range))
        except Exception, e:
            print e
            pass
        finally:
            provider._snmp = None
            self.disconnect()

    def disconnect(self):
        provider = self.get_provider()
        provider.ssh_disconnect()


class Vlan(models.Model):
    # Types of VLANs
    DIRTY = 'DI'
    CLEAN = 'CL'
    NONE = 'NO'

    PUBLIC_VLANS = (
        DIRTY,
        CLEAN,
    )

    TYPES_OF_VLANS = (
        (DIRTY, 'Dirty'),
        (CLEAN, 'Clean'),
        (NONE, 'None'),
    )

    name = models.CharField(max_length=50, verbose_name='Name')
    num = models.IntegerField(verbose_name='VLAN #')
    type = models.CharField(max_length=2, verbose_name='Type', choices=TYPES_OF_VLANS, default=NONE)
    desc = models.TextField(verbose_name='Description', null='true', blank='true')

    class Meta:
        verbose_name = 'VLAN'
        verbose_name_plural = 'VLANs'

    def __unicode__(self):
        return '{0}'.format(self.name)