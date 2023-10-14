from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User
from django.contrib import messages


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
