from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..models import Member, Log, Server, Mail, UserInfo

def mail(request, server_id):
    data = request.GET
    prefill_name = ""
    name_class_add = ""
    prefill_subject = ""
    subject_class_add = ""
    appeal = None
    try:
        member = Member.getMember(user=request.user,server=Server.get(server_id))
        prefill_name = member.username
        name_class_add = "readonly"
    except:
        member = None

    if 'appeal' in data and request.user.is_authenticated and member:
        try:
            appeal = Log.objects.get(id=data['appeal'])
            prefill_subject = appeal.appeal_subject()
            subject_class_add = "readonly"
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
        "error": error,
        "server": Server.get(server_id)
    }
    return render(request, "public/modmail.html", ctx)

def mail_receive(request, server_id):
    if request.method == 'POST':
        server = Server.get(server_id)
        data = request.POST
        sender=data['sender']
        user = None
        if request.user.is_authenticated:
            user = UserInfo.get(request.user)
            sender = user.display()
        mail = Mail(sender=sender,
                    subject=data['subject'],
                    content=data['content'],
                    user=user,
                    server=server)
        type = data['type']
        if type == "appeal":
            mail.appeal = Log.objects.get(id=data['appeal_id'], server=server)
        mail.save()
        # TODO: toast/notification of success
        return redirect("public:mail", server_id)
    else:
        return JsonResponse({
            "error": "This is used via POST."
        })