from django import forms
from network.models import Vlan


class VlanForm(forms.Form):

    vlan = forms.ModelChoiceField(queryset=Vlan.objects.all())
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)