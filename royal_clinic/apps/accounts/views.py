from django.shortcuts import render,redirect
from django.views import View
from .account_forms import RegisterUserForm,LoginUserForm
from .models import Customuser,RulesandRegulations
from django.contrib import messages
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
            return redirect("main:index")
        
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
        if not request.user.is_authenticated:
            messages.info(request,'شما در حال حاضر لاگین نمی باشید برای دسترسی به پنل کاربری وارد شوید','warning')
            return redirect("account:login")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request,*args, **kwarg):
        return render(request,self.template_name)
    
