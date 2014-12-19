from django.contrib import admin
from networkcontrol.models import Switch


class SwitchAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider', 'ip', 'port')

#ip, port

admin.site.register(Switch, SwitchAdmin)