from django.db import models
from networkcontrol.providers import registry


class Switch(models.Model):

    name = models.CharField(max_length=50)
    ip = models.GenericIPAddressField()
    port = models.IntegerField(default=22)

    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    vlan1 = models.IntegerField(default=70, verbose_name='Dirty')
    vlan2 = models.IntegerField(default=50, verbose_name='Clean')

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

    def get_shell(self):
        provider = self.get_provider()
        provider.get_interactive_shell()

    def run_cmd(self, cmd):
        provider = self.get_provider()
        output = provider.run_command(cmd)
        return output

    def get_channel(self):
        self.connect()
        provider = self.get_provider()
        chan = provider.invoke_shell()

        return chan

    def disconnect(self):
        provider = self.get_provider()
        provider.disconnect()