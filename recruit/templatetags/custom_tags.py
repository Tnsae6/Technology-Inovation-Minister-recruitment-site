from django import template
from datetime import datetime
from recruit.models import * 
from django.shortcuts import render,get_object_or_404


register = template.Library()

@register.filter(name="datex")
def datex(value, arg):
    print(value)

    if arg == "datem":
       my_date = value.isoformat()
       return my_date
    else :
        return value

@register.filter(name="edu")
def edu(value, arg):
    phd = False
    ms = False
    bs = False
    DEGREE_CHOICE = (('bachelor', 'Bachelor'),
                     ('masters ', 'Masters '), ('doctor of philosophy', 'Doctor of Philosophy'))
    print(value)
    
    floatInInt = int(float(value))
    # print(floatInInt)
    educaton = Edubackground.objects.filter(edubackground__id = floatInInt)
    for  edu in educaton:
        print(edu.Degree_level)
        if(edu.Degree_level == DEGREE_CHOICE[2][0]):
             phd = True
        elif(edu.Degree_level == DEGREE_CHOICE[1][0]):
             ms = True
        elif edu.Degree_level == DEGREE_CHOICE[0][0]:
            bs = True
    if (phd == True):
        return 'Doctor of Philosophy'
    elif (ms == True):
        return 'Masters'
    elif (bs == True):
        return 'Bachelor'



@register.filter(name="gpa")
def gpa(value, arg):
    phd = False
    ms = False
    bs = False
    GPAD = 0
    GPAM = 0
    GPAP = 0
    DEGREE_CHOICE = (('bachelor', 'Bachelor'),
                     ('masters ', 'Masters '), ('doctor of philosophy', 'Doctor of Philosophy'))
    print(value)
    
    floatInInt = int(float(value))
    # print(floatInInt)
    educaton = Edubackground.objects.filter(edubackground__id = floatInInt)
    for  edu in educaton:
        print(edu.Degree_level)
        if(edu.Degree_level == DEGREE_CHOICE[2][0]):
            phd = True
            GPAP = edu.cumulative_gpa

        elif(edu.Degree_level == DEGREE_CHOICE[1][0]):
            ms = True
            GPAM = edu.cumulative_gpa
        elif edu.Degree_level == DEGREE_CHOICE[0][0]:
            bs = True
            GPAD = edu.cumulative_gpa

    if (phd == True):
        return GPAP
    elif (ms == True):
        return GPAM
    elif (bs == True):
        return GPAD

    

@register.filter(name="interviewx")
def interviewx(value, arg):
        floatInInt = int(float(value))       
        dj= get_object_or_404(History, id = floatInInt)
        try:
           obj1 = Interview_Schedule.objects.get(history_userx_f =  dj)
           formatedDate = obj1.start.strftime("%Y-%m-%d ")
           formatedDate1 = obj1.end.strftime("%Y-%m-%d ")
           print(formatedDate)
           
           return str(formatedDate)
           
        except Interview_Schedule.DoesNotExist:
            return 'Interview Not Scheduled'


@register.filter(name="interviewy")
def interviewy(value, arg):
        floatInInt = int(float(value))       
        dj= get_object_or_404(History, id = floatInInt)
        try:
           obj1 = Interview_Schedule.objects.get(history_userx_f =  dj)
           formatedDate = obj1.start.strftime("%H:%M")
           formatedDate1 = obj1.end.strftime("%H:%M")
          
           
           return str(formatedDate)+"-"+str(formatedDate1)
           
        except Interview_Schedule.DoesNotExist:
            return 'Not Scheduled'


@register.filter(name="name")
def name(value, arg):
    if arg == "Lname":
        floatInInt = int(float(value))       
        dj= get_object_or_404(PersonalInfo, userx__user_id = floatInInt)
        return dj.Lname
    if arg == "Fname":
        floatInInt = int(float(value))       
        dj= get_object_or_404(PersonalInfo, userx__user_id = floatInInt)
        return dj.Fname
    else:
        return 'No Name'

        
