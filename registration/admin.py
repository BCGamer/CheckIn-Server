from django.contrib import admin
from django.utils.translation import ugettext as _
from registration.models import RegisteredUser, ResponseCode
from django.contrib.auth.admin import UserAdmin

class RegisteredUserAdmin(UserAdmin):


    list_display = ('gottacon_id', 'last_name', 'first_name', 'ip_address', 'has_antivirus', 'has_firewall', 'dhcp_enabled', 'uuid')
    list_filter = ('dhcp_enabled', 'has_firewall', 'has_antivirus',)

    search_fields = ('first_name', 'last_name', 'gottacon_id', 'ip_address', 'uuid')


    readonly_fields = ('uuid',)

    fieldsets = (
        (None, {'fields': ('username', 'password', 'gottacon_id', 'uuid')}),
        (_('Personal info'), {'fields': ('first_name',
                                         'last_name',
                                         'email',
                                         'nickname'
        )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('PC Info'), {'fields': ('ip_address', 'mac')}),
        (_('Gottacon Requirements'), {'fields': ('verification_received',
                                                 'has_antivirus',
                                                 'has_firewall',
                                                 'dhcp_enabled',
                                                 'signed_waiver',
                                                 'reg_errors',
        )}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
        ),
    )


class ResponseCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'good_to_go',)
    list_filter = ('good_to_go', )


admin.site.register(RegisteredUser, RegisteredUserAdmin)
admin.site.register(ResponseCode, ResponseCodeAdmin)