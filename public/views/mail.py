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

    if appeal and not appeal.can_appeal():
        return redirect("public:index")

    error = None
    if appeal and not appeal.should_appeal():
        error = "You are trying to appeal this punishment before the appointed time frame. You can still try, but this isn't recommended."

    ctx = {
        "member": member,
        "prefill_name": prefill_name,
        "name_class_add": name_class_add,
        "prefill_subject": prefill_subject,
        "subject_class_add": subject_class_add,
        "appeal": appeal,
        "error": error
    }
    return render(request, "public/modmail.html", ctx)