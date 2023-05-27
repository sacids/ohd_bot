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
        self.fields['message_type'].empty_label  = ('Select')
        self.fields['validation'].empty_label  = ('Select')
        self.fields['action'].empty_label  = ('Select')

    class Meta:
        model  = Thread
        exclude = ('created_by', 'updated_by')
        fields  = ('__all__')

        widgets = {
            'title': forms.Textarea(attrs={'class': '', 'id': 'title', 'placeholder': 'Write title in Swahili...', 'rows': 2 }),
            'title_en_us': forms.Textarea(attrs={'class': '', 'id': 'title_en', 'placeholder': 'Write title in English...', 'rows': 2 }),
            'block': forms.NumberInput(attrs={'class': 'form-control', 'id': 'flag', 'placeholder': 'Write thread block...', 'required': '' }),
            'db_flag': forms.TextInput(attrs={'class': 'form-control', 'id': 'flag', 'placeholder': 'Write flag...', 'required': '' }),
            'label': forms.TextInput(attrs={'class': 'form-control', 'id': 'label', 'placeholder': 'Write label...', 'required': '' }),
            'validation': forms.Select(attrs={'class': 'form-control', 'id': 'validation', 'placeholder': 'Write validation...', }),
            'message_type': forms.Select(attrs={'class': 'form-control', 'id': 'message_type', 'placeholder': 'Write message type...', }),
            'action': forms.Select(attrs={'class': 'form-control', 'id': 'action', 'placeholder': 'action...' }),
            'action_url': forms.TextInput(attrs={'class': 'form-control', 'id': 'action', 'placeholder': 'Write action url...', }),
        } 

        labels = {
            'title': 'Title SW',
            'title_en_us': 'Title EN',
            'block': 'Block',
            'db_flag': 'Flag',
            'label': 'Label',
            'message_type': 'Message Type',
            'validation': 'Validation Rules',
            'action': 'Action',
            'action_url': 'Action URL',
        }      
