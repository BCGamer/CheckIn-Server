from django.conf.urls import patterns, include, url

from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'check_in.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^login/$', 'registration.views.login_user', name='login'),
    url(r'^login/override/$', 'registration.views.override_verification', name='login_override'),

    url(r'^logout/$', 'registration.views.logout_user', name='logout'),

    url(r'^$', 'registration.views.register', name='register'),
    url(r'^override/$', 'registration.views.override_verification', name='register_override'),
    url(r'^override/complete/$', 'registration.views.override_complete', name='override_complete'),

    url(r'^waiver/$', 'registration.views.waiver', name='waiver'),

    url(r'^verify/$', 'registration.views.verify', name='verify'),
    url(r'^verify/check/$', 'registration.views.check_verification', name='check_verification'),
    url(r'^verify/override/$', 'registration.views.override_verification', name='override_verification'),
    url(r'^verify/dl/$', 'registration.views.verify_download', name='verify_dl'),
    url(r'^verify/uuidforip/$', 'registration.views.get_uuid_for_ip', name='uuid_for_ip'),
    url(r'^verified/$', 'registration.views.verify_completed', name='verified'),

    url(r'^verification_response/$', 'registration.views.verification_response', name='verification_resp'),

    url(r'^admin/', include(admin.site.urls)),
)
