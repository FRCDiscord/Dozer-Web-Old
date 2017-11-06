import requests
import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from ..models import UserInfo, Server


def logout_view(request, server_id):
    logout(request)
    dest = redirect('public:index', server_id)
    dest['Location'] += "?logout"
    return dest

def login_or_register(request, server_id):
    if request.method == 'GET':
        discord_url = "https://discordapp.com/oauth2/authorize?response_type=code&client_id=%s&scope=identify&state=%s&redirect_uri=" % (settings.DISCORD_CLIENT_ID, server_id)
        discord_url += request.build_absolute_uri(reverse('public:discord_auth'))
        return render(request, "public/login_register.html", {
            "discord_url": discord_url,
            "server": Server.get(server_id)
        })
    else:
        data = request.POST
        username = data['username']
        password = data['password']
        if data['type'] == 'login':
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                dest = redirect('public:index', server_id)
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
                info = UserInfo(user=user, discord=False)
                info.save()
                login(request, user)


                dest = redirect('public:index', server_id)
                dest['Location'] += "?login"
                return dest
            except:
                return render(request, "public/login_register.html", {
                    "error": "Registration Error: Username taken. Perhaps you meant to log in?"
                })

        return redirect('public:index')

API_ENDPOINT = "https://discordapp.com/api/v6"

def discord(request):
    data = request.GET
    state = data['state']
    code = data['code']

    res = exchange_code(request, code)
    token = res['access_token']

    headers = {
        'Authorization': 'Bearer %s' % token
    }
    r = requests.get('%s/users/@me' % API_ENDPOINT, headers=headers)
    res = json.loads(r.text)

    username = res['username']
    discriminator = res['discriminator']
    acc = username + "#" + discriminator
    try:
        user = User.objects.get(username=acc)
    except:
        user = User.objects.create_user(acc, None, None)
        user.save()
        info = UserInfo(user=user, discord=True, avatar=res['avatar'])
        info.save()
    login(request, user)

    dest = redirect('public:index', state)
    dest['Location'] += "?login"
    return dest

def exchange_code(request, code):
    data = {
        'client_id': settings.DISCORD_CLIENT_ID,
        'client_secret': settings.DISCORD_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': request.build_absolute_uri(reverse('public:discord_auth'))
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post('%s/oauth2/token' % API_ENDPOINT, data, headers)
    r.raise_for_status()
    return r.json()
