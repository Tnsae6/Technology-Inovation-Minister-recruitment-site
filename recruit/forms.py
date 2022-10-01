from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from datetime import datetime
from django.forms import ModelForm
# from tinymce import TinyMCE
from  crispy_forms.layout import Layout , Submit
from crispy_forms.helper import FormHelper
from .models import *
from django.forms import (formset_factory, modelformset_factory,inlineformset_factory)
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from constrainedfilefield.fields import ConstrainedFileField
from django.forms.formsets import BaseFormSet
alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')




def file_size(value): # add this to some file where you can import it from
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 2 MiB.')

# class PillarRequiredFormSet(BaseFormSet):
#     def __init__(self, *args, **kwargs):
#        super(EdubackgroundModelFormFormset, self).all(*args, **kwargs)
#        for form in self.forms:
#          form.empty_permitted = False


class ThatForm(forms.models.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(ThatForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        for form in self.forms:
            form.empty_permitted = True


class MinimumRequiredFormSet(forms.models.BaseInlineFormSet):
    """
    Inline formset that enforces a minimum number of non-deleted forms
    that are not empty
    """
    default_minimum_forms_message = "At least %s set%s of data is required"

    def __init__(self, *args, **kwargs):
        self.minimum_forms = kwargs.pop('minimum_forms', 0)
        minimum_forms_message = kwargs.pop('minimum_forms_message', None)
        if minimum_forms_message:
            self.minimum_forms_message = minimum_forms_message
        else:
            self.minimum_forms_message = \
                self.default_minimum_forms_message % (
                    self.minimum_forms,
                    '' if self.minimum_forms == 1 else 's'
                )

        super(MinimumRequiredFormSet, self).__init__(*args, **kwargs)

    def clean(self):
        non_deleted_forms = self.total_form_count()
        non_empty_forms = 0
        for i in  range(0, self.total_form_count()):
            form = self.forms[i]
            if self.can_delete and self._should_delete_form(form):
                non_deleted_forms -= 1
            if not (form.instance.id is None and not form.has_changed()):
                non_empty_forms += 1
        if (
            non_deleted_forms < self.minimum_forms
            or non_empty_forms < self.minimum_forms
        ):
            raise forms.ValidationError(self.minimum_forms_message)

# class PillarxRequiredFormSet(BaseFormSet):
#     def __init__(self, *args, **kwargs):
#     #    super(.__init__(*args, **kwargs)
#        super(PillarxRequiredFormSet, self).all(*args, **kwargs)
#        for form in self.forms:
#          form.empty_permitted = True
eyob =  True
EdubackgroundModelFormFormset = inlineformset_factory(

   
        PersonalInfo, Edubackground,
        fields = ('University','FieldofStudy','Degree_level','From','To','cumulative_gpa'),
        extra=0,
        min_num=1,
        formset=MinimumRequiredFormSet,

        # validate_min=True,
        widgets={

            'University': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'University',
                    'oninput':'processs(this)',
                    'required': 'true',
                    'onsubmit':'sumx(this)',

                        }
                           ),
            'FieldofStudy': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Field of Study',
                      'oninput':'processs(this)',
                    'required': 'true',
                        'onsubmit':'sumx(this)',

                }
            ),

         	'Degree_level': forms.Select(
                attrs={
                    'class': 'custom-select',
                    'placeholder': ' Degree level',
                    #   'onclick' : '
                    'required': 'true',
                    'oninput':'Filevalidationg(this, this.id)',
                     'required': 'required',
                   
                    

                },

            ),

            'From': forms.DateInput(
                attrs={
                    'class': 'form-control',
                     'required placeholder' :'YYYY/MM/DD or any other ISO date format',
                    'placeholder': 'starting date ',
               					'type':'date',
                                'oninput':'datevalid(this, this.name, this.id )',
                                   'required': 'true',
                                    'onsubmit':'sumx(this)',


                }
            ),
            'To': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'ending date ',
                       'required placeholder' :'YYYY/MM/DD or any other ISO date format',
               					'type': 'date',
                                     'oninput':'datevalidx(this, this.name, this.id )',
                                    'required': 'true',
                                       'onsubmit':'sumx(this)',
                                  
                                    

                }),


            'cumulative_gpa': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Cumulative GPA',
                 
                    'required': 'true',
                 
                    'oninput':'gpavald(this, id)',
                     
                       
                }
                )

        }

        

            )

    





