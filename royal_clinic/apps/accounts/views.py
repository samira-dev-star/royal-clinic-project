from django.shortcuts import render,redirect
from django.views import View
from .account_forms import RegisterUserForm,LoginUserForm,ChangePassword,ForgotPassword,VerifyForm
from .models import Customuser,RulesandRegulations,ActivationCode
from django.contrib import messages
from apps.patient_panel.models import CustomPatient,DrRecommendations
from apps.reservation.models import ReserveAppointment
from apps.contact.models import Contact
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.aggregates import Count
from django.db.models import Q
# Create your views here.


class RegisterUserView(View):
    template_name = 'accounts/register.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request,'شما در حال حاضر لاگین هستید و نمی توانید مجددا ثبت نام کنید','info')
            return redirect("main:index")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request,*args, **kwargs):
        form = RegisterUserForm()
        return render(request,self.template_name,{'form':form})
    
    def post(self,request,*args, **kwargs):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data
            
            if user['accept_rules']:
            
                new_user = Customuser.objects.create_user (
                    mobile_number = user['mobile_number'],
                    password = user['password1'],
                )
                
                # request.session['current_user'] = {
                #     'mobile_number' : user['mobile_number'],
                #     'password' : user['password1'],
                # }
                
                
                messages.success(request,"ثبت نام با موفقیت انجام شد برای ورود شماره موبایل و پسورد خود را وارد کنید",'success')
                new_user.is_active = True
                new_user.save()
                return redirect('main:index')
            
            
                
            else:
                messages.error(request,'با قوانین و مقررات موافقت نکردید','error')
                return render(request,self.template_name,{'form':form})
                 
        messages.error(request,' خطا در انجام ثبت نام','error')
        return render(request,self.template_name,{'form':form})    
            
            
#----------------------------------------------------------------------------------------------------------------        
        
def show_rules_and_regulations(request):
    template_name = "accounts/partials/rules_and_regulations.html"
    rules = RulesandRegulations.objects.all()
    context = {
        'rules' : rules,
    }
    return render(request,template_name,context)

#----------------------------------------------------------------------------------------------------------------

# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip

# ورود کاربر
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login,logout,authenticate
            
class LoginUser(View):
    template_name = "accounts/login.html"
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request,'شما در حال حاضر لاگین هستید و نمی توانید دوباره لاگین کنید','info')
            return redirect("main:index")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        initial_dict = {}
        if 'remember_mobile' in request.COOKIES:
            initial_dict['mobile_number'] = request.COOKIES['remember_mobile']
        else:
            form = LoginUserForm()
        form = LoginUserForm(initial=initial_dict)
        return render(request, self.template_name, {'form': form})  

        
    
    def post(self, request, *args, **kwargs):
        form = LoginUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # print(data['mobile_number']) # تست
            user = authenticate(
                username=data['mobile_number'],  # مطمئن شوید USERNAME_FIELD='mobile_number' در مدل کاربر
                password=data['password']
            )
            if user is not None:
                if user.is_admin:  # اگر is_admin نشاندهنده کاربر مدیر است
                    messages.error(request, 'کاربر ادمین نمی‌تواند از این فرم وارد شود', 'error')
                    return render(request, self.template_name, {'form': form})
                

                messages.success(request, 'حساب کاربری شما فعال شد', 'success')
                login(request, user)
                
                # امنیت
                # request.session['ip_address'] = get_client_ip(request)
                # request.session['user_agent'] = request.META.get('HTTP_USER_AGENT')
                
                # بررسی شرط قبل انتقال کاربر به صفحه ی بعدی
                if not request.POST.get('remember_me'):
                    request.session.set_expiry(0)
                else:
                    # اگر تیک خورده بود، session برای 2 هفته فعال باشد
                    request.session.set_expiry(1209600)  
                    
                    # print(request.session.get_expiry_age())
                    # print(request.session.get_expiry_date())
                    next_url = request.GET.get('next', 'main:index') 
                    response = redirect(next_url)
                    response.set_cookie('remember_mobile', data['mobile_number'], max_age=1209600)
                    response.set_cookie('remember_password', data['password'], max_age=1209600)
                    return response
                
                
                
                next_url = request.GET.get('next', 'main:index')  # پیشفرض به صفحه اصلی
                return redirect(next_url)
                
            
            
            else:
                messages.error(request, 'شماره موبایل یا رمز عبور اشتباه است', 'error')
                return render(request, self.template_name, {'form': form})
        else:
            messages.error(request, 'لطفا اطلاعات را به درستی وارد کنید', 'error')
            return render(request, self.template_name, {'form': form})
        


#----------------------------------------------------------------------------------------------------------------
# خروج - logout

class LogoutUserView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request,'شما در حال حاضر لاگین نمی باشید برای ورود فرم لاگین را پر کنید','info')
            return redirect("account:login")
        
        return super().dispatch(request, *args, **kwargs)
    def get(self,request,*args, **kwargs):
        logout(request)
        messages.success(request,'از حساب کاربری خود خارج شدید','success')
        return redirect('main:index')
    
    
#----------------------------------------------------------------------------------------------------------------
# user_panel

