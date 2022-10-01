
from recruit.models import *
from notifications.signals import notify
from django.contrib.auth.models import User
from quiz.models import *
from core.models import *
from organization.models import *
def orginfo(request):

    portal_info = Organization.objects.all().first()

    if request.user.is_staff or request.user.is_authenticated :
        
        unique = request.user.notifications.unread()
        pic_pro = Profile.objects.get(user = request.user)
        return {'unique': unique, 'pic_pro': pic_pro,'portal_info':portal_info}
    else:
        unique = 'nop'
        pic_pro = {}

        return {'unique': unique, 'pic_pro': pic_pro,'portal_info':portal_info,}
