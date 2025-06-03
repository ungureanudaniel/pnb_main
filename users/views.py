from django.contrib.auth import authenticate, login, logout
from .forms import CustomAuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext as _

def login_view(request):
    if request.user.is_authenticated:
        return redirect('signin')  # or any page you want logged-in users to land on

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, _("Logged in successfully."))
            return redirect('auto-access')  # Change to your desired redirect
        else:
            messages.error(request, _("Invalid username or password."))
    else:
        form = CustomAuthenticationForm()

    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, _("You have been logged out."))
    return redirect('signin')
