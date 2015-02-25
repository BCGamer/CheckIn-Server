import json
import logging
from django.core.urlresolvers import reverse

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.conf import settings
from django.template import loader, RequestContext
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.views.generic import TemplateView

from registration.models import RegisteredUser
from unix_mac import get_mac_address
from registration.forms import RegistrationForm, VerificationResponseForm, WaiverForm, LoginForm, \
    OverrideVerificationForm
from network.models import Vlan, Switch
from network.tasks import flip_users_vlan

log = logging.getLogger(__name__)


def home(request):

    meta = request.META

    return render(request, 'registration/mac_test.html', {
        'meta': meta,
        'mac': get_mac_address(request.META['REMOTE_ADDR'])
    })


def login_user(request):

    # form = AuthenticationForm(data=request.POST or None)
    form = LoginForm(data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('waiver')

    return render(request, 'registration/login.html', {'form': form, 'override_form': OverrideVerificationForm()})


def logout_user(request):
    logout(request)

    return redirect('/login/')


def register(request):

    if request.user.is_authenticated():
        return redirect('verify')

    context = {}

    form = RegistrationForm(request.POST or None)

    if request.POST:
        if form.is_valid():
            registered_user = form.save(commit=False)
            registered_user.ip_address = request.META.get('REMOTE_ADDR')
            registered_user.username = form.cleaned_data['email'].lower()
            registered_user.email = form.cleaned_data['email'].lower()
            registered_user.set_password(form.cleaned_data['password'])
            registered_user.save()
            registered_user.backend = "django.contrib.auth.backends.ModelBackend"

            login(request, registered_user)

            return redirect('waiver')

        else:
            return render(request, 'registration/register.html', {'form': form, 'override_form': OverrideVerificationForm() })

    return render(request, 'registration/register.html', {'form': form, 'override_form': OverrideVerificationForm() })


@login_required
def waiver(request):

    registered_user = request.user

    form = WaiverForm(request.POST or None)

    if registered_user.waiver_signed:
        return redirect('verify')

    if request.POST:
        if form.is_valid():
            registered_user.age_under_18 = form.cleaned_data['age_under_18']
            registered_user.waiver_signed = form.cleaned_data['waiver_signed']
            registered_user.guardian_name = form.cleaned_data['guardian_name']
            registered_user.guardian_phone = form.cleaned_data['guardian_phone']
            registered_user.save()

            return redirect('verify')
        else:
            return render(request, 'registration/waiver.html', {'form': form})

    return render(request, 'registration/waiver.html', {'form': form})


@login_required
def verify(request):

    if not request.META.get('REMOTE_ADDR').startswith(settings.DIRTY_SUBNETS):
        return redirect('verified')

    registered_user = request.user

    override_form = OverrideVerificationForm()

    context = {
        'registered_user': registered_user,
        'override_form': override_form,
    }

    return render(request, 'registration/verification.html', context)



@require_POST
def override_verification(request):

    form = OverrideVerificationForm(request.POST or None)

    if form.is_valid():
        vlan = form.cleaned_data.get('vlan')
        mac = form.cleaned_data.get('mac_address')

        if Switch.objects.flip_vlan(mac, vlan.num):
            # Successfully switched vlan for mac, redirect to success page
            if request.path == reverse('register_override') or request.path == reverse('login_override'):
                return redirect('override_complete')
            else:  # path == '/verification/override/'
                return redirect('verified')
        else:
            # Could not find mac or something went wrong - redirect to verify page with error
            messages.error(request, 'Could not find mac or something went wrong')

    else:
        for field, error in form.errors.items():
            messages.error(request, '%s: %s' % (field.replace('_', ' ').title(), error[0]))

    if request.path == reverse('override_verification'):
        return redirect('verify')

    elif request.path == reverse('login_override'):
        return redirect('login')

    else:  # request.path == '/override/':
        return redirect('register')


class OverrideCompleteTemplateView(TemplateView):
    template_name = 'registration/override_complete.html'

override_complete = OverrideCompleteTemplateView.as_view()


@login_required
def verify_completed(request):
    registered_user = request.user
    context = {
        'registered_user': registered_user
    }
    # If we don't change the user's IP address after it
    # gets reset we could end up with an IP conflict
    # django -> c# app relies on this being relatively unique
    registered_user.ip_address = request.META.get('REMOTE_ADDR')

    return render(request, 'registration/verification_complete.html', context)


@login_required
def verify_download(request):

    registered_user = request.user

    context = {
        'registered_user': registered_user
    }

    # Renaming this file will cause Windows Defender
    # and browser security to freak out
    with open('registration/assets/bcg_system_verification.exe', 'rb') as checkin_exe:

        response = HttpResponse(checkin_exe)
        response['Content-Disposition'] = 'attachment; filename=bcg_system_verification.exe'

    return response


@login_required
def check_verification(request):

    response = {
        'verification_received': request.user.verification_received,
        'ready2lan': False,
        #'antivirus': False,
        'antivirus': request.user.has_antivirus,
        #'firewall': False,
        'firewall': request.user.has_firewall,
        #'dhcp': False,
        'dhcp': request.user.dhcp_enabled,
    }

    if request.user.verification_received:
        if request.user.reg_errors:
            response['errors'] = json.loads(request.user.reg_errors)
        if not request.user.ready2lan():
            response['antivirus'] = request.user.has_antivirus
            response['firewall'] = request.user.has_firewall
            response['dhcp'] = request.user.dhcp_enabled
        else:
            response['ready2lan'] = True

    return JsonResponse(response)


@require_POST
@csrf_exempt
def verification_response(request):

    print(request.POST)
    print(request.body)

    if request.method != 'POST':
        return HttpResponseBadRequest()

    form = VerificationResponseForm(request.POST)

    user = get_object_or_404(RegisteredUser, uuid=request.POST.get('uuid'))

    form_valid = form.is_valid()

    user.dhcp_enabled = form.dhcp_good
    user.has_antivirus = form.antivirus_good
    user.has_firewall = form.firewall_good
    user.mac = form.mac_good
    user.verification_received = True

    if form_valid:
        response = {'detail': 'Good'}
    else:
        user.reg_errors = json.dumps(form.errors)
        response = form.errors

    user.save()

    if user.ready2lan():
        flip_users_vlan.delay(str(user.mac))

    return JsonResponse(response, status=200)


def get_uuid_for_ip(request):

    ipaddress = request.META.get('REMOTE_ADDR')
    log.info(ipaddress)

    registered_user = RegisteredUser.objects.get(ip_address=ipaddress)

    resp = {
        'uuid': registered_user.uuid,
        'ipaddress': ipaddress,
    }

    return HttpResponse(json.dumps(resp), content_type='application/json')


@login_required
def has_ip_changed(request):
    ipaddress_browser = request.META.get('REMOTE_ADDR')
    ipaddress_user = request.user.ip_address

    if ipaddress_browser != ipaddress_user:
        response = {
            'ip_address_changed': True
        }
        request.user.ip_address = ipaddress_browser
        request.user.save()
    else:
        response = {
            'ip_address_changed': False
        }

    return HttpResponse(json.dumps(response), content_type='application/json')