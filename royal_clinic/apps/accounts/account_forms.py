from django import forms
from django.forms import ModelForm
from .models import Customuser
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator,MinLengthValidator

# --------------------------------------------------------------------------------------------------------------------
# admin pannel forms

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
        
        
        
# -----------------------------------------------------------------------------------------------
# Register user form
class RegisterUserForm(ModelForm):
    password1 = forms.CharField(label='رمز عبور',widget=forms.PasswordInput(attrs={'class':'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 form-input','placeholder':'پسورد خود را وارد کنید'}),validators=[MaxLengthValidator(8),MinLengthValidator(4)],help_text='حداقل 4 کاراکتر و حداکثر 8 کاراکتر')
    password2 = forms.CharField(label='تکرار رمز عبور',widget=forms.PasswordInput(attrs={'class':'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 form-input','placeholder':'تکرار پسورد خود را وارد کنید'}),validators=[MaxLengthValidator(8),MinLengthValidator(4)])
    

    accept_rules = forms.BooleanField(
    label='',
    required=True,
    widget=forms.CheckboxInput(attrs={
        'id': 'terms',
        'name': 'terms',
        'type': 'checkbox',
        'class': 'w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-emerald-300'
    })
)


    class Meta:
        model = Customuser
        fields = ['mobile_number',]
        widgets = {
            'mobile_number' : forms.TextInput(attrs={'class':'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 form-input','placeholder':'شماره تماس خود را وارد کنید'})
        }
        
    def clean_password2(self):
        pass1 = self.cleaned_data['password1']
        pass2 = self.cleaned_data['password2']
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError('پسورد و تکرار آن باهم مغایرت دارند')
        return pass2
    
    def clean_mobile_number(self):
        mobile = self.cleaned_data['mobile_number'].strip().replace(" ", "")
        if mobile.startswith('0'):
            mobile = mobile[1:]
        if not mobile.startswith('98') and not mobile.startswith('+98'):
            mobile = '+98' + mobile
        elif mobile.startswith('98'):  # بدون + اگر وارد شده باشه
            mobile = '+' + mobile
        return mobile

            
# -----------------------------------------------------------------------------------------------
