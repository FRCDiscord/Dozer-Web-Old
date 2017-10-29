from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from public.models import Log, User, Punishment, APIToken

def handlePOST(request):
    if request.method == 'GET':
        return JsonResponse({
            "success": False,
            "error": "This is used via POST only."
        })
    else:
        data = request.POST
        if 'token' in data:
            try:
                APIToken.objects.get(token=data['token'])
                tokenLegit = True
            except:
                tokenLegit = False
            if tokenLegit:
                return None
            else:
                return JsonResponse({
                    "success": False,
                    "error": "Invalid token."
                })
        else:
            return JsonResponse({
                "success": False,
                "error": "No token found."
            })

# TODO: confirm if this will work with the same main codebase as handlePOST
def handleGET(request):
    if request.method == 'GET':
        data = request.GET
        if 'token' in data:
            try:
                APIToken.objects.get(token=data['token'])
                tokenLegit = True
            except:
                tokenLegit = False
            if tokenLegit:
                return None
            else:
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
            "error": "This is used via GET only."
        })

@csrf_exempt
def get_logs(request):
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

@csrf_exempt
def create_log(request):
    error = handlePOST(request)
    if error == None:
        data = request.POST
        punished = User.getUser(data['punished'])
        staff = User.getUser(data['staff'])
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
