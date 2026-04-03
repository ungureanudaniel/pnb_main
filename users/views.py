from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from .forms import CustomAuthenticationForm

# def login_view(request):
#     if request.user.is_authenticated:
#         return redirect('/')
    
#     if request.method == 'POST':
#         form = CustomAuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             messages.success(request, _("Logged in successfully."))
#             return redirect('/')
#         else:
#             messages.error(request, _("Invalid username or password."))
#     else:
#         form = CustomAuthenticationForm()

#     return render(request, 'users/login.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('home')
        return redirect('single_vehicle_upload')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Format the last login date properly
            last_login_msg = ""
            if user.last_login:
                # Format the date using Python strftime
                formatted_date = user.last_login.strftime('%B %d, %Y at %H:%M')
                last_login_msg = f"Last login: {formatted_date}"
            else:
                last_login_msg = "This is your first login!"
            
            # Personalized welcome message
            display_name = user.get_full_name() or user.username
            
            if user.is_staff or user.is_superuser:
                messages.success(
                    request, 
                    f"Welcome back, {display_name}! 👋 You have administrator privileges. {last_login_msg}"
                )
                messages.info(
                    request,
                    f"You can access the admin panel at <a href='/admin/'>/admin/</a> to manage content."
                )
            else:
                messages.success(
                    request,
                    f"Welcome back, {display_name}! 🏞️ Enjoy exploring Bucegi Natural Park. {last_login_msg}"
                )
            
            # Redirect based on user type
            if user.is_staff or user.is_superuser:
                return redirect('home')
            return redirect('single_vehicle_upload')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, _("You have been logged out."))
    return redirect('signin')
