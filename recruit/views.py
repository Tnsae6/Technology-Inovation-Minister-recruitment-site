from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from . models import *
from .forms import  *
from django.shortcuts import render,get_object_or_404
from core.models import Profile
from core.decorators import unauthenticated_user
import datetime
from datetime import timedelta
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
# from xhtml2pdf import pisa

import datetime
import datetime
from dateutil.relativedelta import relativedelta
from django.urls import reverse
from quiz.models import Sitting,Quiz
from notifications.signals import notify
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mass_mail
from email import message
from django.template.loader import render_to_string
from django.core import mail
from django.utils import timezone
from notifications.models import *
from django.http import JsonResponse
from organization.models import *
from background_task import background



def Homepage(request):
    CHOICE = (('male', 'Male'),
              ('female', 'Female'))

    users = PersonalInfo.objects.all().count()
    apps = Application.objects.all().count()
    male_count = PersonalInfo.objects.filter( Gender=CHOICE[0][0]).count()
    female_count = PersonalInfo.objects.filter( Gender=CHOICE[1][0]).count()
    
                                                            


    

    return render(request, 'homepage.html', {'male_count':male_count,'male_count':male_count,'apps':apps})



def error_404_view(request, exception):
    return render(request,'404.html')

# def handler404(request, *args, **argv):
#     response = render_to_response('404.html', {},
#                                   context_instance=RequestContext(request))
#     response.status_code = 404
#     return response


# def handler500(request, *args, **argv):
#     response = render_to_response('404.html', {},
#                        applyjob           context_instance=RequestContext(request))
#     response.status_code = 500
#     return response


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None



def get_userprofile(user):
    qs = Profile.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    
    else:
        
     return HttpResponse("there is no author passed for the function")


def get_profile(user):

    qs = PersonalInfo.objects.filter(userx = user.id)
    if qs.exists():
        return qs[0]
    
    else:
        
     return HttpResponse("there is no author passed for the function ")  


@login_required
def applys(request):




    if request.user.is_staff: 
    
            return redirect('adminR')
    
      
    elif request.user.is_authenticated and PersonalInfo.objects.filter(userx=request.user.id) .exists() == False:
        template_name = 'application.html'
        perform = personalInfoForm(request.GET or None, prefix="form1" )
        eduformset = EdubackgroundModelFormFormset(request.GET or None, prefix="form2" , )
        lanformset = LanguageSkillsModelFormFormset(request.GET or None, prefix="form3" )
        expformset = ExperienceModelFormFormset(request.GET or None, prefix="form4") 
         
        elementary = Elementary_SchoolForm(request.GET or None, prefix="form6" )
        secondary   = Secondary_SchoolForm(request.GET or None, prefix="form7" )
        preparatory =  Preparatory_SchoolForm(request.GET or None, prefix="form8" )      
    
        # print(eduformset.errors)
        # print(eduformset.errors)
    
    
       
        print(request.session.get('form_data') );
        
        if request.method == 'POST':
            
            perform = personalInfoForm(request.POST,  request.FILES, prefix="form1",initial=request.session.get('form_data') )
            eduformset = EdubackgroundModelFormFormset(request.POST , prefix="form2",initial=request.session.get('form_data')  )
            lanformset = LanguageSkillsModelFormFormset(request.POST , prefix="form3")
            expformset = ExperienceModelFormFormset(request.POST, prefix="form4")
    
            elementary = Elementary_SchoolForm(request.POST, prefix="form6" )
            secondary   = Secondary_SchoolForm(request.POST,prefix="form7" )
            preparatory =  Preparatory_SchoolForm (request.POST,prefix="form8" )  
            
            
            
         
            context = {
                            'perform': perform,
            'eduset':eduformset,
            'lanset':lanformset,
            'expset':expformset,
            'elementary':elementary,
            'secondary':secondary,
            'preparatory':preparatory,
            }
    
    
            # bookform = BookModelForm(request.POST)
            # formset = AuthorFormset(request.POST)
            print("hello")
            if perform.is_valid() and eduformset.is_valid() and lanformset.is_valid()  and elementary.is_valid() and  secondary.is_valid()and preparatory.is_valid()  :
 
                i = 0;
                for form in eduformset:
                        fromx = request.POST.get('form2-'+str(i)+'-From')
                        tox = request.POST.get('form2-'+str(i)+'-To')
                        gpax =  request.POST.get('form2-'+str(i)+'-cumulative_gpa')
                        datex  = datetime.datetime.strptime(fromx, "%Y-%m-%d").date()
                        datey  = datetime.datetime.strptime(tox, "%Y-%m-%d").date()                
                        CurrentDate = datetime.datetime.now()
                        i= i+1;
                        if(fromx > tox or datey  > (CurrentDate.date()+ relativedelta(years=1))  or datex > (CurrentDate.date() + relativedelta(years=1)) ):
                        
                                messages.success(request, 'the Date you Entered Is Invalid.',extra_tags="register")
                                # redirect(reverse('dash_url', context,))
                                return redirect('apply_url')
                        
                                
               
                # first save this personal_info, as its reference will be used in `education`,`language`,`experiance`
                # return HttpResponse(perform.error)
                

                userf = get_userprofile(request.user)
                perform.instance.userx = userf
                info = perform.save()
                # perform.instance.userx = userf
                # userp = get_profile(request.user)
                print(request.user.id)
                # userp = PersonalInfo.objects.filter(userx = request.user.id)
                userp = PersonalInfo.objects.get(userx = request.user.id)
                print(userp)           
                elementary.instance.pinfoe = userp
                elem = elementary.save()
                
                secondary.instance.pinfos = userp
                sec = secondary.save()
                   
                preparatory.instance.pinfop = userp
                pre = preparatory.save()            
    
              
                for form in eduformset:
                    
                    # so that `personal info` instance can be attached.
                    edu = form.save(commit=False)
                    edu.edubackground = info
                    edu.save()


                for form2 in lanformset:
                    # so that `personal info` instance can be attached.
                    lan = form2.save(commit=False)
                    lan.languageskills = info
                    lan.save()
                for form3 in expformset:
                    # so that `personal info` instance can be attached.
                    exp = form3.save(commit=False)
                    exp.experience = info
                    exp.save()
                    perform = personalInfoForm()
                    eduformset = EdubackgroundModelFormFormset()
                    lanformset = LanguageSkillsModelFormFormset()
                    expformset = ExperienceModelFormFormset()

                messages.success(request, 'You have Created Your Profile Sucessfully ',extra_tags="register")
                return redirect('dash_url', )
            else:
                print('zera')
                err = eduformset.errors
                err2 = lanformset.errors
                # err3 = expformset.errors
                err4 = perform.errors
                err5 = elementary.errors
                err6  = secondary.errors
                err7  = preparatory.errors
                # messages.info(request,err )
                # messages.info(request,err2 )
                # messages.info(request,err3 )
                # messages.info(request,err4 )
                # messages.info(request,err5 )
                # messages.info(request,err6 )
                # messages.info(request,err7 )
    
                # return HttpResponse(err)
    
                print( err)
                print( err2)
                # print(err3 )
                print(err4 )
                print(err5 )
                print(err6 )
                print(err7 )
    
    
    
        return render(request, template_name, {
            'perform': perform,
            'eduset':eduformset,
            'lanset':lanformset,
            'expset':expformset,
            'elementary':elementary,
            'secondary':secondary,
            'preparatory':preparatory,
        })
    else:
            return redirect('dash_url')



@login_required
def edit_user(request):
    template_name = 'userinfo.html'

    author = PersonalInfo.objects.filter(id= idm)
    pero = get_object_or_404(PersonalInfo, id=idm)
    # eduo = get_object_or_404(Edubackground, edubackground=pero)
    eduo = Edubackground.objects.filter(edubackground=pero)
    # lana = get_object_or_404(LanguageSkills, languageskills=pero)
    lano = LanguageSkills.objects.filter(languageskills=pero)
    # expa = get_object_or_404(Experience, experience=pero)
    expo = Experience.objects.filter(experience=pero)


    
    perform = personalInfoForm(request.GET or None, prefix="form1"  )
    eduformset = EdubackgroundModelFormFormset(request.GET or None, prefix="form2"  )
    lanformset = LanguageSkillsModelFormFormset(request.GET or None, prefix="form3" )
    expformset = ExperienceModelFormFormset(request.GET or None, prefix="form4")        

    if request.method == 'POST':
        
        perform = personalInfoForm(request.POST, prefix="form1")
        eduformset = EdubackgroundModelFormFormset(request.POST , prefix="form2" )
        lanformset = LanguageSkillsModelFormFormset(request.POST , prefix="form3")
        expformset = ExperienceModelFormFormset(request.POST, prefix="form4")


        if perform.is_valid() and eduformset.is_valid() and lanformset.is_valid() and expformset.is_valid():
            # first save this personal_info, as its reference will be used in `education`,`language`,`experiance`
     
            userf = get_userprofile(request.user)
            perform.instance.userx = userf
            info = perform.save()
            for form in eduformset:

                
                # so that `personal info` instance can be attached.
                edu = form.save(commit=False)

                edu.edubackground = info
                
                edu.save()
            for form2 in lanformset:
                # so that `personal info` instance can be attached.
                lan = form2.save(commit=False)
                lan.languageskills = info
                lan.save()
            for form3 in expformset:
                # so that `personal info` instance can be attached.
                exp = form3.save(commit=False)
                exp.experience = info
                exp.save()
                perform = personalInfoForm()
                eduformset = EdubackgroundModelFormFormset()
                lanformset = LanguageSkillsModelFormFormset()
                expformset = ExperienceModelFormFormset()

            return redirect('dash_url')
        else:
            print('zera')
            err = eduformset.errors
            err2 = lanformset.errors
            err3 = expformset.errors
            err4 = perform.errors
            messages.info(request,err )
            messages.info(request,err2 )
            messages.info(request,err3 )
            messages.info(request,err4 )

            # return HttpResponse(err)

            print(  err)
            print( err2)
            print(err3 )
            print(err4 )
            # return HttpResponse(err2)
            # return HttpResponse(err3)

    return render(request, template_name, {
        'perform': perform,
        'eduset':eduformset,
        'lanset':lanformset,
        'expset':expformset,
    })

 




 
