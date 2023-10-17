from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages, auth
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


from .forms import UserForm, VendorForm
from .models import User, Profile
from .utils import getAccountUrl
from .utils import send_email_verification
from vendor.models import Vendor

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
            email_template = 'accounts/email/account_verification_email.html'
            mail_subject = "Please click on the link to activate your account"

            send_email_verification(
                request, user, mail_subject, email_template)
            return redirect('login')
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
            email_template = 'accounts/email/account_verification_email.html'
            mail_subject = "Please click on the link to activate your account"

            send_email_verification(
                request, user, mail_subject, email_template)
            return redirect('register-vendor')

    else:

        form = UserForm()
        ven_form = VendorForm()
    context = {
        'form': form,
        'ven_form': ven_form
    }
    return render(request, 'accounts/register-vendor.html', context)


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (User.DoesNotExist, TypeError, ValueError, OverflowError):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated")
        return redirect('my-account')
    else:
        messages.error(request, "Invalid activation link")
        return redirect('my-account')


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


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email__iexact=email).exists():
            user = User.objects.get(email__iexact=email)
            email_template = 'accounts/email/reset-password-email.html'
            mail_subject = "Please reset your password!"
            send_email_verification(
                request, user, mail_subject=mail_subject, email_template=email_template)
            messages.info(
                request, "A reset link has been sent to your email address. Please follow it and reset your password")
            return redirect('login')

    return render(request, 'accounts/forgot-password.html')


def resetPasswordValidate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (User.DoesNotExist, TypeError, ValueError, OverflowError):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, "Please reset your password")
        return redirect('reset-password')
    else:
        messages.error(request, 'This link has expired!')
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session['uid']
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(
                request, "Your password has been reset successfully!")
            return redirect('my-account')
        else:
            messages.error(request, "Passwords do not match!")
            return redirect('reset-password')
    return render(request, 'accounts/reset-password.html')


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
    vendor = Vendor.objects.get(user=request.user)
    context = {
        'vendor': vendor,
    }

    return render(request, 'accounts/vendor-dashboard.html', context)
