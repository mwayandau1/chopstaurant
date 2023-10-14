from django.contrib import admin
from .models import Vendor

# Register your models here.


class VendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'ven_name', 'is_approved', 'created')


admin.site.register(Vendor, VendorAdmin)
