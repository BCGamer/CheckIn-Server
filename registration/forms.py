from django import forms
from registration.models import RegisteredUser
from django.contrib.auth.forms import AuthenticationForm

class RegistrationForm(forms.ModelForm):

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    gottacon_id = forms.CharField(required=True, label="Handle")
    email = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())
    password_2 = forms.CharField(required=True, label='Password Repeat', widget=forms.PasswordInput())

    class Meta:
        model = RegisteredUser
        fields = (
            'first_name',
            'last_name',
            'gottacon_id',
            'email',
        )

    def clean(self):

        cleaned_data = super(RegistrationForm, self).clean()

        password1 = cleaned_data.get('password')
        password2= cleaned_data.get('password_2')

        if password1 != password2:
            return forms.ValidationError("Passwords are not the same.")

        return cleaned_data


class CaseInsenstiveAuthForM(AuthenticationForm):

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username.lower()