import uuid
from django.db import models
# Create your models here.
from django_extensions.db.fields import UUIDField

from django.contrib.auth.models import AbstractUser


class RegisteredUser(AbstractUser):



    has_firewall = models.BooleanField(default=False)
    has_antivirus = models.BooleanField(default=False)
    dhcp_enabled = models.BooleanField(default=False)
    shared_file_print_off = models.BooleanField(default=False)

    verification_received = models.BooleanField(default=False)

    hostname = models.CharField(max_length=50, blank=True)
    mac = models.CharField(max_length=20, blank=True, null=True)
    ip_address = models.IPAddressField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    gottacon_id = models.CharField(max_length=50, blank=True, null=True)

    time_in = models.DateTimeField(blank=True, null=True)
    time_out = models.DateTimeField(blank=True, null=True)

    uuid = UUIDField(default=str(uuid.uuid4()))