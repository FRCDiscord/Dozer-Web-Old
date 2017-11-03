from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def logout_view(request):
    logout(request)
    # TODO: redirect to a successfully logged-out page
    dest = redirect('public:index')
    dest['Location'] += "?logout"
    return dest

def login_or_register(request):
    if request.method == 'GET':
        return render(request, "public/login_register.html", {})
    else:
        data = request.POST
        username = data['username']
        password = data['password']
        if data['type'] == 'login':
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                dest = redirect('public:index')
                dest['Location'] += "?login"
                return dest
            else:
                return render(request, "public/login_register.html", {
                    "error": "Login Error: Invalid login credentials."
                })
        elif data['type'] == 'register':
            try:
                user = User.objects.create_user(username, None, password)
                user.save()
                login(request, user)
                dest = redirect('public:index')
                dest['Location'] += "?login"
                return dest
            except:
                return render(request, "public/login_register.html", {
                    "error": "Registration Error: Username taken. Perhaps you meant to log in?"
                })

        return redirect('public:index')