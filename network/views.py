import json
import logging

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from registration.models import RegisteredUser
from unix_mac import get_mac_address
from django.template import loader, RequestContext
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


log = logging.getLogger(__name__)


def override(request):
    registered_user = request.user

    context = {
        'registered_user': registered_user
    }

