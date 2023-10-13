from django import forms
from .models import User, Profile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['firstName', 'lastName',
                  'username', 'email', 'phone', 'password', 'confirm_password']