LanguageSkillsModelFormFormset = inlineformset_factory(
    PersonalInfo,LanguageSkills,
    fields = ('Language', 'Writing', 'Listening', 'Speaking', 'Reading'),
    extra=0,
    formset=MinimumRequiredFormSet,
    min_num=1,
    # validate_min=True,
    
       
        widgets = {

           
            'Language': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'name': "experience-company",
                    'oninput':'process(this)',
                    'placeholder': "input the language",
                           'required': 'true',


                }
            ),
            'Writing': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Writing',
                        'required': 'true',

                }
            ),
            'Listening': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Listening',
                           'required': 'true',
                }
            ),
            'Speaking': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Speaking',
                          'required': 'true',

                }
            ),
            'Reading': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Reading',
                          'required': 'true',

                }
            ),

        }
)


ExperienceModelFormFormset = inlineformset_factory(
    PersonalInfo,Experience,
    fields = ('Company', 'Position', 'YearofExp','Start', 'End'),
    # formset=PillarxRequiredFormSet,
   
      formset=ThatForm,
    extra=0,
    min_num= 1,
    #  validate_min=True,
    widgets = {


            
            'Company': forms.TextInput(
              
                attrs={
                  
                    'class': 'form-control',
                    'placeholder': 'company Name',
                    
                      'oninput':'processs(this)',
                     'required': 'true',
                    

                }
            ),

            'Position': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Position',
                      'oninput':'processs(this)',
                       'required': 'true',
                  

                    

                }
            ),

            'YearofExp': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Year of experiance',
                   'required': 'true',
                   'readonly': 'true',
                  
                    # 'oninput':'processs(this)',


                }
            ),

            'Start': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Your email',
               					  'required placeholder' :'YYYY/MM/DD or any other ISO date format',
'type':'date',
                            'required': 'true',
                            'oninput':'expdate(this, this.name, this.id )',

                                      

                }
            ),

            'End': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'DATE',
               		  'required placeholder' :'YYYY/MM/DD or any other ISO date format',
'type':'date',
                      'required': 'true',
                    'oninput':'expdate2(this, this.name, this.id )',
                    
                }
            ),

        },
        )





