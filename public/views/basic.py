from django.shortcuts import render, redirect
from ..models import Member, UserInfo
import requests

def index(request, server_id):
    data = request.GET

    toast = None
    if 'login' in data:
        toast = {
            "text": "<strong>Logged in!</strong>",
            "type": "primary"
        }
    if 'logout' in data:
        toast = {
            "text": "<strong>Logged out.</strong>",
            "type": "primary"
        }


    return render(request, "public/index.html", {
        "toast": toast,
        "server_id": server_id
    })

# TODO: Auto-generate staff info or manually design?
def about(request):
    #staff = User.objects.filter(staff=True)
    return render(request, "public/about.html", {
        "staff": "todo"
    })

# TODO: once we have the data, exclude users who aren't in the discord anymore
def rankings(request):
    result = requests.get("https://mee6.xyz/levels/176186766946992128?json=0")
    json = result.json()
    rank = 1
    for person in json['players']:
        person['rank'] = rank
        rank = rank + 1

    return render(request, "public/rankings.html", {
        "players": json['players']
    })

def account(request):
    if request.user.is_authenticated:
        return render(request, "public/account.html", {
            "info": UserInfo.get(request.user)
        })
    else:
        return redirect("public:index")