from django.db import models
from network.exceptions import MacNotFound
from network.providers import registry


class SwitchManager(models.Manager):

    def flip_vlan(self, mac, vlan_number=None):

        found_mac = False
        enabled_switches = super(SwitchManager, self).get_queryset().filter(enabled=True)

        for switch in enabled_switches:
            try:
                switch.flip_vlan(mac, vlan_number)
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

    name = models.CharField(max_length=50)
    ip = models.GenericIPAddressField()
    port = models.IntegerField(default=22)

    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    switch_vlan_dirty = models.ForeignKey('network.VLAN', verbose_name='Dirty',
                                          blank='true', null='true',
                                          related_name='switch_vlan_dirty',
                                          limit_choices_to={'vlan_type': 'DI'})

    switch_vlan_clean = models.ForeignKey('network.VLAN', verbose_name='Clean',
                                          blank='true', null='true',
                                          related_name='switch_vlan_clean',
                                          limit_choices_to={'vlan_type': 'CL'},)

    ports = models.IntegerField(default=24, verbose_name='# of Ports')

    requires_authentication = models.BooleanField(default=True)

    provider = models.CharField(max_length=30, choices=registry.as_choices(), verbose_name='Type')

    enabled = models.BooleanField(default=False)

    objects = SwitchManager()

    _provider_cache = None

    class Meta:
        verbose_name_plural = 'Switches'

    def __unicode__(self):
        return '{0} ({1})'.format(self.name, self.ip)

    def get_provider(self):
        if not self._provider_cache:
            return registry.by_id(self.provider)
        return self._provider_cache

    def connect(self):
        provider = self.get_provider()
        provider.connect(self)
    '''
    def get_shell(self):
        provider = self.get_provider()
        provider.get_interactive_shell()
    '''
    def get_shell(self):
        provider = self.get_provider()
        provider.invoke_shell()
        # Clean the initial data buffer
        provider.receive_data()

    def run_cmd(self, cmd):
        provider = self.get_provider()
        provider.run_command(cmd)
        output = provider.receive_data()
        return output

    def set_vlan(self, vlan_number):
        pass

    def set_port_vlan(self, vlan_number):
        ports = self.uplink_ports.values_list('port', flat=True)

    def flip_vlan(self, mac, vlan_number=None):

        if not vlan_number:
            vlan_number = self.switch_vlan_clean.vlan_num

        self.connect()

        try:

            self.get_shell()

            port = self.get_provider().find_mac_address(mac)
            self.get_provider().change_vlan(port, vlan_number)

        except MacNotFound, e:
            self.disconnect()
            raise MacNotFound()

        except Exception, e:
            pass

        finally:
            self.disconnect()

    '''
    def get_channel(self):
        self.connect()
        provider = self.get_provider()
        chan = provider.invoke_shell()

        return chan
    '''
    def disconnect(self):
        provider = self.get_provider()
        provider.disconnect()


class VLAN(models.Model):
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

    vlan_name = models.CharField(max_length=50, verbose_name='Name')
    vlan_num = models.IntegerField(verbose_name='VLAN #')
    vlan_type = models.CharField(max_length=2, verbose_name='Type',
                                 choices=TYPES_OF_VLANS, default=NONE)
    vlan_desc = models.TextField(verbose_name='Description',
                                 null='true', blank='true')

    def __unicode__(self):
        return '{0}'.format(self.vlan_name)