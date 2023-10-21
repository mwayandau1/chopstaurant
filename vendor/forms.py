from django import forms

from menu.models import Category
from .models import Vendor
from accounts.validators import validateImages


class VendorForm(forms.ModelForm):
    ven_license = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[validateImages])

    class Meta:
        model = Vendor
        fields = ['ven_name', 'ven_license']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description']
