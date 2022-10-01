from django.db import models
from django.contrib.auth.models import User
from core.models import Profile
from django.utils.datetime_safe import date
from .validators import validate_file_extension
from phonenumber_field.modelfields import PhoneNumberField
from quiz.models import Category, Sitting
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect 
from django.contrib import messages
from tinymce.models import HTMLField
  



# Create your models here.






class Interest(models.Model):
    name = models.CharField( max_length=20, blank=True, null=True)
    



    def __str__(self):
            return self.name 
            



class PersonalInfo(models.Model):


    CHOICE = (('male', 'Male'),
              ('female', 'Female'))
    Fname = models.CharField(max_length=50)
    Mname = models.CharField(max_length=50)
    Lname = models.CharField(max_length=50)
    Email = models.EmailField()
    PhoneNo = PhoneNumberField(region='ET')
    Nationality = models.CharField(max_length=50)
    City = models.CharField(max_length=50,blank=True, null=True)
    DateofBirth = models.DateField()
    PlaceofBirth = models.CharField(max_length=50)
    Gender = models.CharField(max_length=50, choices=CHOICE, )
    disablity = models.BooleanField(("True if the person is disabled "), default = False)
    Name = models.CharField(max_length=200, blank=True, null=True)
    PhoneNumber =PhoneNumberField(region='ET', blank = True, null = True)
    EmailAdd = models.EmailField(blank=True, null=True)
    Name_r = models.CharField(max_length=200, blank=True, null=True)
    PhoneNumber_r =PhoneNumberField(region='ET', blank = True, null = True)
    EmailAdd_r = models.EmailField(blank=True, null=True)
    Name_r1 = models.CharField(max_length=200, blank=True, null=True)
    PhoneNumber_r1 =PhoneNumberField(region='ET', blank = True, null = True)
    EmailAdd_r1 = models.EmailField(blank=True, null=True)
    CoverLetter = models.TextField(blank=True, null=True)
    cv = models.FileField(blank=True, null=True,validators=[validate_file_extension])
    docs =  models.FileField(blank=True, null=True,validators=[validate_file_extension])
    
    
    categories = models.ForeignKey(Category, blank=True, null=True,on_delete=models.CASCADE,)
    userx = models.OneToOneField(Profile,on_delete=models.CASCADE, blank=True, null=True)
   
    DEGREE_CHOICE = (('bachelor', 'Bachelor'),
                     ('masters ', 'Masters '), ('doctor of philosophy', 'Doctor of Philosophy'))



    def __str__(self):
            return self.Fname

        
    @property
    def count_edu(self):

        edu = Edubackground.objects.filter(edubackground = self)


    # for edux in edu:

    #     edux.Degree_level == DEGREE_CHOICE[1][0]

        
    # if edu.Degree_level

        
        
    #     return Edubackground.objects.filter(edubackground  = self).count()


    @property 
    def is_male(self):
        
        return PersonalInfo.objects.filter(Gender = male ).count()
    
    @property
    def is_female(self):
            
        return PersonalInfo.objects.filter(Gender = female ).count()

    




class Elementary_School(models.Model):
    School_name =  models.CharField(max_length=200)
    starting_date = models.DateField()
    end_date = models.DateField()
    pinfoe = models.ForeignKey(
        PersonalInfo, related_name='personal_elementary', on_delete=models.CASCADE, null=True, blank=True)

class Secondary_School(models.Model):
    School_names =  models.CharField(max_length=200)
    starting_dates = models.DateField()
    end_dates = models.DateField()
    pinfos = models.ForeignKey(
        PersonalInfo, related_name='personal_Secondary', on_delete=models.CASCADE, null=True, blank=True)

class Preparatory_School(models.Model):
    School_namep =  models.CharField(max_length=200)
    starting_datep = models.DateField()
    end_datesp = models.DateField()
    pinfop = models.ForeignKey(
        PersonalInfo, related_name='personal_preparatory', on_delete=models.CASCADE, null=True, blank=True)



class Edubackground(models.Model):
    DEGREE_CHOICE = (('bachelor', 'Bachelor'),
                     ('masters ', 'Masters '), ('doctor of philosophy', 'Doctor of Philosophy'))

    University = models.CharField(max_length=200)
    FieldofStudy = models.CharField(max_length=200)
    Degree_level = models.CharField(max_length=40, choices=DEGREE_CHOICE)
    From = models.DateField()
    To = models.DateField()
    cumulative_gpa = models.CharField(max_length=60,)
    edubackground = models.ForeignKey(
        PersonalInfo, related_name='personaledu', on_delete=models.CASCADE, null=True, blank=True)








    # def save(self, *args, **kwargs):
    #     if self.To < self.From:
    #         # essages.error(request, "Error. Message not sent.")m
    #         return redirect('error_url', 1)
    #     if int(self.cumulative_gpa) < 4:
    #         # messages.error(request, "Error. Message not sent.")
    #         return redirect('dash_url')            
    #         # raise ValidationError("The date cannot be in the past!")

    #     super(Event, self).save(*args, **kwargs)
    


