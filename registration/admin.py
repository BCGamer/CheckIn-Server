from django.contrib import admin
from django.utils.translation import ugettext as _
from registration.models import RegisteredUser, ResponseCode
from django.contrib.auth.admin import UserAdmin


class RegisteredUserAdmin(UserAdmin):
    list_display = ('username',
                    'last_name',
                    'first_name',
                    'ip_address',
                    'has_av',
                    'has_fw',
                    'has_dhcp',
                    'has_waiver',
                    'gottacon_id')

    list_filter = ('dhcp_enabled',
                   'has_firewall',
                   'has_antivirus',
                   'waiver_signed')

    search_fields = ('first_name',
                     'last_name',
                     'gottacon_id',
                     'ip_address')

    readonly_fields = ('uuid',)

    fieldsets = (
        (None, {'fields': ('email',
                           'username',
                           'gottacon_id',
                           'uuid',
                           'password',)}),
        (_('Personal info'), {'fields': ('first_name',
                                         'last_name',
                                         #'email',
                                         'nickname')}),
        (_('PC Info'), {'fields': ('ip_address', 'mac')}),
        (_('Waiver'), {'fields': ('age_under_18',
                                  'waiver_signed',
                                  'guardian_name',
                                  'guardian_phone',)}),
        (_('Gottacon Requirements'), {'fields': ('verification_received',
                                                 'has_antivirus',
                                                 'has_firewall',
                                                 'dhcp_enabled',
                                                 'reg_errors',)}),
        (_('Important dates'), {'fields': ('last_login',
                                           'date_joined')}),
        (_('Permissions'), {'fields': ('is_active',
                                       'is_staff',
                                       'is_superuser',
                                       'groups',
                                       'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}),
    )

    def has_av(self, obj):
        return obj.has_antivirus
    has_av.short_description = 'AV'

    def has_fw(self, obj):
        return obj.has_firewall
    has_fw.short_description = 'FW'

    def has_dhcp(self, obj):
        return obj.dhcp_enabled
    has_dhcp.short_description = 'DHCP'

    def has_waiver(self, obj):
        return obj.waiver_signed
    has_waiver.short_description = 'Waiver'


class ResponseCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'good_to_go',)
    list_filter = ('good_to_go', )


admin.site.register(RegisteredUser, RegisteredUserAdmin)
admin.site.register(ResponseCode, ResponseCodeAdmin)