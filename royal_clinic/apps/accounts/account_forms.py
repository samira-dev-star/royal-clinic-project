from django import forms
from django.forms import ModelForm
from .models import Customuser
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator,MinLengthValidator

# --------------------------------------------------------------------------------------------------------------------
# admin pannel forms

from django.core.exceptions import ValidationError
# Create your views here.

from django.core.exceptions import ValidationError

def validate_iranian_mobile(number):
    if number is None:
        return

    number = str(number).strip().replace(" ", "").replace("-", "")

    if not number.isdigit():
        raise ValidationError("شماره موبایل فقط باید شامل ارقام باشد.")

    if not number.startswith('09') or len(number) != 11:
        raise ValidationError("شماره موبایل باید با 09 شروع شود و دقیقاً 11 رقم باشد.")
    
    
    
    
    


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
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mobile_number'].validators.append(validate_iranian_mobile)
        
    def clean_password2(self):
        pass1 = self.cleaned_data.get('password1')
        pass2 = self.cleaned_data.get('password2')
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError('پسورد و تکرار آن باهم مغایرت دارند')
        return pass2


    

            
# -----------------------------------------------------------------------------------------------
# فرم لاگین

class LoginUserForm(forms.Form):
    mobile_number = forms.CharField(label="",
                                    error_messages={"required":"لطفا شماره موبایل خود را وارد کنید"},
                                    validators=[validate_iranian_mobile],
                                    widget=forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'09xxxxxxxxx',
                                        'type':'tel',
                                        'id':'mobile'}))
    
    
# min_length=4, 
# max_length=8, 
# اینا رو بذارم توی کرفیلد دیگه پیام های کلید دیتا ولیدیشن ارور ها رو نمایش نمیده
    password = forms.CharField(label="",
                               error_messages={"required":"لطفا پسورد خود را وارد کنید"},
                               widget=forms.PasswordInput(attrs={
                                   'class':'form-control',
                                   'placeholder':'پسوردی که باآن ثبت نام کردید را وارد کنید',
                                   'type':'password',
                                   'id':'password',
                                   }))
    
    


    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 4 :
            raise ValidationError('پسورد باید حداقل 4 کاراکتر داشته باشد')
        if len(password) > 8 :
            raise ValidationError('پسورد باید حداکثر 8 کاراکتر داشته باشد')
        return password
    
    


        
# --------------------------------------------------------------------------------------------------------

class ChangePassword(forms.Form):
    password1 = forms.CharField(
                                label='رمز عبور',
                                error_messages={"required":"لطفا پسورد خود را وارد کنید"},
                                validators=[MaxLengthValidator(8),MinLengthValidator(4)],
                                help_text='حداقل 4 کاراکتر و حداکثر 8 کاراکتر',
                                widget=forms.PasswordInput(attrs={
                                   'class':'form-control',
                                   'placeholder':'پسورد جدید را وارد کنید',
                                   'type':'password',
                                   'id':'password',
                                   }))
    
    password2 = forms.CharField(
                                label='تکرار رمز عبور',
                                error_messages={"required":"لطفا پسورد خود را مجددا وارد کنید"},
                                validators=[MaxLengthValidator(8),MinLengthValidator(4)],
                                help_text='حداقل 4 کاراکتر و حداکثر 8 کاراکتر',
                                widget=forms.PasswordInput(attrs={
                                   'class':'form-control',
                                   'placeholder':'تکرار پسورد جدید را وارد کنید',
                                   'type':'password',
                                   'id':'password',
                                   }))
                            
    
    def clean_password2(self):
        pass1 = self.cleaned_data.get('password1')
        pass2 = self.cleaned_data.get('password2')
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError('پسورد و تکرار آن باهم مغایرت دارند')
        return pass2
    

# --------------------------------------------------------------------------------------------------------

class ForgotPassword(forms.Form):
    mobile_number = forms.CharField(label="",
                                    validators=[validate_iranian_mobile],
                                    error_messages={"required":"لطفا شماره موبایل خود را وارد کنید"},
                                    widget=forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'09xxxxxxxxx',
                                        'type':'tel',
                                        'id':'mobile'}))
    
    

# --------------------------------------------------------------------------------------------------------

class VerifyForm(forms.Form):
    active_code = forms.CharField(label='',
                                  error_messages={"required":"این فیلد نمی تواند خالی باشد"},
                                  widget=forms.TextInput(attrs={'class':'form-control','placeholder':'کد دریافتی را وارد کنید'
                                })) 

# --------------------------------------------------------------------------------------------------------