class UserPanelView(View,LoginRequiredMixin):
    template_name = 'accounts/user_panel.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_admin:
            messages.warning(request,'شما مدیر سایت هستید و نمی توانید دسترسی به پنل کاربری داشته باشید','warning')
            return redirect("main:index")
        if not request.user.is_authenticated:
            messages.info(request,'شما در حال حاضر لاگین نمی باشید برای دسترسی به پنل کاربری وارد شوید','warning')
            return redirect("account:login")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request,*args, **kwarg):
        current_user = request.user
        
        try:
            patient_data = CustomPatient.objects.get(user=request.user)
        except CustomPatient.DoesNotExist:
            patient_data = None
        
        # شمردن تعداد نوبت هایی که فعال هستند
        # annotate : اضافه کردن یک فیلد جدید واسه شمارش
        # order_by : مرتب سازی بر حسب - برعکس جدید به قدیم
        # [:3] : تای اول 3
        reservations = ReserveAppointment.objects.filter(Q(user=current_user) & Q(is_confirmed=True)).annotate(
            reservation_count=Count('id')
        ).order_by("-created_at")[:3]
        
        contacts = Contact.objects.all()
        
        recommended_services = DrRecommendations.objects.filter(patient=patient_data)
        
        context = {
            'patient_data':patient_data,
            'reservations':reservations,
            'current_user':current_user,
            'contacts':contacts,
            'recommended_services':recommended_services,
        }
        
        return render(request,self.template_name,context)
    
#----------------------------------------------------------------------------------------------------------------
# Forgot Password

from utils import random_code_generatore,send_sms


class ForgotPasswordView(View):
    template_name = 'accounts/forgot_password.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("main:index")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request,*args, **kwarg):
        form = ForgotPassword()
        return render(request,self.template_name,{'form':form})
    def post(self,request,*args, **kwarg):
        form = ForgotPassword(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            
            try:
                current_user = Customuser.objects.get(mobile_number = data['mobile_number'])
 
                active_code = random_code_generatore(6)
                current_user_activation_code = ActivationCode.objects.create(
                    user = current_user,
                    code = active_code,
                )
                current_user_activation_code.save()

                send_sms(data['mobile_number'],f'کد ارسال شده را برای تغییر رمز عبور وارد کنید . کد شما :{active_code}')
                request.session['user_session'] = {
                    'active_code' : str(active_code),
                    'mobile_number' : data['mobile_number'],
                    'remember_password' : True,
                }
                messages.success(request,f'{active_code}جهت تغییر رمز عبور کد دریافتی را ارسال کنید:کدفعال سازی','success')
                return redirect('account:verifypass')
            
            except Customuser.DoesNotExist:
                messages.error(request, 'کاربری با این شماره موبایل یافت نشد')
                return render(request,self.template_name,{'form':form})
            
            
        
#----------------------------------------------------------------------------------------------------------------            
class VerifyUserView(View):
    template_name = 'accounts/verify_user.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("main:index")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = VerifyForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = VerifyForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            user_session = request.session.get('user_session')
            if not user_session:
                messages.error(request, 'دسترسی غیرمجاز! لطفاً مجدداً تلاش کنید.')
                return redirect('account:forgotpass')

            # مطمئن شو کد وارد شده با کد داخل سشن برابره
            if data['active_code'] != user_session.get('active_code'):
                messages.error(request, 'کد اعتبارسنجی اشتباه است.')
                return render(request, self.template_name, {'form': form})

            try:
                code_instance = ActivationCode.objects.filter(
                    user__mobile_number=user_session['mobile_number'],
                    code=data['active_code'],
                    is_used=False,
                ).latest('created_at')

            except ActivationCode.DoesNotExist:
                messages.error(request, 'کد وارد شده صحیح نیست یا قبلاً استفاده شده.')
                return render(request, self.template_name, {'form': form})

            # بررسی انقضا
            if code_instance.is_expired():
                messages.error(request, 'کد وارد شده منقضی شده است. لطفاً مجدداً درخواست دهید.', 'error')
                return redirect('account:forgotpass')

            # موفقیت در اعتبارسنجی
            code_instance.is_used = True
            code_instance.save()

            if user_session.get('remember_password') is True:
                messages.success(request, 'کد تایید شد. لطفاً رمز عبور جدید را وارد کنید.', 'success')
                return redirect('account:changepass')

            # fallback در صورتی که remember_password نباشه
            messages.info(request, 'کد تایید شد.')
            return redirect('account:login')  # یا مسیر دیگه‌ای که مدنظرته

        # اگر فرم نامعتبر بود
        messages.error(request, 'اطلاعات وارد شده نامعتبر است.')
        return render(request, self.template_name, {'form': form})


#----------------------------------------------------------------------------------------------------------------
# change password

class ChangePasswordView(View):
    template_name = 'accounts/change_password.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("main:index")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request,*args, **kwarg):
        form = ChangePassword()
        return render(request,self.template_name,{'form':form})
    
    def post(self,request,*args, **kwarg):
        form = ChangePassword(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user_session = request.session['user_session']
            user = Customuser.objects.get(mobile_number=user_session['mobile_number'])
            
            user.set_password(data['password1'])
            user.save()
            
            messages.success(request,'رمز عبور شما با موفقیت تغییر کرد','success')
            return redirect('account:login')
        else:
            messages.error(request,'اطلاعات وارد شده معتبر نمی باشد','danger')
            return render(request,self.template_name,{'form':form})