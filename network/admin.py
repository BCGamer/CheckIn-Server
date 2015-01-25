from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from network.forms import VlanForm
from network.models import Switch, UplinkPort
from network.models import Vlan
from django import forms


class SwitchForm(forms.ModelForm):
    class Meta:
        model = Switch
        widgets = {
            'ssh_pass': forms.PasswordInput(render_value=True),
            'snmp_auth_pass': forms.PasswordInput(render_value=True),
            'snmp_priv_pass': forms.PasswordInput(render_value=True),
        }
        fields = ('ssh_pass', 'snmp_auth_pass', 'snmp_priv_pass')


class UplinkPortInline(admin.TabularInline):
    model = UplinkPort
    extra = 1


class SwitchAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'provider', 'ip', 'ssh_port',
                    'switch_vlan_dirty', 'switch_vlan_clean',
                    'enabled',
                    'ports', 'id')
    ordering = ('ip',)

    inlines = (
        UplinkPortInline,
    )

    form = SwitchForm

    fieldsets = (
        (None, {'fields': (('name', 'ip', 'ports', ),
                           ('provider', ),
                           'enabled', )}),
        ('SSH', {'fields': (('ssh_user', 'ssh_pass', 'ssh_port', ),
                            )}),
        ('SNMP', {'fields': (('snmp_username', 'snmp_community', ),
                             ('snmp_auth_pass', 'snmp_auth_type', ),
                             ('snmp_priv_pass', 'snmp_priv_type', ),
                             ('snmp_security', 'snmp_port', ),
                             )}),
        ('VLAN', {'fields': (('switch_vlan_dirty', 'switch_vlan_clean'), )}),
    )

    actions = [
        'override_switch_vlan',
        'override_port_vlan',
    ]

    def override_switch_vlan(self, request, queryset):


        form = None

        if 'apply' in request.POST:
            form = VlanForm(request.POST)

            if form.is_valid():
                vlan = form.cleaned_data['vlan']

                for switch in queryset:
                    switch.change_vlan(vlan.num)

                self.message_user(request, 'Successfully changed switch VLan.')

            return HttpResponseRedirect(request.get_full_path())

        if not form:
            form = VlanForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

        context = {
            'form': form,
        }

        return render(request, 'admin/network/switch/change_switch_vlan.html', context)

    override_switch_vlan.short_description = "Override switch VLan"

    def override_port_vlan(self, request, queryset):
        pass
    override_port_vlan.short_description = "Override port VLan"


class VlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'num', 'type',)

    ordering = ('num',)

admin.site.register(Switch, SwitchAdmin)
admin.site.register(Vlan, VlanAdmin)