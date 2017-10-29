from django.shortcuts import render, redirect
from ..models import Member
import requests

def mail(request):
    data = request.GET
    prefill_name = ""
    name_class_add = ""
    prefill_subject = ""
    subject_class_add = ""
    appeal = False
    try:
        member = Member.objects.get(account=request.user, verified=True)
        prefill_name = member.username
        name_class_add = "disabled"
    except:
        member = None

    if 'subject' in data:
        prefill_subject = data['subject']
        subject_class_add = "disabled"

    if 'appeal' in data and request.user.is_authenticated and member:
        appeal = bool(data['appeal'])

    return render(request, "public/modmail.html", {
        "member": member,
        "prefill_name": prefill_name,
        "name_class_add": name_class_add,
        "prefill_subject": prefill_subject,
        "subject_class_add": subject_class_add,
        "appeal": appeal
    })