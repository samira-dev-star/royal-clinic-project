from django.contrib import admin

from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from .models import Customuser,RulesandRegulations

from .account_forms import UserCreationForm,UserChangeForm
# Register your models here.



class CustomUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    
    list_display = ('mobile_number','email','name','family','gender','is_active','is_admin')
    list_filter = ('is_active',"is_admin","family")
    

    fieldsets = (
        ('None' , {'fields' : ('mobile_number','password')}), 
        ('personal info' , {'fields' : ('email','name','family','gender')}),
        ('Permissions' , {'fields' : ('is_active','is_admin','is_superuser','groups','user_permissions')})
    )
    
    add_fieldsets = (
        (None , {'fields' : ('mobile_number','email','name','family','gender','password1','password2')}),
    )
    
    search_fields = ('mobile_number',)
    ordering = ('mobile_number',)
    filter_horizontal = ('groups','user_permissions')
    
    class Media:
        css = {
            'all' : ('css/admin_style_apps.css',)
        }
    
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js',
            'js/admin_script.js',
        )
    
    
admin.site.register(Customuser,CustomUserAdmin)



@admin.register(RulesandRegulations)
class RulesandRegulationsAmin(admin.ModelAdmin):
    list_display = ['registered_date','is_active']
    list_editable = ['is_active']
    
    
    
    
# --------------------------------------------------------------------------------------------

# from allauth.socialaccount.models import SocialApp

# admin.site.register(SocialApp)