class personalInfoForm(forms.ModelForm):
    

    def clean_date_of_birth(self):
            dob = self.cleaned_data['DateofBirth']
            age = (datetime.now() - dob).days/365
            if age < 18:
                raise forms.ValidationError('Must be at least 18 years old to register')
            return dob
    def clean_email(self):
            data = self.cleaned_data['email']
            if User.objects.filter(email=data).count() > 0:
              raise forms.ValidationError("We have a user with this user email-id")
            return data
    class Meta:
        model = PersonalInfo
        fields = '__all__'


        widgets = {

            'Fname': forms.TextInput(
				attrs={
					'class': 'form-control',
                    'placeholder':'First Name',
                    'oninput':'process(this)',
                          'required': 'true',
                     
                    # 'pattern':'[a-z A-Z]',
                    # 'oninvalid':"setCustomValidity('Please enter on alphabets only. ')",
                    # 'type':'text',
					}
				),           
            'Mname': forms.TextInput(
				attrs={
					'class': 'form-control',
                    'placeholder':'Middle Name',
                      'oninput':'process(this)',
                #  'pattern':'[a-z A-Z]',
                    #  'oninvalid':"setCustomValidity('Please enter on alphabets only. ')",
                      'type':'text',
                            'required': 'true',
     
					}
				),
            'Lname': forms.TextInput(
				attrs={
					'class': 'form-control',
                    'placeholder':'Last Name',
                    'oninput':'process(this)',
                    
                     
                      'type':'text',
                           'required': 'true',
     
					}
				),
            'Email': forms.EmailInput(
				attrs={
					'class': 'form-control',
                    'placeholder':'email',
                           'required': 'true',
                            'onchange':'ValidateEmail(this)',

     
					}
				),
            'PhoneNo': forms.TextInput(
				attrs={
					'class': 'form-control',
                    'placeholder':' e.g 0912369885',
                    'maxlength':'10',
                    'onchange':'phonenumber(this)',
                    'oninput':'processx(this)',
                     'pattern':'[0]{1}[9]{1}[0-9]{8}',
                    # 'onKeyPress':'return isNumberKey(event)',
                   'onKeyPress':'if(this.value.length==10) return false;',
                         'required': 'true',
                    
                    #  'pattern':"[0-9]{3}-[0-9]{3}-[0-9]{4}",
     
					}
				),
            'Nationality': forms.TextInput(
				attrs={
					'class': 'form-control',
                    'placeholder':'Nationality',
                      'oninput':'process(this)',
               
                      'type':'text',
                            'required': 'true',

     
					}
				),
          	'City': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Your City',
                    'oninput':'processs(this)',
                    'type':'text',
                         'required': 'true',

                }
            ),
            'DateofBirth': forms.DateInput(
				attrs={
					'class': 'form-control',
                    'placeholder':'birth date',
                    'type':'date',
                    'oninput':'birthdate()',
                       'required placeholder' :'YYYY/MM/DD or any other ISO date format',
                           'required': 'true',
     
					}
				),
            'PlaceofBirth': forms.TextInput(
				attrs={
					'class': 'form-control',
                    'placeholder':'birth place',
                       'oninput':'processs(this)',
                  
                      'type':'text',
                            'required': 'true',
                    
                       
     
					}
				),
            'Gender': forms.Select(
				attrs={
					'class': 'custom-select',
                    'placeholder':'Gender',
                          'required': 'true',
     
					}
				),
            'disablity':forms.CheckboxInput(
                attrs={
				
                'type':'checkbox' ,
                'class':'custom-control-input' ,
                'id':'custom_checkbox_inline_right_unchecked',
                'placeholder':'check yes if you are disable ',
                  
     
					}
                    
                    ),
            'Name': forms.TextInput(
				attrs={
					'class': 'form-control',
                    'placeholder':'Name',
                     'onchange':'simref()',
                     'oninput':'processs(this)',
                           'required': 'true',
     
					}
				),
            'PhoneNumber': forms.TextInput(
				attrs={
					'class': 'form-control',
                  'placeholder':' e.g 0912369885',
                   'onchange':'simref();phonenumber(this)',
                    'oninput':'processx(this)',
      'maxlength':'10',
    
                                        'pattern':'[0]{1}[9]{1}[0-9]{8}',
                                        'onKeyPress':'if(this.value.length==10) return false;',
                           'required': 'true',
                                'type':'tel',
                    # 'type':"tel",
                    # 'pattern':'[0-9]{3}-[0-9]{3}-[0-9]{4}',
     
					}
				),
            'EmailAdd': forms.EmailInput(
				attrs={
					'class': 'form-control',
                    'placeholder':'Email',
                     'type':'email',
                        'onchange':'ValidateEmail(this); simref()',
                   'required': 'true',
     
					}
				),                        
           
            'Name_r': forms.TextInput(
				attrs={
					'class': 'form-control',
                    'placeholder':'Name',
                     'oninput':'processs(this)',
                      'onchange':'simref1()',
                         'required': 'true',
     
					}
				),
            'PhoneNumber_r': forms.TextInput(
				attrs={
					'class': 'form-control',
              'placeholder':' e.g 0912369885',
      'maxlength':'10',
  'onchange':'simref1();phonenumber(this)',
                    'oninput':'processx(this)',
   'pattern':'[0]{1}[9]{1}[0-9]{8}',
 'onKeyPress':'if(this.value.length==10) return false;',
                          'required': 'true',
                               'type':'tel',
                    # 'type':"tel",
                    # 'pattern':'[0-9]{3}-[0-9]{3}-[0-9]{4}',
     
					}
				),
            'EmailAdd_r': forms.EmailInput(
				attrs={
					'class': 'form-control',
                    'placeholder':'Email',
                           'required': 'true',
                              'type':'email',
                              
                           'onchange':'ValidateEmail(this); simref1()',
     
					}
				),                        
            'Name_r1': forms.TextInput(
				attrs={
					'class': 'form-control',
                    'placeholder':'Name',
                     'oninput':'processs(this)',
                           'required': 'true',
                           'onchange':'simref2()',
     
					}
				),
            'PhoneNumber_r1': forms.TextInput(
				attrs={
					'class': 'form-control',
                   
                      'placeholder':' e.g 0912369885',
      'maxlength':'10',
    'onchange':'simref2();phonenumber(this)',
                    'oninput':'processx(this)',
   'pattern':'[0]{1}[9]{1}[0-9]{8}',
 'onKeyPress':'if(this.value.length==10) return false;',
                          'required': 'true',
                    'type':'tel',
                    # 'pattern':'[0-9]{3}-[0-9]{3}-[0-9]{4}',
     
					}
				),
            'EmailAdd_r1': forms.EmailInput(
				attrs={
					'class': 'form-control',
                    'placeholder':'Email',
                          'required': 'true',
                             'type':'email',
                          'onchange':'ValidateEmail(this); simref2()',
                    
                      
     
					}
				),                        
                 
            'CoverLetter': forms.Textarea(
				attrs={
					'class': 'form-control',
                    'placeholder':'cover lettter at least 150 word',
                          'required': 'true',
                    'oninput':'processs(this);coverletter(this)',
                   'onchange': 'coverletter(this)',
     
					}
				),
            'cv': forms.FileInput(
				attrs={
					'class': 'form-input-styled',
                    'placeholder':'Your File',
					'type':'file',
                    'input type':'file',
                    'onchange':'Filevalidationx()',
                    'class':'form-input-styled',
                           'required': 'true',
                     'accept':'application/pdf',
                    #  'required data-fouc':,
					},
              
    
				),                 

            'docs': forms.FileInput(
				attrs={
					'class': 'form-input-styled',
                    'placeholder':'Your File',
					'type':'file',
                     'onchange':'Filevalidationx()',
                    'input type':'file',
                    'class':'form-input-styled',
                        'required': 'true',
                      'accept':'application/pdf',
                    #  'required data-fouc':,
					},
              
    
				),   


         
                            }
    def clean(self):
     
        # data from the form is fetched using super function
        super(personalInfoForm, self).clean()
         
        # extract the username and text field from the data
        username = self.cleaned_data.get('Fname')
        text = self.cleaned_data.get('Mname')
        dob = self.cleaned_data.get('DateofBirth')
        doc = self.cleaned_data.get('docs')

        r_name = self.cleaned_data.get('Name')
        r_phone = self.cleaned_data.get('PhoneNumber')
        r_email = self.cleaned_data.get('EmailAdd')
        r1_name = self.cleaned_data.get('Name_r')
        r1_phone = self.cleaned_data.get('PhoneNumber_r')
        r1_email = self.cleaned_data.get('EmailAdd_r')
        r2_name = self.cleaned_data.get('Name_r1')
        r2_phone = self.cleaned_data.get('PhoneNumber_r1')
        r2_email = self.cleaned_data.get('EmailAdd_r1')
 
        # conditions to be met for the username length
        if len(username) < 3 and len(username) > 16:
            self._errors['Fname'] = self.error_class([
                'Minimum 4 characters required'])
        if len(text) < 3 and len(username) > 16:
            self._errors['Mname'] = self.error_class([
                'Minimum 4 characters required'])            
        age = (datetime.now().date() - dob).days/365
        if (age < 18  or age == ''):
                self._errors['DateofBirth'] = self.error_class([
                'Must be at least 18 years old to register']) 
        if (r_name == r1_name or r1_name == r2_name or r_name == r2_name):

                        self._errors['Name'] = self.error_class([
                'Name Cannot be repeated in Reference  ']) 
        if (r_email == r1_email or r1_email == r2_email or r_email == r2_email):
    
                        self._errors['EmailAdd_r'] = self.error_class([
                'Email Cannot be repeated in Reference  ']) 

        if (r_phone == r1_phone or r1_phone == r2_phone or r_phone == r2_phone):
        
                        self._errors['PhoneNumber_r1'] = self.error_class([
                'Phone Number  Cannot be repeated in Reference  ']) 

        return self.cleaned_data



