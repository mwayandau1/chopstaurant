from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from django.contrib.auth.decorators import login_required, user_passes_test


from .forms import VendorForm
from accounts.forms import ProfileForm
from .models import Vendor
from accounts.models import Profile


def checkRoleVendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


@login_required(login_url='login')
@user_passes_test(checkRoleVendor)
def vProfile(request):
    try:

        profile = get_object_or_404(Profile, user=request.user)
        vendor = get_object_or_404(Vendor, user=request.user)
    except:
        profile = None
        vendor = None
    p_form = ProfileForm(instance=profile)
    v_form = VendorForm(instance=vendor)

    if request.method == 'POST':
        p_form = ProfileForm(request.POST, request.FILES, instance=profile)
        v_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if p_form.is_valid() and v_form.is_valid():
            p_form.save()
            v_form.save()
            messages.success(
                request, 'Your restaurant settings has been updated!')
            return redirect('vendor-dashboard')

    context = {
        'profile_form': p_form,
        'vendor_form': v_form,
        'profile': profile,
        'vendor': vendor
    }
    return render(request, 'vendor/profile.html', context)
