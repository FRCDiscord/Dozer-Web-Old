from django.shortcuts import render
from ..models import Server, Mail, Member


def staff_index(request, server_id):
    server = Server.get(server_id)
    if isStaff(request.user, server):
        return render(request, "public/staff_index.html", {
            "all_mail": Mail.objects.all(),
            "server": server
        })


def isStaff(user, server):
    return Member.getMember(user=user, server=server).staff