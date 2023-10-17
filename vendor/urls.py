from django.urls import path
from .import views
from accounts import views as acc_views


urlpatterns = [
    path('', acc_views.vendorDashboard, name='vendor'),
    path('profile/', views.vProfile, name='vendor-profile'),
]
