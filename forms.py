from django import forms
from .models import Command
class NewCommandForm(forms.Form):
    command_type = forms.ChoiceField(label='', choices=Command.COMMAND_TYPES)
    command_param = forms.CharField(label='', max_length=100, required=False)
