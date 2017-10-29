from django.conf.urls import url
from .views import logs, basic, api

app_name = 'public'

urlpatterns = [
    url(r'^about/$', basic.about, name='about'),
    url(r'^rankings/$', basic.rankings, name='rankings'),
    url(r'^mod-logs/search/$', logs.search_logs, name='logs_search'),
    url(r'^mod-logs/$', logs.mod_logs, name='logs'),
    url(r'^api/logs/get/$', api.get_logs, name='get_log'),
    url(r'^api/logs/add/$', api.create_log, name='log_create'),
    url(r'^$', basic.index, name='index')
]