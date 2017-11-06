from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from public.models import Log, Server, Member

PAGE_LENGTH = 10

@csrf_exempt
def mod_logs(request, server_id):
    data = request.GET
    user = None
    staff = None
    if 'user' in data:
        try:
            user = Member.objects.get(id=data['user'])
        except:
            pass

    if 'staff' in data:
        try:
            staff = Member.objects.get(id=data['staff'])
        except:
            pass
    return render(request, "public/logs.html", {
        "logs": Log.objects.all(),
        "user": user,
        "staff": staff,
        "server": Server.get(server_id)
    })

@csrf_exempt
def search_logs(request, server_id):
    if request.method == 'GET':
        return JsonResponse({
            "error": "This is used via POST only."
        })
    else:
        data = request.POST
        q = Q(server__id = server_id)
        if 'punished_user' in data:
            q = Q(punished__username = data['punished_user'])

        if 'staff_user' in data:
            s = Q()
            s |= Q(staff__username = data['staff_user'])
            s |= Q(staff__name=data['staff_user'])
            q &= s

        logs = None
        if not bool(data['reverse']):
            logs = Log.objects.filter(q).order_by('actionTime')
        else:
            logs = Log.objects.filter(q).order_by('actionTime').reverse()

        pages = []
        index = 0
        currentPage = []
        for realIndex, log in enumerate(logs):
            currentPage.append(log)
            index += 1
            realIndex += 1
            if index == PAGE_LENGTH or realIndex == len(logs):
                pages.append(render_to_string("public/partial/logs_table.html",
                                              context=
                                              {
                                                  "logs": currentPage
                                              }, request=request))
                currentPage = []
                index = 0

        if len(pages) == 0:
            pages.append(render_to_string("public/partial/logs_table.html",
                                          context={}, request=request))

        pageNumArray = []
        index = 1
        for page in pages:
            pageNumArray.append(index)
            index += 1


        return JsonResponse({
            "pageCount": len(pages),
            "pages": pages,
            "page_nav": render_to_string("public/partial/logs_pages.html",
                                             {
                                                "pages": pageNumArray
                                             }, request)
        })