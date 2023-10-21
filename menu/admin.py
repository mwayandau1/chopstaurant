from django.contrib import admin
from .models import FootItem, Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['vendor', 'category_name', 'created']
    prepopulated_fields = {('slug'): ('category_name',)}
    search_fields = ('vendor__ven_name', 'category_name',)


class FoodItemAdmin(admin.ModelAdmin):
    list_display = ['vendor', 'category', 'title', 'price', 'is_available', ]
    prepopulated_fields = {('slug'): ('title',)}
    search_fields = ['vendor__ven_name',
                     'category__category_name', 'title', 'price']
    list_filter = ('is_available',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(FootItem, FoodItemAdmin)
