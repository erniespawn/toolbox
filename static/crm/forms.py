from django import forms 

from .models import CdrProcess, EsmeDlr

class CdrProcessForm(forms.ModelForm):
    class Meta:
        model = CdrProcess
        fields = "__all__"

class EsmeDlrForm(forms.ModelForm):
    class Meta:
        model = EsmeDlr
        fields = "__all__"