@login_required
def editform(request,idm):
    
    author = PersonalInfo.objects.filter(id= idm)
    pero = get_object_or_404(PersonalInfo, id=idm)
    # eduo = get_object_or_404(Edubackground, edubackground=pero)
    eduo = Edubackground.objects.filter(edubackground=pero)
    # lana = get_object_or_404(LanguageSkills, languageskills=pero)
    lano = LanguageSkills.objects.filter(languageskills=pero)
    # expa = get_object_or_404(Experience, experience=pero)
    expo = Experience.objects.filter(experience=pero)
    

    perform = personalInfoForm(request.GET or None, prefix="form1", instance=pero  )
    eduformset = EdubackgroundModelFormFormset(request.GET or None, prefix="form2" , instance = pero )
    
    lanformset = LanguageSkillsModelFormFormset(request.GET or None, prefix="form3", instance = pero)
    expformset = ExperienceModelFormFormset(request.GET or None, prefix="form4", instance = pero)        

    print(eduformset.errors)

    template_name = 'applicationedit.html'
   

    print('zera')
    if request.method == 'POST':
        
        perform = personalInfoForm(request.POST, prefix="form1", instance=pero,)
        eduformset = EdubackgroundModelFormFormset(request.POST , prefix="form2" , instance = pero)
        
        lanformset = LanguageSkillsModelFormFormset(request.POST or None, prefix="form3",instance = pero)
        expformset = ExperienceModelFormFormset(request.POST or None, prefix="form4",instance = pero)
     

       
        if perform.is_valid() and eduformset.is_valid() and lanformset.is_valid() and  expformset.is_valid() :

            print('zera')
           
            # instance = PersonalInfo.objects.get(id=idm)
            # instance.delete()              

            # first save this personal_info, as its reference will be used in `education`,`language`,`experiance`
            info = perform.save()
            for form in eduformset:
                # so that `personal info` instance can be attached.
                edu = form.save(commit=False)
                edu.edubackground = info
                
                edu.save()
            for form2 in lanformset:
                # so that `personal info` instance can be attached.
                lan = form2.save(commit=False)
                lan.languageskills = info
                lan.save()
            for form3 in expformset:
                # so that `personal info` instance can be attached.
                exp = form3.save(commit=False)
                exp.experience = info
                exp.save()
                # perform = personalInfoForm()
                # eduformset = EdubackgroundModelFormFormset()
                # lanformset = LanguageSkillsModelFormFormset()
                # expformset = ExperienceModelFormFormset()
        else:
            err = expformset.errors
            return HttpResponse(err)
            # return redirect('list_url')
            # return redirect('list_url')
    return render(request, template_name, {
        'perform': perform,
        'eduset':eduformset,
        'lanset':lanformset,
        'expset':expformset,

        'pinfo':pero,
        'eduo':eduo,
        'lano':lano,
        'expo':expo,
    })


@login_required
@unauthenticated_user
def dashxx(request):
    profile = get_object_or_404(PersonalInfo, userx_id =request.user.id)
    # applicant = PersonalInfo.objects.all()

    status = History.objects.filter(user = request.user.id )

    ids = History.objects.values_list('application_id', flat=True).filter(user__pk = request.user.id).distinct() 
    applications = Application.objects.exclude(pk__in = set(ids))
    # statusX = History.objects.values()




    now=datetime.date.today()
    # applications = Application.objects.filter(pk = names_to_exclude )

    # applications = Application.objects.all()
    





    return render(request, 'dashbored.html', {'profile':profile,'applications':applications,'status':status})

@login_required
def dashx(request):
    profile = get_object_or_404(PersonalInfo, userx_id =request.user.id)
    # applicant = PersonalInfo.objects.all()

    status = History.objects.filter(user = request.user.id )

    ids = History.objects.values_list('application_id', flat=True).filter(user__pk = request.user.id).distinct() 
    applications = Application.objects.exclude(pk__in = set(ids))
    # statusX = History.objects.values()




    now=datetime.date.today()
    # applications = Application.objects.filter(pk = names_to_exclude )

    # applications = Application.objects.all()
    





    return render(request, 'dashbored.html', {'profile':profile,'applications':applications,'status':status})



def uploadimage(request):


    if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            profile= get_object_or_404(Profile, user = request.user )
            profile.profile_pic  = myfile
            profile.save()
            return redirect('dash_url')
    else:
            return redirect('dash_url')


def error_hand(request, id):


  


    if request.user.is_staff: 

        return redirect('adminR')	

    elif request.user.is_authenticated and PersonalInfo.objects.filter(userx=request.user.id) .exists():


    
        app_list = Application.objects.filter(expired = False)

        perform = personalInfoForm(request.GET or None, prefix="form1"  )
        eduformset = EdubackgroundModelFormFormset(request.GET or None, prefix="form2"  )
        lanformset = LanguageSkillsModelFormFormset(request.GET or None, prefix="form3" )
        expformset = ExperienceModelFormFormset(request.GET or None, prefix="form4") 



        statusx = History.objects.filter(user = request.user.id, application__expired = False )
        profile = get_object_or_404(PersonalInfo, userx_id =request.user.id)
        profilex = get_object_or_404(Profile, user =request.user)
         
        edu = Edubackground.objects.filter(edubackground__userx_id = request.user.id)
        #  edu = get_object_or_404(Edubackground, edubackground__userx_id = request.user.id)
        #  lan = get_object_or_404(LanguageSkills, languageskills__userx_id =request.user.id)
        lan = LanguageSkills.objects.filter( languageskills__userx_id =request.user.id)
        #  exp = get_object_or_404(Experience, experience__userx_id =request.user.id)
        exp = Experience.objects.filter(experience__userx_id =request.user.id)

        status = History.objects.filter(user = request.user.id )
        
        ids = History.objects.values_list('application_id', flat=True).filter(user__pk = request.user.id).distinct() 
        applications = Application.objects.exclude(pk__in = set(ids)) 
        # messages.success(request, "Message sent." )
        messages.success(request, 'You have been logged out!')
        now=datetime.date.today()
        context = {
            'profile':profile,
            'applications':applications,
            'status':status,
            'profilex':profilex,
            'edu':edu, 
            'lan':lan,
            'exp':exp,        
            'eduset':eduformset,
            'lanset':lanformset,
            'expset':expformset,
            'statusx':statusx,
            }
        return render(request, 'profilek.html',context )

    else:
        return redirect('apply_url')



def education(request):
    i = 0
    if request.method == 'POST':

        eduformset = EdubackgroundModelFormFormset(request.POST , prefix="form2" )
        
        if eduformset.is_valid():
            userf = get_userprofile(request.user)

            print(request.user.id)
            # zera = request.Post.get('form2-'+i+'-From')
            
            

          

            userp = PersonalInfo.objects.get(userx = request.user.id)
            print(userp)
            

            
            for form in eduformset:
                # so that `personal info` instance can be attached.
                fromx = request.POST.get('form2-'+str(i)+'-From')
                tox = request.POST.get('form2-'+str(i)+'-To')
                gpax =  request.POST.get('form2-'+str(i)+'-cumulative_gpa')
                datex  = datetime.datetime.strptime(fromx, "%Y-%m-%d").date()
                datey  = datetime.datetime.strptime(tox, "%Y-%m-%d").date()                
                CurrentDate = datetime.datetime.now()
            
                print(datex > CurrentDate.date())
                # print(form)
                
                # print(int(fromx)-int(tox))
                if(fromx > tox or datey  > (CurrentDate.date()+ relativedelta(years=1))  or datex > (CurrentDate.date() + relativedelta(years=1)) ):

                    messages.success(request, 'the Date you Entered Is Invalid.',extra_tags="register")
                    return redirect('dash_url')
                    
                # if(float(gpax) > 4):
                #     messages.success(request, 'the GPA YOU Entered Is Invalid.',extra_tags="register")
                #     return redirect('dash_url')
                else:
                    print('not work')
                    edu = form.save(commit=False)
                    edu.edubackground = userp
                    edu.save()
                messages.success(request, 'Educaton Submitted',extra_tags="register")
                return redirect('dash_url')
        else:
            return redirect('dash_url')
    else:
        return redirect('dash_url')



