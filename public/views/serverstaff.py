from django.shortcuts import render, redirect
from ..models import Server, UserInfo, Member


def staff_index(request, server_id):
    server = Server.get(server_id)
    if isStaff(request.user, server):
        return render(request, "public/staff_index.html", {
            "server": server
        })


def isStaff(user, server):
    return Member.getMember(user=user, server=server).staff