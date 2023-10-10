from django.contrib import admin
from .models import User, Profile

class UserAdmin(admin.ModelAdmin):
    list_display = ['firstName', 'lastName', 'username', 'email']
    list_display_links = ['username', 'email']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'country', 'state', 'city']


admin.site.register(User, UserAdmin)
admin.site.register(Profile,ProfileAdmin )