def experiance(request):
    i = 0
    
    if request.method == 'POST':

        expformset = ExperienceModelFormFormset(request.POST, prefix="form4")
        if expformset.is_valid():
            userf = get_userprofile(request.user)

            print(request.user.id)

            userp = PersonalInfo.objects.get(userx = request.user.id)
            print(userp)                        
            for form3 in expformset:

                start = request.POST.get('form4-'+str(i)+'-Start')
                end = request.POST.get('form4-'+str(i)+'-End')


                # gpax =  request.POST.get('form2-'+str(i)+'-cumulative_gpa')
                datex  = datetime.datetime.strptime(start, "%Y-%m-%d").date()
                datey  = datetime.datetime.strptime(end, "%Y-%m-%d").date()    

                CurrentDate = datetime.datetime.now()
                
                if(datex > datey or datey  > (CurrentDate.date()+ relativedelta(years=1))  or datex > (CurrentDate.date() + relativedelta(years=1)) ):
                    
                    messages.success(request, 'the Date you Entered Is Invalid.',extra_tags="register")
                    return redirect('dash_url')
                else:
                    exp = form3.save(commit=False)
                    exp.experience = userp
                    exp.save()
                    messages.success(request, 'Experiance Submitted',extra_tags="register")
                    return redirect('dash_url')
        else:
            return redirect('dash_url')
    else:
        return redirect('dash_url')
        


def language(request):
    
    if request.method == 'POST':

        lanformset = LanguageSkillsModelFormFormset(request.POST , prefix="form3")
        if  lanformset.is_valid():
            userf = get_userprofile(request.user)

            print(request.user.id)

            userp = PersonalInfo.objects.get(userx = request.user.id)
            print(userp)                        
            for form2 in lanformset:
                # so that `personal info` instance can be attached.
                lan = form2.save(commit=False)
                lan.languageskills = userp
                lan.save()
                messages.success(request, 'language Skill Submitted',extra_tags="register")
                return redirect('dash_url')
        else:
            return redirect('dash_url')
    else:
        return redirect('dash_url')


@login_required
def dash(request):


    if request.user.is_staff: 

        return redirect('adminR')	

    elif request.user.is_authenticated and PersonalInfo.objects.filter(userx=request.user.id) .exists():


    
        app_list = Application.objects.filter(expired = False)

        perform = personalInfoForm(request.GET or None, prefix="form1"  )
        eduformset = EdubackgroundModelFormFormset(request.GET or None, prefix="form2"  )
        lanformset = LanguageSkillsModelFormFormset(request.GET or None, prefix="form3" )
        expformset = ExperienceModelFormFormset(request.GET or None, prefix="form4") 



        statusx = History.objects.filter(user = request.user.id, application__expired = False )
        print(statusx)
        profile = get_object_or_404(PersonalInfo, userx_id =request.user.id)
        profilex = get_object_or_404(Profile, user =request.user)
         
        edu = Edubackground.objects.filter(edubackground__userx_id = request.user.id)
        #  edu = get_object_or_404(Edubackground, edubackground__userx_id = request.user.id)
        #  lan = get_object_or_404(LanguageSkills, languageskills__userx_id =request.user.id)
        lan = LanguageSkills.objects.filter( languageskills__userx_id =request.user.id)
        #  exp = get_object_or_404(Experience, experience__userx_id =request.user.id)
        exp = Experience.objects.filter(experience__userx_id =request.user.id).exclude(Company__isnull=True )
 
        status = History.objects.filter(user = request.user.id )
        
        ids = History.objects.values_list('application_id', flat=True).filter(user__pk = request.user.id).distinct() 
        applications = Application.objects.exclude(pk__in = set(ids)) 
        now=datetime.date.today()
        
        context = {
            'profile':profile,
            'applications':applications,
            'status':status,
            'profilex':profilex,
            'edu':edu, 
            'lan':lan,
            'exp':exp,        
            'eduset':eduformset,
            'lanset':lanformset,
            'expset':expformset,
            'statusx':statusx,
            }
        return render(request, 'profilek.html',context )

    else:
        return redirect('apply_url')



@login_required
def applyjob(request, id):

    apps = get_object_or_404(Application, id=id)
    profile = get_object_or_404(Profile, id=request.user.id)
    profilex = get_object_or_404(PersonalInfo, userx_id =request.user.id)
    his = History.objects.filter(user = request.user.id ,application = id )
    if apps.endingdate > timezone.now().date() and his.exists() :
       # return HttpResponse('YOU HAVE ALREADY APPLIED FOR THE JOB OR THE APPLICATION HAS EXPIRED )
        messages.success(request, 'YOU HAVE ALREADY APPLIED FOR THE JOB OR THE APPLICATION HAS EXPIRED',extra_tags="register")
        return redirect('status_list')



    else:
        article = History()
        article.user = profile
        article.profile = profilex

        article.application  = apps

        article.save()
        messages.success(request,request.user+'Your Job Application is Scucessfull',extra_tags="register")

        return redirect('status_list')

@login_required  
def editform2(request,idm):
    

    pero = get_object_or_404(PersonalInfo, pk=idm)
    # eduo = get_object_or_404(Edubackground, edubackground=pero)
    eduo = Edubackground.objects.filter(edubackground=pero)
    # lana = get_object_or_404(LanguageSkills, languageskills=pero)
    lano = LanguageSkills.objects.filter(languageskills=pero)
    # expa = get_object_or_404(Experience, experience=pero)
    expo = Experience.objects.filter(experience=pero)
    
    perform = personalInfoForm(request.GET or None,request.FILES or None, prefix="form1", instance=pero  )
    eduformset = EdubackgroundModelFormFormset(request.GET or None, prefix="form2" , queryset=Edubackground.objects.filter(edubackground = idm))
    lanformset = LanguageSkillsModelFormFormset(request.GET or None, prefix="form3",queryset=LanguageSkills.objects.filter(languageskills=idm))
    expformset = ExperienceModelFormFormset(request.GET or None, prefix="form4",queryset=Experience.objects.filter(experience=idm))
        



    template_name = 'applicationedit.html'
   

    
    if request.method == 'POST' :
  
        
       

        if perform.is_valid() and eduformset.is_valid() and lanformset.is_valid() and expformset.is_valid():
     
            instance = PersonalInfo.objects.get(id=idm)
            instance.delete()              

            # first save this personal_info, as its reference will be used in `education`,`language`,`experiance`
            info = perform.save()
            for form in eduformset:
                # so that `personal info` instance can be attached.
                edu = form.save(commit=False)
                edu.edubackground = info
                edu.save()
            for form2 in lanformset:
                # so that `personal info` instance can be attached.
                lan = form2.save(commit=False)
                lan.languageskills = info
                lan.save()
            for form3 in expformset:
                # so that `personal info` instance can be attached.
                exp = form3.save(commit=False)
                exp.experience = info
                exp.save()
                # perform = personalInfoForm()
                # eduformset = EdubackgroundModelFormFormset()
                # lanformset = LanguageSkillsModelFormFormset()
                # expformset = ExperienceModelFormFormset()

            return redirect('list_url')
    return render(request, template_name, {
        'perform': perform,
        'eduset':eduformset,
        'lanset':lanformset,
        'expset':expformset,

        'pinfo':pero,
        'eduo':eduo,
        'lano':lano,
        'expo':expo,
    })

def profile(request):

    return render(request,'profile.html')

def reset(request):
    return render(request,'resetpassword.html')



@staff_member_required
def dashbored(request):

    application = ApplicationForm(request.GET or None, prefix="form10")


    apps = Application.objects.all()
    

    if request.method == 'POST':

        application  = ApplicationForm(request.POST, prefix="form10" )
        apps = Application.objects.all()

        if application.is_valid():

                #             userf = get_userprofile(request.user)
                # perform.instance.userx = userf
                
                info = application.save()
                
                messages.success(request, 'You have created application sucessfully !')
                return redirect('admin_url2')
        else:
            
            print(application.errors)
            # application = ApplicationForm(request.GET or None, prefix="form10")
            # messages.success(request, 'there is some eroor on the form!')

            return render(request, 'adash.html', {'apps': apps, 'application': application})


      
      
      


    



    return render(request, 'adash.html', {'apps':apps,'application':application})



def get_score(current_score,question_order):
        dividend = float(self.current_score)
        divisor = len(int(n) for n in question_order.split(',') if n)
        if divisor < 1:
            return 0            # prevent divide by zero error

        if dividend > divisor:
            return 100

        correct = int(round((dividend / divisor) * 100))

        if correct >= 1:
            return correct
        else:
            return 0

