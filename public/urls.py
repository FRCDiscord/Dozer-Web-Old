from django.conf.urls import url
from .views import logs, basic, api, auth, mail, serverstaff
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'public'

urlpatterns = [

    url(r'^(?P<server_id>[0-9]+)/about/$', basic.about, name='about'),
    url(r'^(?P<server_id>[0-9]+)/rankings/$', basic.rankings, name='rankings'),
    url(r'^(?P<server_id>[0-9]+)/account/$', basic.account, name='account'),
    url(r'^(?P<server_id>[0-9]+)/result/$', basic.result, name='result'),
    url(r'^(?P<server_id>[0-9]+)/$', basic.index, name='index'),
    url(r'^$', basic.dozer_index, name='dozer_index'),

    url(r'^(?P<server_id>[0-9]+)/mod-logs/$', logs.mod_logs, name='logs'),
    url(r'^(?P<server_id>[0-9]+)/mod-logs/search/$', logs.search_logs, name='logs_search'),

    url(r'^(?P<server_id>[0-9]+)/mod-mail/$', mail.mail, name='mail'),
    url(r'^(?P<server_id>[0-9]+)/mod-mail/send/$', mail.mail_receive, name='mail_receive'),

    url(r'^(?P<server_id>[0-9]+)/staff/mail_update$', serverstaff.staff_mail_update, name='staff_mail_update'),
    url(r'^(?P<server_id>[0-9]+)/staff/$', serverstaff.staff_index, name='staff_index'),

    url(r'^(?P<server_id>[0-9]+)/log-in/$', auth.login_or_register, name='login'),
    url(r'^(?P<server_id>[0-9]+)/log-out/$', auth.logout_view, name='logout'),
    url(r'^discord-auth/$', auth.discord, name='discord_auth'),


    url(r'^api/logs/get/$', api.get_logs, name='get_log'),
    url(r'^api/logs/add/$', api.create_log, name='log_create')
]

#urlpatterns += staticfiles_urlpatterns()

