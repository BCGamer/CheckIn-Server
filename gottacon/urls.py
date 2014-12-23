from django.conf.urls import patterns, include, url

from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gottacon.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^login/$', 'registration.views.login_user', name='login'),
    url(r'^logout/$', 'registration.views.logout_user', name='logout'),

    url(r'^$', 'registration.views.register', name='register'),

    url(r'^waiver/$', 'registration.views.waiver', name='waiver'),

    url(r'^verify/$', 'registration.views.verify', name='verify'),
    url(r'^verify/check/$', 'registration.views.check_verification', name='check_verification'),
    url(r'^verify/dl/$', 'registration.views.verify_download', name='verify_dl'),
    url(r'^verify/uuidforip/$', 'registration.views.get_uuid_for_ip', name='uuid_for_ip'),

    url(r'^verification_response/$', 'registration.views.verification_response', name='verification_resp'),

    url(r'^admin/', include(admin.site.urls)),
)
