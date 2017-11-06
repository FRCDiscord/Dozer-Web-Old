from django.conf.urls import url
from .views import logs, basic, api, auth, mail

app_name = 'public'

urlpatterns = [

    # TODO: make all of these take a server ID "(?P<server_id>[0-9]+)"
    url(r'^about/$', basic.about, name='about'),
    url(r'^rankings/$', basic.rankings, name='rankings'),
    url(r'^account/$', basic.account, name='account'),
    url(r'^(?P<server_id>[0-9]+)/$', basic.index, name='index'),

    url(r'^log-in/$', auth.login_or_register, name='login'),
    url(r'^log-out/$', auth.logout_view, name='logout'),
    url(r'^discord-auth/$', auth.discord, name='discord_auth'),
    #url(r'^discord-exchange/$', auth.discord, name='discord_exchange'),

    url(r'^mod-logs/$', logs.mod_logs, name='logs'),
    url(r'^mod-logs/search/$', logs.search_logs, name='logs_search'),

    url(r'^mod-mail/$', mail.mail, name='mail'),



    url(r'^api/logs/get/$', api.get_logs, name='get_log'),
    url(r'^api/logs/add/$', api.create_log, name='log_create')
]