# this view enabels us to pass the applicant to the interview process based on seted score 
def pass_exam(request , id):

    EXAM_RESULT = ( 
         ('Pending', 'Pending'), 
        ('Passed For Interview', 'Passed For Interview'),
        ('Failed For Interview', 'Failed For Interview'),   
  

    )

    # update_history = History.objects.filter(History,application_id = id  )
    users_object = Sitting.objects.filter(quiz__applicationc = id )
    # update_history = get_object_or_404(History,user__id = user_object.user.id ,application  = id )
    his_obj = Sitting.objects.values_list('user_id',flat=True).filter(quiz__applicationc = id).distinct() 
    print(his_obj,'zera')

    applications = History.objects.filter(user__in = set(his_obj), application = id )
    print(applications,'zeraxx')

    # for single_user_history in applications:
    #     single_user_history.exam_marks = 

      
    
    for user_single in users_object:

        if  user_single.check_if_passed == True:
           user_single.interview_status = EXAM_RESULT[1][0]
           
           user_single.save()
           if History.objects.filter(user__id = user_single.user.id , application_id = user_single.quiz.applicationc.id).exists():
              his = get_object_or_404(History, user_id = user_single.user.id , application_id = user_single.quiz.applicationc.id )
              his.exam_marks = EXAM_RESULT[1][0]
              his.save()

        if  user_single.check_if_passed == False:
    
            user_single.interview_status = EXAM_RESULT[2][0]
        #    update_history.exam_marks = EXAM_RESULT[2][0]
            user_single.save()
            if History.objects.filter(user__id = user_single.user.id , application_id = user_single.quiz.applicationc.id).exists():
                his = get_object_or_404(History, user_id = user_single.user.id , application_id = user_single.quiz.applicationc.id )
                his.exam_marks = EXAM_RESULT[2][0]
                his.save()
           
    # for user_single in update_history:
    #     user_single.exam_marks = EXAM_RESULT[1][0]
    #     user_single.save()



        
    return redirect('list_url', id )

# this virew enabels us to send both email and notifcation to the user that the exam date is schedueld 
def exam_schedule(request, id ):

    if request.method == 'POST':
        

        exam_form = ExamScheduleForm(request.POST,  prefix="form9")

        app_object= get_object_or_404(Application, id = id)
        print(exam_form)

        if exam_form.is_valid():
            info = exam_form.save()
            print(exam_form.cleaned_data['exam_date'])

            MY_CHOICES = (
                        ('pending', 'Pending'),
                        ('Passed for Exam', 'Passed for Exam'),
                        ('Failed for Exam', 'Failed for Exam'),
                        ('Passed for INTERVIEW ', 'Passed for INTERVIEW '),
                        ('Failed for INTERVIEW ', 'Failed for INTERVIEW'),
                        ('INTERVIEW PASSED', 'INTERVIEW PASSED'),
                        ('INTERVIEW FAILED', 'INTERVIEW FAILED'),)
            exam_ready1 = History.objects.filter(application = id ,status  = MY_CHOICES[1][0],exam_date_notified = False)

            for exam_ready_single  in exam_ready1:
                idm = exam_ready_single.id
                user = exam_ready_single.profile.Fname
                postion = exam_ready_single.application.title
                passed_user =User.objects.filter(id=exam_ready_single.user.user.id)
                url = 'exam_date_url'
                notify.send(sender=request.user, recipient=passed_user,
                            verb='Your Exam Is schedule pls click to view details ', description=url , target = exam_ready_single )
                exam_ready_single.exam_date_notified = True
                exam_ready_single.save()




            exam_ready = History.objects.filter(application = id ,status  = MY_CHOICES[1][0],exam_date_notified_email = False)
            for exam_ready_single  in exam_ready:
                idm = exam_ready_single.id
                user = exam_ready_single.profile.Fname
                postion = exam_ready_single.application.title
                subject = 'Techin Notifcation'
                location = exam_form.cleaned_data['exam_location']
                date_of_interview = exam_form.cleaned_data['exam_date']
                time_of_interview = exam_form.cleaned_data['exam_time']
                google_map_link = exam_form.cleaned_data['google_map_link']
                message = render_to_string('emails/exam_date_notify.html', {
                    'postion':postion,
                    'user':user,
                    'location':location,
                    'date':date_of_interview,
                    'time':time_of_interview,
                    'map':google_map_link
                    })
                user_email = exam_ready_single.user.user.email
                
                failed_user =User.objects.filter(id=exam_ready_single.user.user.id)
                to_email = user_email
                sender = 'techinethiopia@gmail.com'
                plain_message = strip_tags(message)
            
                mail.send_mail(subject, plain_message, sender,
	                               [to_email], html_message=message)
                message = EmailMultiAlternatives(subject, plain_message, sender, [to_email])
                exam_ready_single.exam_date_notified_email = True
                exam_ready_single.save()
                
                
                # notify.send(sender=request.user, recipient=failed_user,
                #             verb='Your Exam Is schedule pls click to view details ', description=url , target = exam_ready_single )
                # exam_ready_single.exam_date_notified = True
                # exam_ready_single.save()
            return redirect('list_url', id)

        else:
            
            return redirect('list_url', id) 
    else:
        
        return redirect('list_url', id)



# this virew enabels us to send both email and notifcation to the user that the exam date is schedueld 
def interview_scheduler(request, id ):


        EXAM_RESULT = ( 
             ('Pending', 'Pending'), 
            ('Passed For Interview', 'Passed For Interview'),
            ('Failed For Interview', 'Failed For Interview'),   )  


        exam_ready1 = Interview_Schedule.objects.filter(application_f = id, history_userx_f__Interivew_date_notified = False  )
          
       # exam_readyx = History.objects.filter(application = id ,status  = MY_CHOICES[1][0],exam_date_notified = False)

        for exam_ready_single  in exam_ready1:
            idm = exam_ready_single.history_userx_f.id
            user = exam_ready_single.history_userx_f.profile.Fname
            postion = exam_ready_single.history_userx_f.application.title
            passed_user =User.objects.filter(id=exam_ready_single.history_userx_f.user.user.id)
            url = 'interviewx_date_url'
            notify.send(sender=request.user, recipient=passed_user,
                        verb='Your Interview Date Is schedule, click to view details ', description=url , target = exam_ready_single )
            exam_ready_single.save()
            exam_ready_single.history_userx_f.Interivew_date_notified = True
            
       # exam_readyxy = History.objects.filter(application = id ,status  = MY_CHOICES[1][0],exam_date_notified_email = False)
        exam_ready = Interview_Schedule.objects.filter(application_f = id, history_userx_f__Interivew_date_notified_email = False  )

        info = Organization.objects.all().first()
   
        for exam_ready_single  in exam_ready:
            formatedDate = exam_ready_single.start.strftime("%H:%M")
            formatedDate1 = exam_ready_single.end.strftime("%H:%M")

            idm = exam_ready_single.history_userx_f.id
            user = exam_ready_single.history_userx_f.profile.Fname
            postion = exam_ready_single.history_userx_f.application.title
            subject =  str(info.name+'Notifcation')
            location = info.location
            date_of_interview = exam_ready_single.start.strftime("%Y-%m-%d ")
            time_of_interview = str(formatedDate)+"-"+str(formatedDate1)
            google_map_link = info.googlemap_link
            message = render_to_string('emails/interview_date_notify.html', {
                'postion':postion,
                'user':user,
                'location':location,
                'date':date_of_interview,
                'time':time_of_interview,
                'map':google_map_link
                })
            user_email = exam_ready_single.history_userx_f.user.user.email
            
            # failed_user =User.objects.filter(id=exam_ready_single.user.user.id)
            to_email = user_email
            sender = 'techinethiopia@gmail.com'
            plain_message = strip_tags(message)
        
            mail.send_mail(subject, plain_message, sender,
	                           [to_email], html_message=message)
            message = EmailMultiAlternatives(subject, plain_message, sender, [to_email])            
            exam_ready_single.save()
            exam_ready_single.exam_date_notified_email = True
           
                
                # notify.send(sender=request.user, recipient=failed_user,
                #             verb='Your Exam Is schedule pls click to view details ', description=url , target = exam_ready_single )
                # exam_ready_single.exam_date_notified = True
                # exam_ready_single.save()
        return redirect('list_url', id)





