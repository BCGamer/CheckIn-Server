from django.db import models
from network.providers import registry


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

    def flip_vlan(self, mac):
        # Need to deal with failure still
        provider = self.get_provider()
        port = provider.find_mac_address(mac)
        provider.change_vlan(port, self.switch_vlan_clean.vlan_num)

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