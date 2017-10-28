from django.conf.urls import url
from .views import logs, basic

app_name = 'public'

urlpatterns = [
    url(r'^about/$', basic.about, name='about'),
    url(r'^mod-logs/search/$', logs.search_logs, name='logs_search'),
    url(r'^mod-logs/$', logs.mod_logs, name='logs'),
    url(r'^api/logs/add/$', logs.create_log, name='log_create'),
    url(r'^$', basic.index, name='index')
]