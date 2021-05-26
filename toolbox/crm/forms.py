from django import forms 

from .models import CdrProcess

class CdrProcessForm(forms.ModelForm):
    class Meta:
        model = CdrProcess
        fields = "__all__"