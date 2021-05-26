from django import forms 

from .models import CdrProcess, EsmeDlr, sendSMS

class CdrProcessForm(forms.ModelForm):
    class Meta:
        model = CdrProcess
        fields = "__all__"

class EsmeDlrForm(forms.ModelForm):
    class Meta:
        model = EsmeDlr
        fields = "__all__"

class sendSMSForm(forms.ModelForm):
    class Meta:
        model = sendSMS
        fields = "__all__"