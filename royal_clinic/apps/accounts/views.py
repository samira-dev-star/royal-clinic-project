from django.shortcuts import render,redirect
from django.views import View
from .account_forms import RegisterUserForm
from .models import Customuser,RulesandRegulations
from django.contrib import messages
# Create your views here.


class RegisterUserView(View):
    template_name = 'accounts/register.html'
    
    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         return redirect('main:index')
    #     return super().dispatch(request, *args, **kwargs)
    
    def get(self,request,*args, **kwargs):
        form = RegisterUserForm()
        return render(request,self.template_name,{'form':form})
    
    def post(self,request,*args, **kwargs):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data
            
            if user['accept_rules']:
            
                Customuser.objects.create_user (
                    mobile_number = user['mobile_number'],
                    password = user['password1'],
                )
                
                messages.success(request,"ثبت نام با موفقیت انجام شد برای ورود شماره موبایل و پسورد خود را وارد کنید",'success')
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