from django import forms
from registration.models import RegisteredUser
from django.contrib.auth.forms import AuthenticationForm

class RegistrationForm(forms.ModelForm):

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    gottacon_id = forms.CharField(required=True, label="Attendee ID")
    nickname = forms.CharField(required=True, label="In Game Name / Handle")
    email = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())
    password_2 = forms.CharField(required=True, label='Password Repeat', widget=forms.PasswordInput())

    class Meta:
        model = RegisteredUser
        fields = (
            'first_name',
            'last_name',
            'gottacon_id',
            'nickname',
            'email',
        )

    def clean(self):

        cleaned_data = super(RegistrationForm, self).clean()

        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('password_2')

        if password1 != password2:
            return forms.ValidationError("Passwords are not the same.")

        return cleaned_data


class CaseInsenstiveAuthForM(AuthenticationForm):

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username.lower()


class VerificationResponseForm(forms.Form):

    DHCP_CHOICES = (
        ('True', 'True'),
        ('False', 'False'),
        ('Problem', 'Problem'),
    )

    SECOND_BLOCK_GOOD_CODES = ['10', '11']  # enabled
    SECOND_BLOCK_BAD_CODES = ['00', '01']  # disabled

    THIRD_BLOCK_GOOD_CODES = ['00']  # up to date
    THIRD_BLOCK_BAD_CODES = ['10']  # out of date

    firewall = forms.CharField(max_length=6)
    antivirus = forms.CharField(max_length=6)
    dhcp = forms.ChoiceField(choices=DHCP_CHOICES)

    firewall_good = False
    antivirus_good = False
    dhcp_good = False

    def charint_to_hex(self, value):
        try:
            firewall = hex(int(value))
        except ValueError:
            raise forms.ValidationError("Invalid Hex value submitted")

        return value

    def test_second_block(self, value):
        if value[-2:] in self.SECOND_BLOCK_BAD_CODES:
            raise forms.ValidationError("Disabled")
        elif value[-4:-2] in self.THIRD_BLOCK_BAD_CODES:
            raise forms.ValidationError("Out of date")

    def clean_dhcp(self):
        dhcp = self.cleaned_data['dhcp']

        if dhcp == 'False':
            raise forms.ValidationError("DHCP is not enabled.")

        elif dhcp == 'Problem':
            raise forms.ValidationError("DHCP configuration error was detected.")

        self.dhcp_good = True

    def clean_firewall(self):
        firewall = self.charint_to_hex(self.cleaned_data['firewall'])
        self.test_second_block(firewall)

        self.firewall_good = True

    def clean_antivirus(self):
        antivirus = self.charint_to_hex(self.cleaned_data['antivirus'])
        self.test_second_block(antivirus)

        self.antivirus_good = True


class WaiverForm(forms.ModelForm):
    age_under_18 = forms.BooleanField(required=False, label="I am under the age of 18")
    waiver_signed = forms.BooleanField(required=True, label="I acknowledge and accept")

    # these next two properties should be required if 'age_under_18 = true'
    guardian_name = forms.CharField(required=False, label="Parent or Legal Guardian name")
    guardian_phone = forms.CharField(required=False, label="Emergency phone number")

    class Meta:
        model = RegisteredUser
        fields = (
            'age_under_18',
            'waiver_signed',
            'guardian_name',
            'guardian_phone',
        )
