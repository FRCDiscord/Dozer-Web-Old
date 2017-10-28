from django.shortcuts import render
from ..models import User

def index(request):
    return render(request, "public/index.html", {})

# TODO: Auto-generate staff info or manually design?
def about(request):
    #staff = User.objects.filter(staff=True)
    return render(request, "public/about.html", {
        "staff": "todo"
    })