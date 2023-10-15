from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages, auth
from django.core.exceptions import PermissionDenied


from .forms import UserForm, VendorForm
from .models import User, Profile
from .utils import getAccountUrl

# RESTRICT VENDOR FROM ACCESSING CUSTOMER PAGE


def checkRoleVendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


def checkRoleCustomer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            firstName = form.cleaned_data['firstName']
            lastName = form.cleaned_data['lastName']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(
                firstName=firstName, lastName=lastName,
                username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(
                request, "Your account has been registered successfully!")
            return redirect('register-user')
        else:
            pass

    else:
        form = UserForm()
    context = {'form': form, }
    return render(request, 'accounts/register-user.html', context)


def registerVendor(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in')
        return redirect('dashboard')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        ven_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and ven_form.is_valid():
            firstName = form.cleaned_data['firstName']
            lastName = form.cleaned_data['lastName']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(
                firstName=firstName, lastName=lastName,
                username=username, email=email, password=password)
            user.role = User.VENDOR
            user.save()
            vendor_profile = Profile.objects.get(user=user)
            vendor = ven_form.save(commit=False)
            vendor.user = user
            vendor.ven_profile = vendor_profile
            vendor.save()
            messages.success(
                request, "Your account has been registered successfully. Our board will approve you soon!")
            return redirect('register-vendor')

    else:

        form = UserForm()
        ven_form = VendorForm()
    context = {
        'form': form,
        'ven_form': ven_form
    }
    return render(request, 'accounts/register-vendor.html', context)


def login(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in')
        return redirect('my-account')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are logged in!')
            return redirect('my-account')
        else:
            messages.error(request, 'Password or email is incorrect')
            return redirect('login')
    return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    messages.success(request, "You are logged out!")
    return redirect('login')


@login_required(login_url='login')
def myAccount(request):
    url = getAccountUrl(request)

    return redirect(url)


@login_required(login_url='login')
@user_passes_test(checkRoleCustomer)
def customerDashboard(request):
    return render(request, 'accounts/customer-dashboard.html')


@login_required(login_url='login')
@user_passes_test(checkRoleVendor)
def vendorDashboard(request):

    return render(request, 'accounts/vendor-dashboard.html')