class Elementary_SchoolForm(forms.ModelForm):
    class Meta:
        model = Elementary_School
        fields = '__all__'
        widgets = {
            
            
            'School_name': forms.TextInput(
				attrs={
					'class': 'form-control',
                    'placeholder':'Elementary School Name',
                      
                     'required': 'true',
                     
                    # 'pattern':'[a-z A-Z]',
                    # 'oninvalid':"setCustomValidity('Please enter on alphabets only. ')",
                    # 'type':'text',
					}
				),
            
            
            'starting_date': forms.DateInput(
				attrs={
					'class': 'form-control',
                    'placeholder':'birth date',
                    'type':'date',
                       'required placeholder' :'YYYY/MM/DD or any other ISO date format',
                        'required': 'true',
                         'oninput':'elementvalid()',
                     

     
					}
				),
            'end_date': forms.DateInput(
				attrs={
					'class': 'form-control',
                    'placeholder':'birth date',
                    'type':'date',
                      'oninput':'elementvalid1()',
                       'required placeholder' :'YYYY/MM/DD or any other ISO date format',
                        'required': 'true',
     
					}
				),
           
				
            

         
                            }






class Secondary_SchoolForm(forms.ModelForm):
    class Meta:
        model = Secondary_School
        fields = '__all__'
        widgets = {
            
            
            'School_names': forms.TextInput(
				attrs={
					'class': 'form-control',
                    'placeholder':'Secondary School Name',
                    #   'oninput':'processs(this)',
                     'required': 'required',
                     
                    # 'pattern':'[a-z A-Z]',
                    # 'oninvalid':"setCustomValidity('Please enter on alphabets only. ')",
                    # 'type':'text',
					}
				),
            
            
            'starting_dates': forms.DateInput(
				attrs={
					'class': 'form-control',
                    'placeholder':'birth date',
                    'type':'date',
                      'oninput':'elementvalid()',
                       'required placeholder' :'YYYY/MM/DD or any other ISO date format',
                        'required': 'required'
     
					}
				),
            'end_dates': forms.DateInput(
				attrs={
					'class': 'form-control',
                    'placeholder':'birth date',
                    'type':'date',
                      'oninput':'elementvalid1()',
                       'required placeholder' :'YYYY/MM/DD or any other ISO date format',
                        'required': 'required'
     
					}
				),
           
				
            

         
                            }






