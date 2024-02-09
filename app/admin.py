from django.contrib import admin
from .models import ToDo, Status


admin.site.register(ToDo)
admin.site.register(Status)