@staff_member_required
def appList(request , id):
    interview = False
    if Interview_Schedule.objects.all().exists():
        interview = True
    else:
         interview = False
    pased_exam = Sitting.objects.filter(quiz__applicationc = id )
    failed_exam = Sitting.objects.filter(quiz__applicationc = id )
    app_idx = id

    CHOICE = (('male', 'Male'),
              ('female', 'Female'))


    EXAM_RESULT = ( 
         ('Pending', 'Pending'), 
        ('Passed For Interview', 'Passed For Interview'),
        ('Failed For Interview', 'Failed For Interview'),   
  

    )

    MY_CHOICES = ( 
        ('pending', 'Pending'),
        ('Passed for Exam', 'Passed for Exam'), 
        ('Failed for Exam', 'Failed for Exam'),
        ('Passed for INTERVIEW ', 'Passed for INTERVIEW '),
        ('Failed for INTERVIEW ', 'Failed for INTERVIEW'),
        ('INTERVIEW PASSED', 'INTERVIEW PASSED'), 
        ('INTERVIEW FAILED', 'INTERVIEW FAILED'),   

    )

    # EXAM_RESULT = ( 
    #      ('Pending', 'Pending'), 
    #     ('Passed', 'Passed'),
    #     ('Failed', 'Faild'),   
  

    # )
    interview_s = Interview_Schedule.objects.filter()

    if  request.POST:
        print('postxxxxxx')

        zid = request.POST.get('pass1')
        update_pass = get_object_or_404(Quiz, applicationc=id)
        update_pass.pass_mark = int(zid)
        update_pass.save()

        return redirect('list_url', id )


    vote_counts = {}
    pased_exam_no = 0;
    failed_exam_no = 0;
    less_no = 0;

    pased_exam = Sitting.objects.filter(quiz__applicationc = id ,)
    passed_id_list = []
    failed_id_list = []
    for vote in pased_exam:
        
            
        if vote.check_if_passed == True:
            pased_exam_no=pased_exam_no+1;
            passed_id_list.append(vote.user.id)


        if vote.check_if_passed == False:
             failed_exam_no=failed_exam_no+1;
             failed_id_list.append(vote.user.id)

        if vote.get_percent_correct < 50 :
             less_no=less_no+1;             
 
    pased_for_exam_male_count = PersonalInfo.objects.filter(userx__user_id__in=passed_id_list, Gender=CHOICE[0][0]
                                                            ).count()
    pased_for_exam_female_count = PersonalInfo.objects.filter(userx__user_id__in=passed_id_list, Gender=CHOICE[1][0]
                                                            ).count()
    failed_for_exam_male_count = PersonalInfo.objects.filter(userx__user_id__in=failed_id_list, Gender=CHOICE[0][0]
                                                            ).count()
    failed_for_exam_female_count = PersonalInfo.objects.filter(userx__user_id__in=failed_id_list, Gender=CHOICE[1][0]
                                                            ).count()

    passed_for_inter = int(pased_for_exam_female_count) + int(pased_for_exam_male_count)
    print(passed_for_inter)

    print(pased_for_exam_male_count)
    exam_schedule = Exam_Schedule.objects.filter(application_user=id)
    applicant_count = History.objects.filter(application = id).count()
    applicant_female_count = History.objects.filter(application=id, profile__Gender = CHOICE[1][0] ).count()
    applicant_male_count = History.objects.filter(application=id, profile__Gender=CHOICE[0][0]).count()

    exam_ready_count = History.objects.filter(
        application=id, status=MY_CHOICES[1][0]).count()

    exam_failed_count = History.objects.filter(
        application=id, status=MY_CHOICES[2][0]).count()

    exam_ready_female_count = History.objects.filter(
        application=id, status=MY_CHOICES[1][0], profile__Gender=CHOICE[1][0]).count()

    exam_ready_male_count = History.objects.filter(
        application=id, status=MY_CHOICES[1][0], profile__Gender=CHOICE[0][0]).count()

    pased_for_exam = Sitting.objects.filter(quiz__applicationc = id).count()

    # pased_for_exam_male_count = Sitting.objects.filter(quiz__applicationc=id ,user =  ).count()
    # pased_for_exam_female_count = Sitting.objects.filter(
    #     quiz__applicationc=id).count()
    

    zera = request.user.notifications.unread()
    # applicant = PersonalInfo.objects.all()
    # this queryset filters the diffrent status of the applicants based on the chooice felid 
    apps = Application.objects.filter(id = id, )
    pending = History.objects.filter(application = id , status  = MY_CHOICES[0][0] )
    exam_ready = History.objects.filter(application = id ,status  = MY_CHOICES[1][0])
    exam_form = ExamScheduleForm(request.GET or None, prefix="form9")
    
    result_exam = Sitting.objects.filter(quiz__applicationc = id , )
    all_events = Interview_Schedule.objects.all()
    # exam_ready = History.objects.filter(application = id ,status  = MY_CHOICES[1][0])
    passed_for_interview = History.objects.filter(
        application=id, exam_marks=EXAM_RESULT[1][0])

    if Exam_Schedule.objects.filter(application_user=id).exists():
        Exam_Multiple = False
    else:
        Exam_Multiple = True
    

    interview_form = Interview_Schedule_User(request.GET or None, prefix="form12")

    context = {'applicant': pending, 'apps': apps, 'exam_ready': exam_ready, 'result_exam': result_exam, 
              'applicant_count': applicant_count, 'pased_for_exam': pased_for_exam,
               'pased_exam': pased_exam_no, 'failed_exam': failed_exam_no, 'less_no': less_no, 
               'app_idx': app_idx,
            'passed_for_interview': passed_for_interview, 'exam_form': exam_form, 
               'zera': zera, 'exam_Schedule': exam_schedule, 'Exam_Multiple': Exam_Multiple,
               'applicant_female_count': applicant_female_count,
               'applicant_male_count': applicant_male_count,
               'exam_ready_count': exam_ready_count,
               'exam_ready_female_count':exam_ready_female_count,
               'exam_ready_male_count': exam_ready_male_count,
               'exam_failed_count': exam_failed_count,
               'events': all_events,
               'pased_for_exam_male_count': pased_for_exam_male_count,
               'pased_for_exam_female_count': pased_for_exam_male_count,
               'failed_for_exam_male_count': failed_for_exam_male_count,
               'failed_for_exam_female_count': failed_for_exam_female_count,
               'interview_form': interview_form,
               'interview':interview
               }

 


    return render(request,'admin2.html', context)




def exam_deactive_all(request,id):

    MY_CHOICES = (
        ('pending', 'Pending'),
        ('Passed for Exam', 'Passed for Exam'),
        ('Failed for Exam', 'Failed for Exam'),
        ('Passed for INTERVIEW ', 'Passed for INTERVIEW '),
        ('Failed for INTERVIEW ', 'Failed for INTERVIEW'),
        ('INTERVIEW PASSED', 'INTERVIEW PASSED'),
        ('INTERVIEW FAILED', 'INTERVIEW FAILED'),

    )

    EXAM_STATUS = ( 
         ('Dectivate', 'Dectivate'), 
        ('Active', 'Active'),
        ('Closed', 'Closed'),   
  

    )

    exam_ready = History.objects.filter(application = id ,status  = MY_CHOICES[1][0])

    for exam_ready_single  in exam_ready:

        exam_ready_single.exam_status = EXAM_STATUS[0][0]

        exam_ready_single.save()

    return redirect('list_url', id)


def notfiy_failed_m_all(request,idm,id):


    info = get_object_or_404(History, id = int(idm))

    # print(idm)
    # print(notifications.objects.all())
     
    noti_read = Notification.objects.filter(id = id)
    noti_read.mark_all_as_read()


    
    return render(request,'failed_screen.html', {'info' :info,})
    # return render(request, 'admin2.html', context)

    
def notfiy_exam(request,idm,id):


    info = get_object_or_404(History, id= int(idm))


    user = info.profile.Fname
    postion = info.application.title
    subject = 'Techin Notifcation'
    print(info.application.id)
    apps = get_object_or_404(Application, id=info.application.id)

    notice_info = get_object_or_404(Exam_Schedule,
                                    application_user=apps)
    

    location = notice_info.exam_location
    date_of_exam = notice_info.exam_date
    time = notice_info.exam_time
    google_map_link = notice_info.google_map_link
    
    noti_read = Notification.objects.filter(id = id)
    noti_read.mark_all_as_read()



    context =  {'info' :info,
                'postion': postion,
                'date': date_of_exam,
                'location': location,
                'time': time,
                'user': user,
                'map': google_map_link
                
    
    }
 


    
    return render(request,'exam_date_notify.html', context)





   
def notfiy_interviewx(request,idm,id):

    
    info_user = get_object_or_404(Interview_Schedule, id= int(idm))

    formatedDate = info_user.start.strftime("%H:%M")
    formatedDate1 = info_user.end.strftime("%H:%M")
    date_of_interview = info_user.start.strftime("%Y-%m-%d ")
    time_of_interview = str(formatedDate)+"-"+str(formatedDate1)

    # history of the User that is about to click the detail view 
    info = get_object_or_404(History, id= info_user.history_userx_f.id)

    # organixation inofrmation
    infox = Organization.objects.all().first()


    user = info.profile.Fname
    postion = info.application.title
    subject = 'Techin Notifcation'
    print(info.application.id)
    apps = get_object_or_404(Application, id=info.application.id)

    notice_info = get_object_or_404(Exam_Schedule,
                                    application_user=apps)
    

    location = info.location
    date_of_exam = date_of_interview
    time = str(formatedDate)+"-"+str(formatedDate1)
    google_map_link = infox.googlemap_link
    
    noti_read = Notification.objects.filter(id = id)
    noti_read.mark_all_as_read()



    context =  {'info' :info,
                'postion': postion,
                'date': date_of_exam,
                'location': location,
                'time': time,
                'user': user,
                'map': google_map_link
                
    
    }
 


    
    return render(request,'interview_date_notify.html', context)