class Preparatory_SchoolForm(forms.ModelForm):
    class Meta:
        model = Preparatory_School
        fields = '__all__'
        widgets = {
            
            
            'School_namep': forms.TextInput(
				attrs={
					'class': 'form-control',
                    'placeholder':'Preparatory School Name',
                    #   'oninput':'processs(this)',
                     'required': 'required',
                     
                     
                    # 'pattern':'[a-z A-Z]',
                    # 'oninvalid':"setCustomValidity('Please enter on alphabets only. ')",
                    # 'type':'text',
					}
				),
            
            
            'starting_datep': forms.DateInput(
				attrs={
					'class': 'form-control',
                    'placeholder':'birth date',
                    'type':'date',
                       'required placeholder' :'YYYY/MM/DD or any other ISO date format',
                        'required': 'required',
                          'oninput':'elementvalid()',
     
					}
				),
            'end_datesp': forms.DateInput(
				attrs={
					'class': 'form-control',
                    'placeholder':'birth date',
                    'type':'date',
                       'required placeholder' :'YYYY/MM/DD or any other ISO date format',
                        'required': 'required',
                          'oninput':'elementvalid1()',
     
					}
				),
           
				
            

         
                            }








class InfoForm(forms.ModelForm):
    class Meta:
        model = History
        fields = ('status', 'comment')
      
        widgets = {
            
            

            'status': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'status'

                }
            ),
            
            
            'comment': forms.TextInput(
				attrs={
					'class': 'form-control',
                    'placeholder':'comments',
                    'rows':'5' ,
                    'cols':'5',
                    'placeholder':'comment'
     
					}
				),
          
          
                             
			}
    
