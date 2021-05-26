from django import forms 

from .models import Toolbox

class ToolboxForm(forms.ModelForm):
    class Meta:
        model = Toolbox
        fields = [
            'msisdn',
            'status'
        ]

