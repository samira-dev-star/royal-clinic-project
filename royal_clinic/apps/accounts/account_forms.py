from django import forms
from django.forms import ModelForm
from .models import Customuser
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator,MinLengthValidator

# --------------------------------------------------------------------------------------------------------------------
# admin pannel forms

from django.core.exceptions import ValidationError
# Create your views here.

def normalize_iranian_mobile(number):
    if number is None:
        return number
        
    # حذف فاصله‌ها و نویسه‌های غیرضروری
    number = str(number).strip().replace(" ", "").replace("-", "").replace("+", "")
    
    # حذف پیشوند 0 اگر وجود دارد
    if number.startswith('0'):
        number = number[1:]
    
    # افزودن پیشوند 98 اگر وجود ندارد
    if not number.startswith('98'):
        number = '98' + number
    
    # حذف 98 اضافی در ابتدا
    if number.startswith('9898'):
        number = '98' + number[4:]
    
    # اطمینان از طول 12 رقمی (98 + 10 رقم)
    if len(number) != 12:
        raise ValidationError("شماره موبایل باید ۱۰ رقم (بدون پیشوند) باشد")
    
    return number


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
    
    
    
    def clean_mobile_number(self):
       try:
           mobile = self.cleaned_data['mobile_number']
           return normalize_iranian_mobile(mobile)
       except ValidationError as e:
           raise ValidationError(e.message)
       
       
    
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
        pass1 = self.cleaned_data.get('password1')
        pass2 = self.cleaned_data.get('password2')
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError('پسورد و تکرار آن باهم مغایرت دارند')
        return pass2


    def clean_mobile_number(self):
        mobile = self.cleaned_data['mobile_number']
        try:
            # استفاده از تابع یکسان برای نرمال‌سازی
            return normalize_iranian_mobile(mobile)
        except ValidationError as e:
            raise ValidationError(e.message)

            
# -----------------------------------------------------------------------------------------------
# فرم لاگین

class LoginUserForm(forms.Form):
    mobile_number = forms.CharField(label="",
                                    error_messages={"required":"لطفا شماره موبایل خود را وارد کنید"},
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
    
    def clean_mobile_number(self):
        number = self.cleaned_data.get('mobile_number')
        if not number:
            raise ValidationError("شماره موبایل نمی‌تواند خالی باشد.")
        try:
            # استفاده از تابع یکسان برای نرمال‌سازی
            normalized = normalize_iranian_mobile(number)
            # اگر شماره با 98 شروع شد، به فرمت 09 برگردان برای سازگاری با دیتابیس
            if normalized.startswith('98'):
                normalized = '0' + normalized[2:]
            return normalized
        except ValidationError as e:
            raise ValidationError(e.message)



        
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
                                    error_messages={"required":"لطفا شماره موبایل خود را وارد کنید"},
                                    widget=forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'09xxxxxxxxx',
                                        'type':'tel',
                                        'id':'mobile'}))
    
    
    def clean_mobile_number(self):
        number = self.cleaned_data.get('mobile_number')

        if " " in number:
            raise ValidationError("شماره موبایل نباید فاصله داشته باشد.") 

        if not number.replace('+', '').isdigit():
            raise ValidationError("شماره موبایل فقط باید شامل عدد باشد.")

        if not (number.startswith('09') or number.startswith('+989') or number.startswith('989')):
            raise ValidationError("شماره موبایل باید با 09 یا +989 یا 989 شروع شود.")

        # تبدیل به فرمت بین‌المللی
        if number.startswith('09'):
            number = '+98' + number[1:]  # 0912... => +98912...
        elif number.startswith('989'):
            number = '+' + number  # 98912... => +98912...
        
        # بررسی طول
        if len(number) != 13:
            raise ValidationError("تعداد ارقام شماره موبایل صحیح نمی‌باشد.")

        return number
    
# --------------------------------------------------------------------------------------------------------

class VerifyForm(forms.Form):
    active_code = forms.CharField(label='',
                                      error_messages={"required":"این فیلد نمی تواند خالی باشد"},
                                      widget=forms.TextInput(attrs={'class':'form-control','placeholder':'کد دریافتی را وارد کنید'})) 

# --------------------------------------------------------------------------------------------------------