# class RequestForm(forms.Form):
#         id = forms.IntegerField(required=False, widget=forms.HiddenInput())




class ApplicationForm(forms.ModelForm):
    
    class Meta:
        model = Application
        fields = '__all__'
      
        widgets = {
            
            

            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'title',
                      'required': 'true',

                }
            ),
            
            
            'postion': forms.TextInput(
				attrs={
					'class': 'form-control',
                    'placeholder':'Postion',
                      'required': 'true',
                    'rows':'5' ,
                    'cols':'5',
                    
     
					}
				),
              
            'qualifaction': forms.TextInput(
				attrs={
					'class': 'form-control',
                    'placeholder':'qualifaction',
                    'rows':'5' ,
                      'required': 'true',
                    'cols':'5',
                
     
					}
				),
            'required_experinace': forms.TextInput(
				attrs={
					'class': 'form-control',
                    'placeholder':'required experinace',
                    'rows':'5' ,
                      'required': 'true',
                    'cols':'5',
                   
     
					}
				),
                
            'description': forms.TextInput(
				attrs={
					'class': 'form-control',
                    'placeholder':'Application Details ',
                    'rows':'5' ,
                      'required': 'true',
                    'cols':'5',
                    
     
					}
				),
            'starting_date': forms.DateInput(
				attrs={
					'class': 'form-control',
                    'placeholder':'starting date of application',

                     'type':'date',
                       'required placeholder' :'YYYY/MM/DD or any other ISO date format',
                        'required': 'true',
                    'rows':'5' ,
                    'cols':'5',
                  
     
					}
				),

            'types': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Type of Applicantion',

                    'required': 'true',
                    'rows': '5',
                    'cols': '5',


                }
            ),


           
            'endingdate': forms.DateInput(
				attrs={
					'class': 'form-control',
                    'placeholder':'Application Ending Date ',
                     'type':'date',
                       'required placeholder' :'YYYY/MM/DD or any other ISO date format',
                        'required': 'required',
                    'rows':'5' ,
                    'cols':'5',
                  
     
					}
				),
          
                             
			}
    def clean(self):
         
        # data from the form is fetched using super function
        super(ApplicationForm, self).clean()
         
        # extract the username and text field from the data
        title = self.cleaned_data.get('title')
        postion = self.cleaned_data.get('postion')
        qualifaction = self.cleaned_data.get('qualifaction')
        experiance = self.cleaned_data.get('required_experinace')
        description = self.cleaned_data.get('description')
        starting_date = self.cleaned_data.get('starting_date')
        ending_date = self.cleaned_data.get('endingdate')

        if (datetime.now().date() > starting_date):
            self._errors['starting_date'] = self.error_class([
                'Application Starting Date Cant be in Past']) 
            # raise forms.ValidationError('Passwords are not the same')
        if (datetime.now().date() > ending_date):
            self._errors['ending_date'] = self.error_class([
                'Application Ending  Date Cant be in Past'])
        if (starting_date > ending_date):
            self._errors['starting_date'] = self.error_class([
                'Application starting date must cant be after ending date '])
        # return any errors if found
        return self.cleaned_data



