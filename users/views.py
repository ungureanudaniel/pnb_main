from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

#------------------------LOGIN---------------------------------------
def login_view(request):
    context = {}
    template = 'users/login.html'
    
    if request.method == 'POST':
        username = request.POST.get('signin-name')
        password = request.POST.get('signin-password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            try:
                login(request, user)
                context['user'] = username
                return redirect('home')  # Redirect to the homepage or any other page
            except Exception as e:
                messages.warning(request, _("Warning! {e}").format(e=e))
                return redirect('/')
        else:
            messages.warning(request, _("User does not exist!"))
            return redirect('/')
    
    return render(request, template, context)
#---------------------------------LOGOUT VIEW-----------------------------------
def user_logout(request):
    try:
        logout(request)
    except (Exception, ValueError) as e:
        print(e)
    return redirect('/')
