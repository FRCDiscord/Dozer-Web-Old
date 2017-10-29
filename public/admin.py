from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Punishment)
admin.site.register(Member)
admin.site.register(Log)
admin.site.register(APIToken)