class ExamScheduleForm(forms.ModelForm):

    class Meta:
        model = Exam_Schedule
        fields = '__all__'

        widgets = {

            
            
            
            
           

            'exam_message': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Message',
                    'required': 'true',

                }
            ),


         

            'exam_date': forms.DateInput(
                attrs={

                    'class': 'form-control',
                    'type': 'date',
                    'placeholder': 'exam date',
                    'rows': '3',
                    'required': 'true',
                    'cols': '3',
                    'placeholder': 'comment'

                }
          
            ),
            'exam_time': forms.TimeInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'description',
                    'rows': '3',
                    'type': 'time',
                    'placeholder': 'exam time',
                    'required': 'true',
                    'cols': '3',
                    'placeholder': 'comment'

                }

            ),
          
            'exam_location': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': ' exam loction',
                    'rows': '3',
                    'required': 'true',
                    'cols': '3',
                

                }

            ),
            'google_map_link': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Google Map Link',
                    'rows': '3',
                    'required': 'true',
                    'cols': '3',
                   

                }

            ),

            'application_user': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Google Map Link',
                    'rows': '3',
                    'required': 'true',
                    'cols': '3',


                }

            ),

        

        }
    
    def clean(self):
         
        # data from the form is fetched using super function
        super(ExamScheduleForm, self).clean()
         
        # extract the username and text field from the data
        message  = self.cleaned_data.get('exam_message')
        exam_date = self.cleaned_data.get('exam_date')
        exam_time = self.cleaned_data.get('exam_time')
        exam_location = self.cleaned_data.get('exam_location')
        google_map_link = self.cleaned_data.get('google_map_link')

        if (datetime.now().date() >= exam_date):
            self._errors['exam_date'] = self.error_class([
                'Exam Scheduling Date Must be after Current Date '])  
        # return any errors if found
        return self.cleaned_data


# Interview_Schedule_User
# name
# start
# end
# interview_location
# google_map_link
# history_userx_f
# application_f

class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%dT%H:%M"
        super().__init__(**kwargs)





class Interview_Schedule_User(forms.ModelForm):

        # ids = History.objects.values_list('application_id', flat=True).filter(user__pk = request.user.id).distinct() 
        # applications = Application.objects.exclude(pk__in = set(ids)) 


    class Meta:
        model = Interview_Schedule
        fields = ('name', 'start', 'end', 'history_userx_f')

        widgets = {



            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'title',
                    'required': 'true',

                }
            ),


            'start': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Interview Starting Time ',
                    'type': 'datetime-local',
                    # 'required placeholder': 'YYYY/MM/DD or any other ISO date format',
                    'required': 'required',
                    # 'rows': '3',
                    # 'cols': '3',


                }
            ),
            'end': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Interview Ending Time ',
                    'type': 'datetime-local',
                    # 'required placeholder': 'YYYY/MM/DD or any other ISO date format',
                    'required': 'required',
                    # 'rows': '3',
                    # 'cols': '3',


                }
            ),


            'history_userx_f': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Applicants',

                    'type': 'Secheduled User',
                    
                    'required': 'true',
                    # 'rows': '3',
                    # 'cols': '3',


                }
            ),









        }


    def __init__(self, *args, **kwargs):
        super(Interview_Schedule_User, self).__init__(*args, **kwargs)
        zera = Interview_Schedule.objects.all()
        ids = Interview_Schedule.objects.values_list(
            'history_userx_f', flat=True).distinct()

        self.fields['history_userx_f'].queryset = self.fields['history_userx_f'].queryset.exclude(
            pk__in=ids)

    def clean(self):

        # data from the form is fetched using super function
        super(Interview_Schedule_User, self).clean()

        # extract the username and text field from the data
        title = self.cleaned_data.get('title')
        start = self.cleaned_data.get('start')
        end = self.cleaned_data.get('end')

        if (datetime.now().date() > start):
            self._errors['start'] = self.error_class([
                'Schedule Starting Date Cant be in Past'])
            # raise forms.ValidationError('Passwords are not the same')
        if (datetime.now().date() > end):
            self._errors['end'] = self.error_class([
                'Schedule Ending  Date Cant be in Past'])
        if (start > end):
            self._errors['start'] = self.error_class([
                'Schedule starting date must cant be after ending date '])
        # return any errors if found
        return self.cleaned_data


