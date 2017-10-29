from django.shortcuts import render, redirect
from ..models import Member, Log

def mail(request):
    data = request.GET
    prefill_name = ""
    name_class_add = ""
    prefill_subject = ""
    subject_class_add = ""
    appeal = None
    try:
        member = Member.objects.get(account=request.user, verified=True)
        prefill_name = member.username
        name_class_add = "disabled"
    except:
        member = None

    if 'appeal' in data and request.user.is_authenticated and member:
        try:
            appeal = Log.objects.get(key=data['appeal'])
            prefill_subject = appeal.appeal_subject()
            subject_class_add = "disabled"
        except Exception:
            appeal = None

    ctx = {
        "member": member,
        "prefill_name": prefill_name,
        "name_class_add": name_class_add,
        "prefill_subject": prefill_subject,
        "subject_class_add": subject_class_add,
        "appeal": appeal
    }
    print(ctx)
    return render(request, "public/modmail.html", ctx)