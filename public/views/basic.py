from django.shortcuts import render, redirect
from ..models import Server, UserInfo, Member
import requests

def dozer_index(request):
    return render(request, "public/base.html")

def index(request, server_id):
    data = request.GET

    toast = None
    if 'login' in data:
        toast = {
            "text": "<strong>Logged in!</strong>",
            "type": "success"
        }
    if 'logout' in data:
        toast = {
            "text": "<strong>Logged out.</strong>",
            "type": "danger"
        }


    return render(request, "public/index.html", {
        "toast": toast,
        "server": Server.get(server_id)
    })

# TODO: Auto-generate staff info or manually design?
def about(request, server_id):
    #staff = User.objects.filter(staff=True)
    return render(request, "public/about.html", {
        "staff": "todo",
        "server": Server.get(server_id)
    })

# TODO: once we have the data, exclude users who aren't in the discord anymore
def rankings(request, server_id):
    result = requests.get("https://mee6.xyz/levels/176186766946992128?json=0")
    json = result.json()
    rank = 1
    for person in json['players']:
        person['rank'] = rank
        rank = rank + 1

    return render(request, "public/rankings.html", {
        "players": json['players'],
        "server": Server.get(server_id)
    })

def account(request, server_id):
    if request.user.is_authenticated:
        server = Server.get(server_id)
        return render(request, "public/account.html", {
            "info": UserInfo.get(request.user),
            "member": Member.getMember(user=request.user, server=server),
            "server": server
        })
    else:
        return redirect("public:index", server_id)