# this view enables us to send both notifications and email for applicant that failed for screening process  
def notfiy_failed_all(request,id):
    
    MY_CHOICES = (
        ('pending', 'Pending'),
        ('Passed for Exam', 'Passed for Exam'),
        ('Failed for Exam', 'Failed for Exam'),
        ('Passed for INTERVIEW ', 'Passed for INTERVIEW '),
        ('Failed for INTERVIEW ', 'Failed for INTERVIEW'),
        ('INTERVIEW PASSED', 'INTERVIEW PASSED'),
        ('INTERVIEW FAILED', 'INTERVIEW FAILED'),

    )
    exam_ready1 = History.objects.filter(application = id ,status  = MY_CHOICES[2][0],failed_screning_notified = False)
    for exam_ready_single  in exam_ready1:
        idm = exam_ready_single.id
        failed_user =User.objects.filter(id=exam_ready_single.user.user.id)
        url = 'notfiy_failed_exam_url'
        notify.send(sender=request.user, recipient=failed_user,
                    verb='You Have Failed the The Screening Process ', description=url , target = exam_ready_single )
        exam_ready_single.save()
        exam_ready_single.failed_screning_notified = True


    exam_ready = History.objects.filter(application = id ,status  = MY_CHOICES[2][0],failed_screning_notified_email = False)
    for exam_ready_single  in exam_ready:
        idm = exam_ready_single.id

        user = exam_ready_single.profile.Fname
        postion = exam_ready_single.application.title
        subject = 'Techin Notifcation'
        message = render_to_string('emails/failed_screen.html', {
            'postion':postion,
            'user':user
            })

        zera = exam_ready_single.user.user.email
        print(zera)
        failed_user =User.objects.filter(id=exam_ready_single.user.user.id)

        to_email = zera
        sender = 'techinethiopia@gmail.com'
        plain_message = strip_tags(message)
    
        mail.send_mail(subject, plain_message, sender,
		                   [to_email], html_message=message)
        message = EmailMultiAlternatives(subject, plain_message, sender, [to_email])
        exam_ready_single.failed_screning_notified_email = True
        exam_ready_single.save()


        # url = 'notfiy_failed_exam_url'
        # notify.send(sender=request.user, recipient=failed_user,
        #             verb='You Have Failed the Exam ', description=url , target = exam_ready_single )

        # exam_ready_single.failed_screning_notified = True
        # exam_ready_single.save()

        
        

        # exam_ready_single.save()

    return redirect('list_url', id)


    



# this view enables us to send both notifications and email for applicant that failed the exams 
def notfiy_failed_exams(request,id):

    EXAM_RESULT = ( 
         ('Pending', 'Pending'), 
        ('Passed For Interview', 'Passed For Interview'),
        ('Failed For Interview', 'Failed For Interview'),   
  

    )
    exam_readyq = History.objects.filter(application = id ,status  = EXAM_RESULT[2][0],failed_exam_notified = False)

    for exam_ready_single  in exam_readyq:
        idm = exam_ready_single.id
        user = exam_ready_single.profile.Fname
        postion = exam_ready_single.application.title
        url = 'notficaton_url'
        notify.send(sender=request.user, recipient=failed_user,
                    verb='You Have Failed the Exam ', description=url , target = exam_ready_single )
        exam_ready_single.save()
        exam_ready_single.failed_exam_notified = True



    exam_ready = History.objects.filter(application = id ,status  = EXAM_RESULT[2][0],failed_exam_notified_email = False)
    for exam_ready_single  in exam_ready:
        idm = exam_ready_single.id

        user = exam_ready_single.profile.Fname
        postion = exam_ready_single.application.title
        subject = 'Techin Notifcation'
        message = render_to_string('emails/failed.html', {
            'postion':postion,
            'user':user
            })

        zera = exam_ready_single.user.user.email
        print(zera)
        failed_user =User.objects.filter(id=exam_ready_single.user.user.id)

        to_email = zera
        sender = 'techinethiopia@gmail.com'
        plain_message = strip_tags(message)
    
        mail.send_mail(subject, plain_message, sender,
		                   [to_email], html_message=message)
        message = EmailMultiAlternatives(subject, plain_message, sender, [to_email])
        exam_ready_single.failed_screning_notified_email = True
        exam_ready_single.save()


        # url = 'notficaton_url'
        # notify.send(sender=request.user, recipient=failed_user,
        #             verb='You Have Failed the Exam ', description=url , target = exam_ready_single )

        # exam_ready_single.failed_screning_notified = True
        # exam_ready_single.save()

        
        

        # exam_ready_single.save()

    return redirect('list_url', id)




def exam_active_all(request,id):

    MY_CHOICES = (
        ('pending', 'Pending'),
        ('Passed for Exam', 'Passed for Exam'),
        ('Failed for Exam', 'Failed for Exam'),
        ('Passed for INTERVIEW ', 'Passed for INTERVIEW '),
        ('Failed for INTERVIEW ', 'Failed for INTERVIEW'),
        ('INTERVIEW PASSED', 'INTERVIEW PASSED'),
        ('INTERVIEW FAILED', 'INTERVIEW FAILED'),

    )

    EXAM_STATUS = ( 
         ('Dectivate', 'Dectivate'), 
        ('Active', 'Active'),
        ('Closed', 'Closed'),   
  

    )

    exam_ready = History.objects.filter(application = id ,status  = MY_CHOICES[1][0])

    for exam_ready_single  in exam_ready:

        exam_ready_single.exam_status = EXAM_STATUS[1][0]

        exam_ready_single.save()
    messages.success(request, 'The Exam Is Activated.')

    return redirect('list_url', id)





def exam_active(request):
    if  request.POST:

        idx = request.POST.get('qid')
        # the pased  id value of the history app the applicants 
        status = request.POST.get('pid')
         # the pased  EXAM STATUS value of the history app the applicants 
        zid = request.POST.get('zid')  
        update_history = get_object_or_404(History,id = idx )
        update_history.exam_status = status
        print(update_history.exam_status)
        update_history.save()

        userx = get_object_or_404(User, id=update_history.user.id)

        # notify.send(sender=request.user, recipient=userx,
        #             verb='Your Exam Is Activated Please Click the Link below', description= 'quiz_index')

         # the pased  application id  value of the history app the applicants 
    
         # same goes for the other 2 functions 
        messages.success(request, str(update_history.profile.Fname)+' '+'Exam Is Activated.')
        return redirect('list_url', zid )
        # return HttpResponse(idx,status)

def exam_active1(request):

    if request.POST:
        idx1 = request.POST.get('qid1')
        status1 = request.POST.get('pid1')
        zid1 = request.POST.get('zid1')
        update_historyx = get_object_or_404(History,id = idx1 )
        update_historyx.exam_status = status1
        print(update_historyx.exam_status)
        update_historyx.save()        
        messages.info(request, str(update_historyx.profile.Fname)+' '+'Exam Is Deactivated.')
        return redirect('list_url', zid1 )
        # return HttpResponse(idx1,status1)

def exam_active2(request):
    if  request.POST:
        idx2 = request.POST.get('qid2')
        status2 = request.POST.get('pid2')
        zid2 = request.POST.get('zid2')
        update_historyy = get_object_or_404(History,id = idx2 )
        update_historyy.exam_status = status2
        print(update_historyy.exam_status)
        update_historyy.save()
        messages.info(request, str(update_historyx.profile.Fname)+' '+'Exam Is Closed.')
        return redirect('list_url', zid2 )
        # return HttpResponse(idx2,status2)
        # this are felids that updates the status of the exam once its choosen from the html page and then redirect it back 
    

def interview_active(request):
    if  request.POST:

        sitting_id = request.POST.get('qidx')
        print(sitting_id)
        print('hello')
        # the pased  id value of the history app the applicants 
        interview_status = request.POST.get('pidx')
        print(interview_status)
         # the pased  EXAM STATUS value of the history app the applicants 
        application_id = request.POST.get('zidx')
        print(application_id)  

        user_object = get_object_or_404(Sitting , id = sitting_id )


        update_history = get_object_or_404(History,user__id = user_object.user.id ,application  =  application_id )
        print('hello')
        print(update_history)


            
        update_history.exam_marks = interview_status
        update_history.save()
        
        user_object.interview_status = interview_status
        user_object.save()
         

        # print(update_history.exam_status)
        # update_history.save()
         # the pased  application id  value of the history app the applicants 

         # same goes for the other 2 functions 
        messages.info(request, str(update_history.profile.Fname)+' '+'Has been Selected For Interview')
        return redirect('list_url', application_id )
        # return HttpResponse(idx,status)

