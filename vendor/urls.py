from django.urls import path
from .import views
from accounts import views as acc_views
from menu import views as menu_views


urlpatterns = [
    path('', acc_views.vendorDashboard, name='vendor'),
    path('profile/', views.vProfile, name='vendor-profile'),
    path('menu-builder', views.menuBuilder, name='menu-builder'),
    path('menu-builder/category/<str:pk>/',
         views.foodItemByCategory, name='food-item-by-category'),
    path('menu-builder-category-add/', views.addCategory, name='add-category'),
    path('menu-builder-category-edit/<str:pk>/',
         views.editCategory, name='edit-category')

]
