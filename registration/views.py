import json
import logging

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from registration.models import RegisteredUser
from unix_mac import get_mac_address
from registration.forms import RegistrationForm, VerificationResponseForm, WaiverForm, LoginForm
from django.template import loader, RequestContext
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


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

    return render(request, 'registration/login.html', {'form': form})


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
            return render(request, 'registration/register.html', {'form': form})

    return render(request, 'registration/register.html', {'form': form})


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

    registered_user = request.user

    context = {
        'registered_user': registered_user
    }

    return render(request, 'registration/verification.html', context)


@login_required
def verify_download(request):
    registered_user = request.user

    context = {
        'registered_user': registered_user
    }

    #t = loader.get_template('registration/../_media/binaries/hostname.ps1')
    t = loader.get_template('binaries/hostname.ps1')
    c = RequestContext(request, context)

    powershell_script = t.render(c)

    response = HttpResponse(powershell_script)
    response['Content-Disposition'] = 'attachment; filename=assess-%s.ps1' % registered_user.uuid

    return response


@login_required
def check_verification(request):

    response = {
        'verification_received': request.user.verification_received,
        'ready2lan': False,
        'antivirus': False,
        'firewall': False,
        'dhcp': False,
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
    user.verification_received = True

    if form_valid:
        response = {'detail': 'Dobbo is good'}
    else:
        user.reg_errors = json.dumps(form.errors)
        response = form.errors

    user.save()

    return JsonResponse(response, status=200)


def get_uuid_for_ip(request):

    log.info(request.META.get('REMOTE_ADDR'))

    registered_user = RegisteredUser.objects.get(ip_address=request.META.get('REMOTE_ADDR'))

    resp = {
        'uuid': registered_user.uuid,
        'ip': request.META.get('REMOTE_ADDR'),
    }

    return HttpResponse(json.dumps(resp), content_type='application/json')