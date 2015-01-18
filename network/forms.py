from django import forms
from network.models import VLAN


class VlanForm(forms.Form):

    vlan = forms.ModelChoiceField(queryset=VLAN.objects.all())
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)