from django.contrib import admin
from django.urls import path, include
from . import views
from taskmanager import settings

app_name = 'accounts'
urlpatterns = [
     
    #path('login', views.login_view, name='login'),       
    path('user_login/',views.user_login, name='user_login'),
    path('user_register/',views.user_register, name='user_register'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout, name='logout')
    
]