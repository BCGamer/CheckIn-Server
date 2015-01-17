from django.contrib import admin
from network.models import Switch
from network.models import VLAN
from django import forms


class SwitchForm(forms.ModelForm):
    class Meta:
        model = Switch
        widgets = {
            'password': forms.PasswordInput(render_value=True),

        }
        fields = ('password',)


class SwitchAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'provider', 'ip', 'port',
                    'switch_vlan_dirty', 'switch_vlan_clean',
                    'enabled',
                    'ports', 'id')
    ordering = ('ip',)
    form = SwitchForm

    fieldsets = (
        (None, {'fields': ('name', 'provider', 'enabled', 'ports')}),
        ('Connectivity', {'fields': ('ip', 'port')}),
        ('Authentication', {'fields': ('username', 'password')}),
        ('VLAN', {'fields': ('switch_vlan_dirty', 'switch_vlan_clean')}),
    )


class VLANAdmin(admin.ModelAdmin):
    list_display = ('vlan_name', 'vlan_num', 'vlan_type',)

    ordering = ('vlan_num',)

admin.site.register(Switch, SwitchAdmin)
admin.site.register(VLAN, VLANAdmin)