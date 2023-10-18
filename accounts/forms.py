from django import forms
from .models import User, Profile
from .validators import validateImages


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


class ProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Start Typing Your Address...', 'required': 'required'}))
    profile_picture = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[validateImages])
    cover_photo = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[validateImages])

    # latitude = forms.CharField(
    #     widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    # longitude = forms.CharField(
    #     widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = Profile
        fields = ['profile_picture', 'cover_photo',
                  'address', 'country', 'state', 'city', 'pin_code', 'latitude', 'longitude']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'latitude' or field == 'longitude':
                self.fields[field].widget.attrs['readonly'] = 'readonly'
