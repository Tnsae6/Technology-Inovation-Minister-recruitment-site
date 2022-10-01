from django.urls import path, include
from django.views.static import serve 
from .views import *
from  recruit.views import *

from django.conf.urls import url


urlpatterns = [
    
    
# path('apply/', apply, name="apply_url"),
# path('login/', loginPage, name="login"),  
path('apply/',applys, name="apply_url"),
path('profiles/',dash, name="dash_url"),
path('',Homepage, name="homex_url"),
path('da/',dashx, name="dashx_url"),

path('user_profile/',edit_user, name="edit_user_url"),
path('applye/<idm>/',editform, name="applye_url"),
path('apply/<kena>/<joly>/',detail, name="detail_url"),
path('appjob/<id>/',applyjob, name="job_url"),

path('applist/<id>/',appList, name="list_url"),

path('appdetail/<idx>/',appDetail, name="detail_url2"),
path('adminR/', dashbored, name="admin_url2"),
path('new/',newx, name="new"),

path('upload/', uploadimage, name = "upload_url" ),

path('application/', application_list, name = "app_list"),
path('applied/', applied_application, name = "status_list"),


path('detailx/<id>/<ida>/',detail_app, name = "detail_url"),

path('detailxy/<id>/<ida>/',detailx_app, name = "detailx_url"),

path('update_education/', education, name = "edu_url"),
path('update_experiance/', experiance, name = "exp_url"),
path('update_language/', language, name = "lan_url"),
path('pdf_view/<id>/', viewpdf, name = "pdf_url"),

path('error/<id>/',error_hand, name = "error_url"),

# this 3 (active_exam, closed , pending ) url are for activating the exam status of specfic application 
path('active/',exam_active, name = "active_url"),
path('active1/',exam_active1, name = "active_url1"),
path('active2/',exam_active2, name = "active_url2"),

# this 3 (passed_for_interview , failed_interview, pending ,) url are for activating the interview  status of specfic application 
path('activexy/',interview_active, name = "interview_url"),
path('activex1/',interview_active1, name = "interview_url1"),
path('activex2/',interview_active2, name = "interview_url2"),


path('interview/<id>/', pass_exam, name = "pass_with_grade_url"),

path('schedule/<id>/', exam_schedule, name="exam_schedule_url"),
path('schedule&interview/<id>/', interview_scheduler, name="interviewx_schedule_url"),


# activating  exam for all users  url 
path('exam_a/<id>/', exam_active_all, name="exam_active_url"),
path('exam_d/<id>/', exam_deactive_all, name="exam_deactive_url"),



# all applicant that has failed the screnning process 
path('exa_not_fail/<id>/', notfiy_failed_all, name="notfiy_failed_url"),


# all applicant that has failed the exam 
path('exam_not_fail/<id>/', notfiy_failed_exams, name="notfiy_failed_exam_url"),

#this url is for the link to notficaion or message 
path('exam_fail/<str:idm>/<id>/',notfiy_failed_m_all, name="notficaton_url"),

path('exam_date/<str:idm>/<id>/', notfiy_exam, name="exam_date_url"),

# detail view after the click of the notfication of interview scheduling 
path('exam_datex/<str:idm>/<id>/', notfiy_interviewx, name="interviewx_date_url"),

#interview_scheduler
path('admin/', admin_dash, name="adminR"),
    # viewdetailadminR



path('sc_add/<id>/', add_schedule, name = "schedule_now_url"),

path('calendar/<id>/', calendar, name='calendar'),

url('^add_event$', add_event, name='add_event'),
url('^update$', update, name='update'),
url('^remove', remove, name='remove'),
  
path('create_post/', create_post, name='create'),
    

]

