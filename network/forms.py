from django import forms
from network.models import Vlan


class VlanForm(forms.Form):

    vlan = forms.ModelChoiceField(queryset=Vlan.objects.all())
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)


class SwitchPortForm(forms.Form):

    ports = [(x, x) for x in range(1,49)]

    vlan = forms.ModelChoiceField(queryset=Vlan.objects.all())
    port = forms.ChoiceField(choices=ports)
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)