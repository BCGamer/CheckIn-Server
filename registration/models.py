import uuid
from django.core import validators
from django.core.mail import send_mail
from django.db import models
# Create your models here.
from django.utils import timezone
from django_extensions.db.fields import UUIDField
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin, UserManager
from django.utils.translation import ugettext as _

def generate_uuid():
    return str(uuid.uuid4())


class RegisteredUser(AbstractBaseUser, PermissionsMixin):

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

    uuid = UUIDField(default=generate_uuid)

    username = models.CharField(_('username'), max_length=30, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, digits and '
                    '@/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(r'^[\w.@+-]+$', _('Enter a valid username.'), 'invalid')
        ])
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def ready2lan(self):
        return all([self.has_firewall, self.has_antivirus, self.dhcp_enabled])


class ResponseCode(models.Model):

    good_to_go = models.BooleanField(default=False)
    code = models.CharField(max_length=6)

    def __unicode__(self):
        return '{self.code}'.format(self=self)