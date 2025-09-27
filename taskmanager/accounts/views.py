from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserLogin, CustomUserCreationForm, UserProfileForm  # Add this import, adjust path if needed

# Create your views here.


@login_required
def logout(request):
    auth.logout(request)
    return redirect('accounts:user_login')

def login_view(request):
    if request.method == 'POST':
        form = UserLogin(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard:home') 
    else:
        form = UserLogin()
    return render(request, 'accounts/user_login.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLogin(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard:home') 
    else:
        form = UserLogin()
    return render(request, 'accounts/user_login.html', {'form': form})


def user_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully.")
            login(request, user)
            return redirect('accounts:user_login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/user_register.html', {'form': form})

@login_required
def profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated!")
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'accounts/profile.html', {'form': form})