import json
import logging

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from registration.models import RegisteredUser
from unix_mac import get_mac_address
from registration.forms import RegistrationForm
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

    form = AuthenticationForm(data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('verify')

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
            registered_user.username = form.cleaned_data['gottacon_id'].lower()
            registered_user.set_password(form.cleaned_data['password'])
            registered_user.save()
            registered_user.backend = "django.contrib.auth.backends.ModelBackend"

            login(request, registered_user)

            return redirect('verify')

        else:
            return render(request, 'registration/register.html', {'form': form})

    return render(request, 'registration/register.html', {'form': form})

@login_required
def verify(request):

    registered_user = request.user

    context = {
        'registered_user': registered_user
    }


    return render(request, 'registration/powershell.html', context)

@login_required
def verify_download(request):
    registered_user = request.user

    context = {
        'registered_user': registered_user
    }

    t = loader.get_template('registration/hostname.ps1')
    c = RequestContext(request, context)

    powershell_script = t.render(c)

    response = HttpResponse(powershell_script)
    response['Content-Disposition'] = 'attachment; filename=assess-%s.ps1' % registered_user.uuid

    return response

@login_required
def check_verification(request):

    response = {'verification_received': request.user.verification_received}

    if request.user.verification_received:
        response['antivirus'] = request.user.has_antivirus
        response['firewall'] = request.user.has_firewall
        response['sfp'] = request.user.shared_file_print_off
        response['dhcp'] = request.user.dhcp_enabled

    return HttpResponse(json.dumps(response), content_type='application/json')

@csrf_exempt
def verification_response(request):

    if request.method != 'POST':
        return HttpResponseBadRequest()

    user = get_object_or_404(RegisteredUser, uuid=request.POST.get('uuid'))

    firewall = request.POST.get('firewall')
    antivirus = request.POST.get('antivirus')
    dhcp = request.POST.get('dhcp')
    sfp = request.POST.get('sfp')

    user.has_firewall = True if firewall == 'good' else False
    user.has_antivirus = True if antivirus == 'good' else False
    user.shared_file_print_off = True if sfp == 'good' else False
    user.dhcp_enabled = True if dhcp == 'good' else False

    user.save()

    return HttpResponse(status=200)


def get_uuid_for_ip(request):

    log.info(request.META.get('REMOTE_ADDR'))

    registered_user = RegisteredUser.objects.get(ip_address=request.META.get('REMOTE_ADDR'))

    resp = {
        'uuid': registered_user.uuid,
        'ip': request.META.get('REMOTE_ADDR'),
    }

    return HttpResponse(json.dumps(resp), content_type='application/json')