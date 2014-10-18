from django.contrib import admin
from networkcontrol.models import Switch


class SwitchAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider')

admin.site.register(Switch, SwitchAdmin)