def interview_active1(request):
    if  request.POST:

        sitting_id = request.POST.get('qid1x')
        print(sitting_id)
        print('hello')
        # the pased  id value of the history app the applicants 
        interview_status = request.POST.get('pid1x')
        print(interview_status)
         # the pased  EXAM STATUS value of the history app the applicants 
        application_id = request.POST.get('zid1x')
        print(application_id)  

        user_object = get_object_or_404(Sitting , id = sitting_id )


        update_history = get_object_or_404(History,user__id = user_object.user.id ,application  =  application_id )
        print('hello')
        print(update_history)


            
        update_history.exam_marks = interview_status
        update_history.save()
        
        user_object.interview_status = interview_status
        user_object.save()
         

        # print(update_history.exam_status)
        # update_history.save()
         # the pased  application id  value of the history app the applicants 

         # same goes for the other 2 functions 
        messages.info(request, str(update_history.profile.Fname)+' '+'Has Not been Selected For Interview')
        return redirect('list_url', application_id )
        # return HttpResponse(idx,status)

def interview_active2(request):
    if  request.POST:

        sitting_id = request.POST.get('qid2x')
        print(sitting_id)
        print('hello')
        # the pased  id value of the history app the applicants 
        interview_status = request.POST.get('pid2x')
        print(interview_status)
         # the pased  EXAM STATUS value of the history app the applicants 
        application_id = request.POST.get('zid2x')
        print(application_id)  

        user_object = get_object_or_404(Sitting , id = sitting_id )


        update_history = get_object_or_404(History,user__id = user_object.user.id ,application  =  application_id )
        print('hello')
        print(update_history)


            
        update_history.exam_marks = interview_status
        update_history.save()
        
        user_object.interview_status = interview_status
        user_object.save()
         

        # print(update_history.exam_status)
        # update_history.save()
         # the pased  application id  value of the history app the applicants 

         # same goes for the other 2 functions 
        messages.info(request, str(update_history.profile.Fname)+' '+'Pending  for Interview Selection')
        return redirect('list_url', application_id )
        # return HttpResponse(idx,status)



def appDetail(request,idx):

    # author = PersonalInfo.objects.filter(id= id)
    pero = get_object_or_404(PersonalInfo,request.FILES or None, id=idx)
    # eduo = get_object_or_404(Edubackground, edubackground=pero)
    eduo = Edubackground.objects.filter(edubackground=pero)
    # lana = get_object_or_404(LanguageSkills, languageskills=pero)
    lano = LanguageSkills.objects.filter(languageskills=pero)
    # expa = get_object_or_404(Experience, experience=pero)
    expo = Experience.objects.filter(experience=pero)
    

    perform = personalInfoForm(request.GET or None,request.FILES or None, prefix="form1", instance=pero  )
    eduformset = EdubackgroundModelFormFormset(request.GET or None, prefix="form2" , instance = pero )
    
    lanformset = LanguageSkillsModelFormFormset(request.GET or None, prefix="form3", instance = pero)
    expformset = ExperienceModelFormFormset(request.GET or None, prefix="form4", instance = pero)  

    return render(request,'appDetail.html')

@login_required
@staff_member_required
def detail(request,kena,joly):
    
    # author = PersonalInfo.objects.filter(id= kena)
    pero = get_object_or_404(PersonalInfo,userx_id=kena,)
    # eduo = get_object_or_404(Edubackground, edubackground=pero)
    eduo = Edubackground.objects.filter(edubackground=pero)
    # lana = get_object_or_404(LanguageSkills, languageskills=pero)
    lano = LanguageSkills.objects.filter(languageskills=pero)
    # expa = get_object_or_404(Experience, experience=pero)
    expo = Experience.objects.filter(experience=pero)
    apps = get_object_or_404(History, application=joly,user=kena )
    history =InfoForm(request.GET or None, prefix="form5", instance=apps,)

    perform = personalInfoForm(request.GET or None, prefix="form1", instance=pero,   )
    eduformset = EdubackgroundModelFormFormset(request.GET or None, prefix="form2" , instance = pero )
    
    lanformset = LanguageSkillsModelFormFormset(request.GET or None, prefix="form3", instance = pero)
    expformset = ExperienceModelFormFormset(request.GET or None, prefix="form4", instance = pero)        

    print(eduformset.errors)

    template_name = 'detail.html'
   

    print('zera')
    if request.method == 'POST':

        history =InfoForm(request.POST or None, prefix="form5",instance=apps,)
        # genre_obj = get_object_or_404(Status , id=2)  
        sta = request.POST.get('form5-status')
        cooment = request.POST.get('form5-comment')
        
        # zera = Status.objects.get(name=request.POST.get('stainstance=pero, tus'))
        man = get_object_or_404(Status, id = sta )  
        # return HttpResponse(genre_obj)      
     
       
        if history.is_valid:
            zerax = get_object_or_404(Application, id=joly)
            t = History.objects.get(application= joly,user=kena )
            t.status = man
            t.comment = cooment
            t.save() 
            return redirect('list_url', joly)


        else:
            err = expformset.errors
            return HttpResponse(err)
            # return redirect('list_url')
            # return redirect('list_url')
    return render(request, template_name, {
        'perform': perform,
        'eduset':eduformset,
        'lanset':lanformset,
        'expset':expformset,
        'history':history,

        'pinfo':pero,
        'eduo':eduo,
        'lano':lano,
        'expo':expo,
    })


@login_required
def application_list(request):

    if request.user.is_staff: 

        return redirect('adminR')	

    elif request.user.is_authenticated and PersonalInfo.objects.filter(userx=request.user.id) .exists():
    

            app_list = Application.objects.filter(expired = False)
            statusx = History.objects.filter(user = request.user.id, application__expired = False )
            
            ids = History.objects.values_list('application_id', flat=True).filter(user__pk = request.user.id).distinct() 
            applications = Application.objects.exclude(pk__in = set(ids), )
            # applicationsx = Applications.objects.filter(expired = False )
            return render(request,'joblist.html' ,{ 'applications':applications,'statusx':statusx},)
            
    else:
        return redirect('apply_url')


@login_required
def applied_application(request):

    if request.user.is_staff: 

        return redirect('adminR')	


    elif request.user.is_authenticated and PersonalInfo.objects.filter(userx=request.user.id) .exists():

        # get_object_or_404(Quiz ,  )
        # zera = request.user.notifications.unread()
        status = History.objects.filter(user = request.user.id )
        return render(request,'applist.html',{'status':status,})
    else:
            return redirect('apply_url')


def admin_dash(request):

    app_count = Application.objects.all().count()
    active_app_count = Application.objects.filter(expired = False).count()
    p_info_count = PersonalInfo.objects.all().count()
    app_obj = Application.objects.all()
    history_obj = History.objects.all()
    per_info_obj = PersonalInfo.objects.all()


    context ={
     'app_count':app_count,
     'app_obj':app_obj,
     'active_app_count':active_app_count,
     'p_info_count':p_info_count,
     'history_obj':history_obj,
     'per_info_obj':per_info_obj,





    }




 


    return render(request, 'admin_dash.html', context)



def newx(request):



    return render(request, 'new.html')




def detailx_app(request, id, ida,):


    apps = get_object_or_404(History, application=ida,user= id )
    if request.method == 'POST':

         
        statusform = InfoForm(request.POST, prefix = "form8") 

        if statusform.is_valid():
    
          history =InfoForm(request.POST or None, prefix="form8",instance=apps)
        # genre_obj = get_object_or_404(Status , id=2)  
          sta = request.POST.get('form8-status')
          cooment = request.POST.get('form8-comment')
        
        # zera = Status.objects.get(name=request.POST.get('stainstance=pero, tus'))
        # man = get_object_or_404(Status, id = sta )  
        # return HttpResponse(genre_obj)      
     
       
        if history.is_valid:
            zerax = get_object_or_404(Application, id=ida)
            t = History.objects.get(application= ida,user= id )
            t.status = sta
            t.comment = cooment
            t.save() 
            return redirect('list_url', ida)


        else:
            err = expformset.errors
            return HttpResponse(err)

    else:
       
        app_list = Application.objects.filter(expired = False)

        perform = personalInfoForm(request.GET or None, prefix="form1"  )
        eduformset = EdubackgroundModelFormFormset(request.GET or None, prefix="form2"  )
        lanformset = LanguageSkillsModelFormFormset(request.GET or None, prefix="form3" )
        expformset = ExperienceModelFormFormset(request.GET or None, prefix="form4") 
        statusform = InfoForm(request.GET or None, prefix = "form8") 



        statusx = History.objects.filter(user = request.user.id, application__expired = False )
        profile = get_object_or_404(PersonalInfo, userx_id = id )
        profilex = get_object_or_404(Profile, user = id)
         
        edu = Edubackground.objects.filter(edubackground__userx_id = id)
        #  edu = get_object_or_404(Edubackground, edubackground__userx_id = request.user.id)
        #  lan = get_object_or_404(LanguageSkills, languageskills__userx_id =request.user.id)
        lan = LanguageSkills.objects.filter( languageskills__userx_id = id)
        edu1 = get_object_or_404(Elementary_School, pinfoe__userx_id = id)
        edu2 = get_object_or_404(Secondary_School, pinfos__userx_id = id)
        edu3 = get_object_or_404(Preparatory_School, pinfop__userx_id = id)
        exp = Experience.objects.filter(experience__userx_id = id).exclude(Company__isnull=True)
        apps = get_object_or_404(History, application=ida,user= id )
        status = History.objects.filter(user = request.user.id )
        
        # ids = History.objects.values_list('application_id', flat=True).filter(user__pk = request.user.id).distinct() 
        # applications = Application.objects.exclude(pk__in = set(ids)) 
        now=datetime.date.today()
        context = {
            'profile':profile,
            # 'applications':applications,
            'status':status,
            'profilex':profilex,
            'edu':edu, 
            'lan':lan,
            'exp':exp,        
            'eduset':eduformset,
            'lanset':lanformset,
            'expset':expformset,
            'statusx':statusx,
            'edu1':edu1,
            'edu2':edu2,
            'edu3':edu3,
            'statusform':statusform,
            'ida': ida,
            }
        return render(request, 'detailx.html',context )





