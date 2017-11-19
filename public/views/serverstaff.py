from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from ..models import Server, Mail, Member

@csrf_exempt
def staff_index(request, server_id):
    server = Server.get(server_id)
    if isStaff(request.user, server):
        q = Q()
        q &= ~Q(state="spam")
        q &= ~Q(state="resolved")
        return render(request, "public/staff_index.html", {
            "all_mail": Mail.objects.filter(q),
            "server": server
        })
    else:
        raise Http404("User who is not staff tried to access a staff page")


@csrf_exempt
def staff_mail_update(request, server_id):
    if request.method == 'GET':
        return JsonResponse({
            "success": False,
            "error": "This is used via POST."
        })
    else:
        if request.user.is_authenticated:
            server = Server.get(server_id)
            if not server:
                return JsonResponse({
                    "success": False,
                    "error": "Server does not exist."
                })
            member = Member.getMember(user=request.user, server=server)
            if not member or (member and not member.staff):
                return JsonResponse({
                    "success": False,
                    "error": "Insufficient permissions."
                })
            data = request.POST
            try:
                type = data['type']
                mail_id = data['mail_id']
            except:
                return JsonResponse({
                    "success": False,
                    "error": "Invalid or missing arguments."
                })
            try:
                mail = Mail.objects.get(id=mail_id, server__id=server_id)
            except:
                return JsonResponse({
                    "success": False,
                    "error": "Invalid mail ID and/or server ID data."
                })

            if type == "delete":
                mail.delete()
                print("DE-LETE")
            else:
                mail.state = type
                mail.save()

            return JsonResponse({
                "success": True
            })
        else:
            return JsonResponse({
                "success": False,
                "error": "Insufficient permissions."
            })

def isStaff(user, server):
    return Member.getMember(user=user, server=server).staff