from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^superuser/', admin.site.urls),
    url(r'^', include('public.urls')),
]
