import uuid
from django.db import models
# Create your models here.
from django_extensions.db.fields import UUIDField

from django.contrib.auth.models import AbstractUser


def generate_uuid():
    return str(uuid.uuid4())


class RegisteredUser(AbstractUser):

    has_firewall = models.BooleanField(default=False)
    has_antivirus = models.BooleanField(default=False)
    dhcp_enabled = models.BooleanField(default=False)

    reg_errors = models.TextField(blank=True)

    verification_received = models.BooleanField(default=False)

    age_under_18 = models.BooleanField(default=False)
    waiver_signed = models.BooleanField(default=False)
    guardian_name = models.CharField(max_length=50, blank=True, null=True)
    guardian_phone = models.CharField(max_length=50, blank=True, null=True)

    hostname = models.CharField(max_length=50, blank=True)
    mac = models.CharField(max_length=20, blank=True, null=True)
    ip_address = models.IPAddressField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    gottacon_id = models.CharField(max_length=50, blank=True, null=True)
    nickname = models.CharField(max_length=50, blank=True, null=True)

    time_in = models.DateTimeField(blank=True, null=True)
    time_out = models.DateTimeField(blank=True, null=True)

    uuid = UUIDField( default=generate_uuid )

    def ready2lan(self):
        return all([self.has_firewall, self.has_antivirus, self.dhcp_enabled])


class ResponseCode(models.Model):

    good_to_go = models.BooleanField(default=False)
    code = models.CharField(max_length=6)

    def __unicode__(self):
        return '{self.code}'.format(self=self)