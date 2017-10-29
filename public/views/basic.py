from django.shortcuts import render
import requests
from ..models import User

def index(request):
    return render(request, "public/index.html", {})

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