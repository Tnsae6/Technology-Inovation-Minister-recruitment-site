from django.contrib import admin
from .models import *








class NameAdmin(admin.ModelAdmin):
    list_display = ('name','website','location')

admin.site.register(Organization, NameAdmin)


# Register your models here.
