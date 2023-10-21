from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required, user_passes_test


from .forms import VendorForm, CategoryForm
from accounts.forms import ProfileForm
from .models import Vendor
from accounts.models import Profile
from menu.models import FootItem, Category


def getVendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor


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


@login_required(login_url='login')
@user_passes_test(checkRoleVendor)
def menuBuilder(request):
    vendor = getVendor(request)
    categories = Category.objects.filter(vendor=vendor).order_by('-created')
    context = {
        'vendor': vendor,
        'categories': categories
    }
    return render(request, 'vendor/menu-builder.html', context)


@login_required(login_url='login')
@user_passes_test(checkRoleVendor)
def foodItemByCategory(request, pk):
    vendor = getVendor(request)
    category = get_object_or_404(Category, id=pk)
    food_items = FootItem.objects.filter(vendor=vendor, category=category)
    context = {
        'food_items': food_items,
        'category': category
    }
    return render(request, 'vendor/food-item-by-category.html', context)


def addCategory(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = getVendor(request)
            category.slug = slugify(category_name)
            category.save()
            messages.success(request, "Your new category has been added!")
            return redirect('menu-builder')
        else:
            messages.error(request, "There was something wrong ")

    context = {
        'form': form
    }

    return render(request, 'vendor/add-category.html', context)


def editCategory(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(instance=category)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.slug = slugify(category_name)
            category.vendor = getVendor(request)
            category.save()
            messages.success(request, 'Your category has been updated!')
            return redirect('menu-builder')
    context = {
        'form': form,
        'category': category
    }

    return render(request, 'vendor/add-category.html', context)
