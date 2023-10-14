from django import forms
from .models import User, Profile
from vendor.models import Vendor


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['firstName', 'lastName',
                  'username', 'email', 'phone', 'password', 'confirm_password']


def clean(self):
    cleaned_data = super(UserForm, self).clean()
    password = cleaned_data.get('password')
    confirm_password = cleaned_data.get('confirm_password')

    if password != confirm_password:
        raise forms.ValidationError("Passwords do not match")


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['ven_name', 'ven_license']
