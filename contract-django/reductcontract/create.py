from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    email=forms.EmailField(help_text='Required')
    crediantials=forms.CharField(initial='Viewer')

    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password1','password2']

    def clean_email(self,*args,**kwargs):
        email=self.cleaned_data['email']
        obj=User.objects.filter(email=email)
        if obj.exists():
            raise forms.ValidationError('This Email is already registered')
        return email




class UserUpdateForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','first_name','last_name','email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['images']


class contractupdateform(forms.ModelForm):
    class Meta:
        model=contractor
        fields=['first_name','last_name','role','contract_duration','start_date','finish_date','address','email','phone_number']
