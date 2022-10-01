from django.shortcuts import get_object_or_404, redirect, render, render_to_response
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView
from core.forms import SignUpForm, ProfileForm
from django.contrib.auth.models import User

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from core.tokens import account_activation_token
from django.core.mail import EmailMessage
from django.core import mail
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from core.decorators import unauthenticated_user
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from recruit.models import PersonalInfo,Profile
from django.utils.encoding import force_text



# Sign Up View
class SignUpView(View):
    form_class = SignUpForm
    template_name = 'accounts/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your Techin Job Portal Account'
            message = render_to_string('emails/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': force_text(urlsafe_base64_encode(force_bytes(user.pk))),
                'token': account_activation_token.make_token(user),
                
            })
            # user.email_user(subject, message)
            #             emails = EmailMessage(
            #             subject, message, to=[to_email]
            # )
            # emails.send()
            to_email = form.cleaned_data.get('email')
            sender = 'techinethiopia@gmail.com'
            plain_message = strip_tags(message)
    
            mail.send_mail(subject, plain_message, sender,
		                   [to_email], html_message=message)
            message = EmailMultiAlternatives(subject, plain_message, sender, [to_email])

            
            messages.success(request, ('Please Confirm your email to complete registration.'))

            return redirect('login')

        return render(request, self.template_name, {'form': form})


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from core.tokens import account_activation_token
from django.http import HttpResponseRedirect
from django.template import RequestContext
from recruit.models import PersonalInfo,Profile

class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            
            login(request, user,backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('apply_url')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('login')


# def login_user(request):
#     logout(request)
#     username = password = ''
# 	if request.method == 'POST':
#     	username = request.POST.get('username')
# 		password =request.POST.get('password')
# 		user = authenticate(request, username=username, password=password)
# 		if user is not None:
# 			login(request, user)
# 			return redirect('homeurl')
# 		else:
# 			messages.info(request, 'Username OR password is incorrect')
# 	context = {}
# 	return render(request, 'accounts/login.html', context)


def get_userprofile(user):
    qs = PersonalInfo.objects.filter(userx=user)
    if qs.exists():
        return qs[0]
    
    else:
        
     return HttpResponse("there is no author passed for the function")



# # admin login for commeties 
# def login_



#user login for recruits 
def login_user(request):
    
	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)     

			if user.is_staff:    
			    return redirect('adminR')	 
			elif PersonalInfo.objects.filter(userx =request.user.id) .exists():
			    # organization = get_object_or_404(Organization, pk=pk)
			    return redirect('dash_url')
			elif Profile.objects.filter(user =request.user.id,email_confirmed = True) .exists()and request.path != '/apply/':
			    # organization = get_object_or_404(Organization, pk=pk)
			    return redirect('apply_url')               

			else:
			    return redirect('login')
		else:
			messages.info(request, 'Username OR password is incorrect')
	context = {}
	return render(request, 'accounts/login.html', context)


# Edit Profile View
class ProfileView(UpdateView):
    model = User
    form_class = ProfileForm
    success_url = reverse_lazy('apply_url')
    template_name = 'application.html'