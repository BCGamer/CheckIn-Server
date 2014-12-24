from django.contrib import admin
from network.models import Switch
from django import forms


class switchForm(forms.ModelForm):
    class Meta:
        model = Switch
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }
        fields = ('password',)


class SwitchAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'provider',
                    'ip',
                    'port',
                    'vlan1',
                    'vlan2',
                    'enabled',
                    'ports')
    ordering = ('ip',)
    form = switchForm

    fieldsets = (
        (None, {'fields': ('name', 'provider', 'enabled', 'ports')}),
        ('Connectivity', {'fields': ('ip', 'port')}),
        ('Authentication', {'fields': ('username', 'password')}),
        ('VLAN', {'fields': ('vlan1', 'vlan2')}),
    )


admin.site.register(Switch, SwitchAdmin)