from django.conf.urls import url
from .views import logs, basic, api, auth, mail

app_name = 'public'

urlpatterns = [

    # TODO: make all of these take a server ID "(?P<server_id>[0-9]+)"
    url(r'^(?P<server_id>[0-9]+)/about/$', basic.about, name='about'),
    url(r'^(?P<server_id>[0-9]+)/rankings/$', basic.rankings, name='rankings'),
    url(r'^(?P<server_id>[0-9]+)/account/$', basic.account, name='account'),
    url(r'^(?P<server_id>[0-9]+)/$', basic.index, name='index'),
    url(r'^$', basic.dozer_index, name='dozer_index'),

    url(r'^(?P<server_id>[0-9]+)/mod-logs/$', logs.mod_logs, name='logs'),
    url(r'^(?P<server_id>[0-9]+)/mod-logs/search/$', logs.search_logs, name='logs_search'),

    url(r'^(?P<server_id>[0-9]+)/mod-mail/$', mail.mail, name='mail'),

    url(r'^(?P<server_id>[0-9]+)/log-in/$', auth.login_or_register, name='login'),
    url(r'^(?P<server_id>[0-9]+)/log-out/$', auth.logout_view, name='logout'),
    url(r'^discord-auth/$', auth.discord, name='discord_auth'),


    url(r'^api/logs/get/$', api.get_logs, name='get_log'),
    url(r'^api/logs/add/$', api.create_log, name='log_create')
]