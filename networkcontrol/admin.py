from django.contrib import admin
from networkcontrol.models import Switch


class SwitchAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')

admin.site.register(Switch, SwitchAdmin)