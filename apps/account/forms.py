import datetime
from datetime import timedelta
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    """Login form"""
    username = forms.CharField(max_length=30, required=True, label=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write username...'}))
    password = forms.CharField(max_length=20, required=True, label=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password...'}))

    class Meta: 
        fields = ('username', 'password')


class ChangePasswordForm(PasswordChangeForm):
    """Change password form"""
    old_password = forms.CharField(max_length=30, required=True, label="Old Password ", widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Write old password...'}))
    new_password1 = forms.CharField(max_length=30, required=True, label="New Password ", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New password...'}))
    new_password2 = forms.CharField(max_length=30, required=True, label="Confirm Password ", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new password...'}))

    class Meta: 
        fields = ('old_password', 'new_password1', 'new_password2')
