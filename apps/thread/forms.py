import datetime
from datetime import timedelta
from django import forms
from .models import *

class ThreadForm(forms.ModelForm):
    """
    A class to create form
    """
    def __init__(self, *args, **kwargs):
        super(ThreadForm, self).__init__(*args, **kwargs)
        self.fields['action'].empty_label  = ('Select')

    class Meta:
        model  = Thread
        exclude = ('created_by', 'updated_by')
        fields  = ('__all__')

        widgets = {
            'title': forms.Textarea(attrs={'class': '', 'id': 'title', 'placeholder': 'Write title...', 'rows': 3 }),
            'block': forms.NumberInput(attrs={'class': 'form-control', 'id': 'flag', 'placeholder': 'Write thread block...', 'required': '' }),
            'db_flag': forms.TextInput(attrs={'class': 'form-control', 'id': 'flag', 'placeholder': 'Write flag...', 'required': '' }),
            'label': forms.TextInput(attrs={'class': 'form-control', 'id': 'label', 'placeholder': 'Write label...', 'required': '' }),
            'validate': forms.TextInput(attrs={'class': 'form-control', 'id': 'verify', 'placeholder': 'Validate...' }),
            'validate_url': forms.TextInput(attrs={'class': 'form-control', 'id': 'verify_url', 'placeholder': 'Write validation url...', }),
            'action': forms.Select(attrs={'class': 'form-control', 'id': 'action', 'placeholder': 'action...' }),
            'action_url': forms.TextInput(attrs={'class': 'form-control', 'id': 'action', 'placeholder': 'Write action url...', }),
        } 

        labels = {
            'title': 'Title',
            'block': 'Block',
            'db_flag': 'Flag',
            'label': 'Label',
            'validate': 'Validation',
            'validate_url': 'Validation URL',
            'action': 'Action',
            'action_url': 'Action URL',
        }      
