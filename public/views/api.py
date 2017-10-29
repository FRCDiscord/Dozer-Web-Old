from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, F
from public.models import Log, Member, Punishment, APIToken

# TODO: rate limit
def handle(request, type):
    if type == 'GET':
        other = 'POST'
    else:
        other = 'GET'
    if request.method == type:
        if type == 'GET':
            data = request.GET
        else:
            data = request.POST
        if 'token' in data:
            try:
                apitoken = APIToken.objects.get(token=data['token'])
                apitoken.uses = F('uses') + 1
                apitoken.save()
                return None
            except:
                return JsonResponse({
                    "success": False,
                    "error": "Invalid token."
                })

        else:
            return JsonResponse({
                "success": False,
                "error": "No token found."
            })
    else:
        return JsonResponse({
            "success": False,
            "error": "This is used via " + other + " only."
        })

def handlePOST(request):
    return handle(request, 'POST')

def handleGET(request):
    return handle(request, 'GET')

@csrf_exempt
def get_logs(request):
    error = handleGET(request)
    if error == None:
        logs = Log.objects.all()
        logsAsJSON = []
        for log in logs:
            logsAsJSON.append({
                "user": log.punished.username,
                "staff": log.staff.display(),
                "reason": log.reason,
                "punishment": log.punishment.name,
                    "punishment_length": log.punishment.timeInHours,
            "time": str(log.actionTime)
            })
        return JsonResponse({
            "log_count": len(logs),
            "logs": logsAsJSON
        })
    else:
        return error

@csrf_exempt
def create_log(request):
    error = handlePOST(request)
    if error == None:
        data = request.POST
        punished = Member.getUser(data['punished'])
        staff = Member.getUser(data['staff'])
        staff.staff = True
        staff.save()
        punishment = Punishment.objects.get(key=data['punishment'])
        log = Log(
            punished=punished,
            reason=data['reason'],
            punishment=punishment,
            staff=staff
        )
        log.save()
        return JsonResponse({
            "success": True
        })
    else:
        return error
