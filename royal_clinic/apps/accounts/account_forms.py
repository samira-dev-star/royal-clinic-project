from django import forms
from django.forms import ModelForm
from .models import Customuser
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator,MinLengthValidator


class UserCreationForm(ModelForm):
    password1 = forms.CharField(label="Password",widget=forms.PasswordInput ,validators=[MaxLengthValidator(8),MinLengthValidator(4)])
    password2 = forms.CharField(label="RePassword",widget=forms.PasswordInput ,validators=[MaxLengthValidator(8),MinLengthValidator(4)])
    class Meta:
        model = Customuser
        fields = ['mobile_number','email','name','family','gender']
    
    def clean_password2(self):
        pass1 = self.cleaned_data['password1']
        pass2 = self.cleaned_data['password2']
        if pass1 and pass2 and pass1 != pass2 :
            raise ValidationError("رمز عبور و تکرار ان با هم مغایرت دارد")
        return pass2
    
    def save(self,commit=True):
        # commit false baes mishe user save nashe va user save nashode ro mirizim tu user
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    

from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserChangeForm(ModelForm):
    password  = ReadOnlyPasswordHashField(help_text="برای تغییر رمز عبور روی این <a href='../password'>لینک</a> کلیک کنید")
    class Meta:
        model = Customuser
        fields = ['mobile_number','password','email','name','family','gender','is_active','is_admin']
        
        