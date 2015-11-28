#files.py
import re
from django import forms
from .models import Memory
from django.utils.translation import ugettext_lazy as _


class RegistrationForm(forms.Form):
 
    username = forms.CharField(label="username", max_length=100)
    # if not User.objects.filter(username).exists():
    #     raise forms.ValidationError(_("The username already exists. Please try another one."))
    # pass  
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("email"))
    password = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("password"))
    #password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password (again)"))
 
    # def clean_username(self):
    #     try:
    #         user = User.objects.get(self.cleaned_data['username'])
    #     except User.DoesNotExist:
    #         return username
    #     raise forms.ValidationError(_("The username already exists. Please try another one."))
    # #class LoginForm(forms.Form)
    # def clean(self):
    #     if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
    #         if self.cleaned_data['password1'] != self.cleaned_data['password2']:
    #             raise forms.ValidationError(_("The two password fields did not match."))
    #     return self.cleaned_data

class BioForm(forms.Form):
    bioTextArea = forms.CharField(label='BioTextArea', max_length=100)