class LanguageSkills(models.Model):
    LEVEL = (('excellent', 'Excellent'),
             ('verygood', 'Very Good'), ('good', 'Good'), ('poor', 'Poor'))

    Language = models.CharField(max_length=50)
    Writing = models.CharField(max_length=10, choices=LEVEL)
    Listening = models.CharField(max_length=10, choices=LEVEL,)
    Speaking = models.CharField(max_length=10, choices=LEVEL)
    Reading = models.CharField(max_length=10, choices=LEVEL)
    languageskills = models.ForeignKey(
        PersonalInfo, related_name='personallangu', on_delete=models.CASCADE, blank=True, null=True)


class Experience(models.Model):


    Company = models.CharField(max_length=200,blank=True , null= True)
    Position = models.CharField(max_length=200,blank=True , null= True)
    YearofExp = models.CharField(max_length=10, blank=True , null= True)
    Start = models.DateField(blank=True , null= True)
    End = models.DateField(blank=True , null= True)
    experience = models.ForeignKey(
        PersonalInfo, related_name='personalexxp', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
            unique_together = ('Start', 'End',)

class Reference(models.Model):
    Name = models.CharField(max_length=200,blank=True , null= True)
    PhoneNumber = models.CharField(max_length=14,blank=True , null= True)
    EmailAdd = models.EmailField(blank=True , null= True)





class Document(models.Model):
    CoverLetter = models.TextField(blank=True, null=True)
    cv = models.FileField()



# class Postion(models.Model):
#     name = models.CharField(max_length=20, blank=True, null=True)

class ApplicationType(models.Model):
    typesApps = models.CharField(max_length=20, blank=True, null=True)
    def __str__(self):
            return self.typesApps

class Application(models.Model):
    # typ = (('intern', 'intern'),
    #        ('vacancy', 'vacancy'))
    title = models.CharField(max_length=100, blank=True, null=True)
    postion = models.CharField(max_length=100, blank=True, null=True)
    # postion = models.ManyToManyField("Postion", verbose_name=_("postions"), blank,blank=True, null=True)
    qualifaction= models.CharField(max_length=10000, blank=True, null=True)
    required_experinace = models.CharField(max_length=100,blank=True, null=True)                                                                                                                                                                                                                                                                                                                                                                                                                                                  
    description = models.CharField(max_length = 900, blank=True, null=True)
    detail = HTMLField('Content', blank=True, null=True)

    types = models.ForeignKey(ApplicationType, on_delete=models.SET_NULL, blank=True, null=True)
    starting_date = models.DateField()
    endingdate = models.DateField()
    created_at = models.DateField(auto_now_add = True,blank=True, null=True)
    
    expired  = models.BooleanField(("if the date has paseed and Expired "), default = False )

    failed_screning_notifiedyx = models.BooleanField(
        ("if the applicant has been notified if failed for screning  "), default=False)
    failed_exam_notifiedyx = models.BooleanField(
        ("if the applicant has been notified if failed for exam  "), default=False)
    failed_interview_notifiedyx = models.BooleanField(
        ("if the applicant has been notified if failed for interview  "), default=False)
    exam_date_notifiedyx = models.BooleanField(
        ("if the applicant has been notified for exam date  "), default=False)
    Interivew_date_notifiedyx = models.BooleanField(
        ("if the applicant has been notified for interview date  "), default=False)
 
    @property
    def is_past_due(self):
        
        return date.today() > self.endingdate

    @property
    def application_male(self):
        return History.objects.filter(application  =  self,  profile__Gender = 'male' ).count() 

    @property
    def application_female(self):
        return History.objects.filter(application  =  self , profile__Gender = 'female' ).count()






    def __str__(self):
            return self.title


# pending 
# passed for exam
# faild for exam
# passed the exam
#faild the exam 
#passed for interview 
#falid for interview 
# secdule intreview


class Messages(models.Model):
    message_exam = models.CharField(max_length=10020, blank=True, null=True)
    message_interview = models.CharField(max_length=10020, blank=True, null=True)



class Exam_Schedule(models.Model):

    TIME = (('A.M', 'A.M'),
             ('P.M', 'P.M'),
             )


    exam_message = models.CharField(max_length=10020, blank=True, null=True)
    exam_date = models.DateField(("the date when the exam is held "), auto_now=False, auto_now_add=False)
    exam_time = models.TimeField(auto_now=False, auto_now_add=False)
    # time_set = models.CharField(
    #     max_length=10, choices=TIME, default=TIME[0][0])
    exam_location = models.CharField(max_length=500, )

    google_map_link = models.URLField(max_length=200, blank=True, null=True)
    application_user = models.ForeignKey(
        Application, on_delete=models.SET_NULL, blank=True, null=True)
    # history_user = models.ForeignKey(
    #     "History", on_delete=models.SET_NULL, blank=True, null=True)




class Status(models.Model):

  name = models.CharField(max_length = 20)

  def __str__(self):
            return self.name


class Recruit_Application_Status(models.Model):
    
    application =  models.ForeignKey('Application', related_name='application', on_delete=models.CASCADE)
    user = models.ForeignKey(Profile,on_delete=models.CASCADE, )
    pending  = models.BooleanField((" if the user has applied for specfic application but still waiting for evaluation "))
    falied = models.BooleanField(("if the applicants has falied  specfic applicaton its active then  "), default = False)
    exam_active = models.BooleanField(("active exam for applicant  "), default = False)
    exam_taken = models.BooleanField(("if the applicants has taken the exam and waitng for result  "), default = False)
    exam_result_pending = models.BooleanField(("if the applicants has taken the exam and waitng for result  "), default = False)
    passed_the_exam =  models.BooleanField(("if the applicants has passed the exam"), default = False)
    falied_the_exam = models.BooleanField(("if the applicants has falied the exam"), default = False)
    interview_passed = models.BooleanField(("if the applicants has passed the interview "), default = False)
    interview_falied = models.BooleanField(("if the applicants has falied the interview "), default = False)
    jump_to_interview = models.BooleanField(("if the applicants pass directly to interview e.g interns  "), default = False)



# class Interset

class History(models.Model):

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
  EXAM_RESULT = ( 
         ('Pending', 'Pending'), 
        ('Passed For Interview', 'Passed For Interview'),
        ('Failed For Interview', 'Failed For Interview'),   
  

    )
  
  user = models.ForeignKey(Profile,on_delete=models.CASCADE, blank=True, null=True)
  profile = models.ForeignKey(
        PersonalInfo, related_name='personal', on_delete=models.SET_NULL, blank=True, null=True)
#   field_of_interest = Many_to(Interest,)
  application = models.ForeignKey(Application,on_delete=models.CASCADE, blank=True, null=True)
  date = models.DateField(auto_now_add=True)

#   interest = models.ManyToOneRel
  exam_status = models.CharField(choices=EXAM_STATUS, default=EXAM_STATUS[0][0], max_length=100)
  exam_marks = models.CharField(choices=EXAM_RESULT, default=EXAM_RESULT[0][0], max_length=100)
  interview_start = models.DateTimeField(null=True, blank=True)
  interview_end = models.DateTimeField(null=True, blank=True)
  status = models.CharField(choices=MY_CHOICES, default=MY_CHOICES[0][0], max_length=100, )
  comment = models.CharField(max_length = 800, blank = True, null = True)
  failed_screning_notified = models.BooleanField(
      ("if the applicant has been notified if failed for screning  "), default=False)
  failed_screning_notified_email = models.BooleanField(
      ("if the applicant has been notified if failed for screning via email  "), default=False)
  failed_exam_notified = models.BooleanField(
      ("if the applicant has been notified if failed for exam  "), default=False)
  failed_exam_notified_email = models.BooleanField(
      ("if the applicant has been notified if failed for exam  via email  "), default=False)
  failed_interview_notified = models.BooleanField(
      ("if the applicant has been notified if failed for interview  "), default=False)
  failed_interview_notified_email = models.BooleanField(
      ("if the applicant has been notified if failed for interview via email  "), default=False)
  exam_date_notified = models.BooleanField(
      ("if the applicant has been notified for exam date  "), default=False)
  exam_date_notified_email = models.BooleanField(
      ("if the applicant has been notified for exam date via email  "), default=False)
  Interivew_date_notified_email = models.BooleanField(
      ("if the applicant has been notified for interview date via email  "), default=False)

  Interivew_date_notified = models.BooleanField(
      ("if the applicant has been notified for interview date   "), default=False)

  exam_resultx = models.ForeignKey('quiz.Sitting', related_name='resultx',on_delete=models.SET_NULL, blank=True, null=True) 

#  Sitting
  def __str__(self):
            return self.profile.Fname
  @property
  def application_male(self):
        return History.objects.filter(application=self.application,profile__Gender = 'male' ).count() 

  @property
  def application_female(self):
        return History.objects.filter(application=self.application,profile__Gender = 'female' ).count()

  @property
  def application_li(self):
        return History.objects.filter(application=self.application,)





class Exam_passed(models.Model):
    pass 


class Interview_Schedule(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    interview_location = models.CharField(
        max_length=500, blank=True, null=True)
    google_map_link = models.URLField(max_length=200, blank=True, null=True)
    history_userx_f = models.OneToOneField(
        "History", verbose_name=("Interview Schedule Per User"), on_delete=models.CASCADE, )
    
      
    application_f = models.ForeignKey(
        Application, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name






    
    