def detail_app(request, id, ida,):


    apps = get_object_or_404(History, application=ida,user= id )
    if request.method == 'POST':

         
        statusform = InfoForm(request.POST, prefix = "form8") 

        if statusform.is_valid():
    
          history =InfoForm(request.POST or None, prefix="form8",instance=apps)
        # genre_obj = get_object_or_404(Status , id=2)  
          sta = request.POST.get('form8-status')
          cooment = request.POST.get('form8-comment')
        
        # zera = Status.objects.get(name=request.POST.get('stainstance=pero, tus'))
        # man = get_object_or_404(Status, id = sta )  
        # return HttpResponse(genre_obj)      
     
       
        if history.is_valid:
            zerax = get_object_or_404(Application, id=ida)
            t = History.objects.get(application= ida,user= id )
            t.status = sta
            t.comment = cooment
            t.save() 
            return redirect('list_url', ida)


        else:
            err = expformset.errors
            return HttpResponse(err)

    else:
       
        app_list = Application.objects.filter(expired = False)

        perform = personalInfoForm(request.GET or None, prefix="form1"  )
        eduformset = EdubackgroundModelFormFormset(request.GET or None, prefix="form2"  )
        lanformset = LanguageSkillsModelFormFormset(request.GET or None, prefix="form3" )
        expformset = ExperienceModelFormFormset(request.GET or None, prefix="form4") 
        statusform = InfoForm(request.GET or None, prefix = "form8") 



        statusx = History.objects.filter(user = request.user.id, application__expired = False )
        profile = get_object_or_404(PersonalInfo, userx_id = id )
        profilex = get_object_or_404(Profile, user = id)
         
        edu = Edubackground.objects.filter(edubackground__userx_id = id)
        #  edu = get_object_or_404(Edubackground, edubackground__userx_id = request.user.id)
        #  lan = get_object_or_404(LanguageSkills, languageskills__userx_id =request.user.id)
        lan = LanguageSkills.objects.filter( languageskills__userx_id = id)
        edu1 = get_object_or_404(Elementary_School, pinfoe__userx_id = id)
        edu2 = get_object_or_404(Secondary_School, pinfos__userx_id = id)
        edu3 = get_object_or_404(Preparatory_School, pinfop__userx_id = id)
        exp = Experience.objects.filter(experience__userx_id = id).exclude(Company__isnull=True)
        apps = get_object_or_404(History, application=ida,user= id )
        status = History.objects.filter(user = request.user.id )
        
        # ids = History.objects.values_list('application_id', flat=True).filter(user__pk = request.user.id).distinct() 
        # applications = Application.objects.exclude(pk__in = set(ids)) 
        now=datetime.date.today()
        context = {
            'profile':profile,
            # 'applications':applications,
            'status':status,
            'profilex':profilex,
            'edu':edu, 
            'lan':lan,
            'exp':exp,        
            'eduset':eduformset,
            'lanset':lanformset,
            'expset':expformset,
            'statusx':statusx,
            'edu1':edu1,
            'edu2':edu2,
            'edu3':edu3,
            'statusform':statusform,
            'ida': ida,
            }
        return render(request, 'detailx.html',context )



def viewpdf(request , id):

    profile = get_object_or_404(PersonalInfo, userx_id = id )



    return render(request, 'pdr.html',{'profile':profile, } )


def add_schedule(request, id):
    all_events = Interview_Schedule.objects.all()
    #interview_start
    interview_form = Interview_Schedule_User(
        request.GET or None, prefix="form12", )
    if request.method == 'POST':

        interview_form = Interview_Schedule_User(request.POST, prefix="form12")

        if interview_form.is_valid():
            schedule = interview_form.save(commit=False)
            schedule.application_f = id
            schedule.save()
            
            
        else:

            return render(request, 'calendar.html',  {'events': all_events,
                          'interview_form': interview_form,})
    context = {
        "events": all_events,
        'interview_form': interview_form,
    }

    return render(request, 'calendar.html', context)
    

def create_post(request):
        all_events = Interview_Schedule.objects.all()
        interview_form = Interview_Schedule_User(
        request.GET or None, prefix="form12", )


    # app_idx = id
        response_data = {}

 
        title = request.GET.get('title')
        starting = request.GET.get('starting')
        ending = request.GET.get('ending')
        his_id = request.GET.get('his_id')
        app_id = request.GET.get('app_id')
        # datex = datetime(starting, "%Y-%m-%d %H:%M:%S")2021-01-19, 8:05:00 a.m. format date js
        print(starting)
        start = starting[:10]+" "+starting[11:19]
        end = ending[:10]+" "+ending[11:19]
        print(start)
        print(end)
        # startx = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
        # endx = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
         
        startx = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
        endx = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
        print(startx)

        if(startx > endx):
            response_data['error_message'] = 'starting date cant come after ending date '
            response_data['is_right'] = False

        if(startx < datetime.datetime.now()):
            response_data['error_message'] = 'starting date cant be in the past'
            response_data['is_right'] = False
        if(endx < datetime.datetime.now()):
            response_data['error_message'] = 'Ending date cant be in the past'
            response_data['is_right'] = False

        else:  
            hist = get_object_or_404(History, id =  his_id)
            
            apps = get_object_or_404(Application, id = app_id)
            schedule = Interview_Schedule(name=str(title), start=startx,
                               end=endx, history_userx_f=hist, application_f=apps)
            schedule.save()
            hist.interview_start = startx
            hist.interview_end = endx
            hist.save()

            
            response_data['is_right'] = True
            response_data['error_message'] = 'You have Scheduled Interview sucessfully '
        



        print(response_data)
        return JsonResponse(response_data)




def calendar(request, id ):
    EXAM_RESULT = (
         ('Pending', 'Pending'),
        ('Passed For Interview', 'Passed For Interview'),
        ('Failed For Interview', 'Failed For Interview'),


    )

    ids = Interview_Schedule.objects.values_list(
           'history_userx_f', flat=True).distinct()

    passed_for_interview = History.objects.filter(
        application=id, exam_marks=EXAM_RESULT[1][0],).exclude(pk__in=ids)

    all_events = Interview_Schedule.objects.all()

    # application_user= Interview_Schedule.objects.all().exclude()
    app_idx = id
    interview_form = Interview_Schedule_User(
        request.GET or None, prefix="form12", )
 
    context = {
        'events': all_events,
        'interview_form': interview_form,
        'app_idx':app_idx,
        'interview': passed_for_interview
    }
    return render(request, 'new_event.html', context)


def add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    event = Interview_Schedule(name=str(title), start=start, end=end)
    event.save()
    data = {}
    return JsonResponse(data)


def update(request):
    response_data = {}
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    startc = start[:10]+" "+start[11:19]
    endc = end[:10]+" "+end[11:19]
    startx = datetime.datetime.strptime(startc, "%Y-%m-%d %H:%M:%S")
    endx = datetime.datetime.strptime(endc, "%Y-%m-%d %H:%M:%S")
    print(id)
    if(startx > endx):
            response_data['error_message'] = 'starting date cant come after ending date '
            response_data['is_right'] = False

    if(startx < datetime.datetime.now()):
            response_data['error_message'] = 'starting date cant be in the past'
            response_data['is_right'] = False
    if(endx < datetime.datetime.now()):
            response_data['error_message'] = 'Ending date cant be in the past'
            response_data['is_right'] = False

    else:
        event = Interview_Schedule.objects.get(id=int(id))
        event.start = startx
        event.end = endx
        event.name = title
        event.save()
        print(event)    
        
        response_data['error_message'] = 'Interview Has been Sucessfully Scheduled '
        response_data['is_right'] = True
    # hist.interview_start = start
    # hist.interview_end = end
    # hist.save()
   
    return JsonResponse(response_data)


def remove(request):
    data = {}
    id = request.GET.get("id", None)
    if id is None:
         data['error_message'] = 'Null Value'

    else:
        event = Interview_Schedule.objects.get(id=int(id))
        event.delete()
        data['is_right'] = True
    data['error_message'] = 'Interview Schedule Has been Sucessfully Deleted '



    
    return JsonResponse(data)
