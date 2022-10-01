from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Sign Up Form
class SignUpForm(UserCreationForm):
    # first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    # last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':"form-control",'placeholder':"xyz@example.com" }),max_length=254, help_text='Enter a valid email address')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':"form-control",'placeholder':"Password" }), min_length=8,
        strip=True,)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':"form-control",'placeholder':"Repeat Password" }), min_length=8,
        strip=True,)
    	

    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'password1', 
            'password2',
             
            ]
        widgets = {
                 'username': forms.TextInput(
            		attrs={
					'class': 'form-control',
                    'placeholder':'Enter User Name' 
					}
				),
                
                            }
    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).count() > 0:
              raise forms.ValidationError("We have a user with this user email-id")
        return data


    

        
# Profile Form

class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'username',
            'first_name', 
            'last_name', 
            'email',
            ]
