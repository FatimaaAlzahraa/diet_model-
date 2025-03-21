from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup',views.signup, name='signup'),
    path('profile/',views.profile, name='profile'),
    path('profile/edit/',views.profile_edit, name='profile_edit'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('', views.home, name='home'),
    
]