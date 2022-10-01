from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Interest)

admin.site.register(LanguageSkills)
admin.site.register(Experience)
# admin.site.register(Reference)
# admin.site.register(Document)




admin.site.register(Elementary_School)
admin.site.register(Secondary_School)
admin.site.register(Preparatory_School)

admin.site.register(Edubackground)







class InterviewAdmin(admin.ModelAdmin):
    list_display = ('id','name','start','end','history_userx_f')
    
admin.site.register(Status)
admin.site.register(ApplicationType)
admin.site.register(Exam_Schedule)

class Plan1Admin(admin.ModelAdmin):
    list_display = ('id','Fname','Email','PhoneNo','Nationality','City','DateofBirth','Gender','Name','EmailAdd')

admin.site.register(PersonalInfo, Plan1Admin)
admin.site.register(Interview_Schedule, InterviewAdmin)






class AppAdmin(admin.ModelAdmin):
    list_display = ('id','title','types','starting_date','endingdate')

admin.site.register(Application, AppAdmin)


class HisAdmin(admin.ModelAdmin):
    list_display = ('id','user','application','date','status')

admin.site.register(History, HisAdmin)




















