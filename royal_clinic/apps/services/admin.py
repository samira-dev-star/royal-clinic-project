from django.contrib import admin
from .models import Services,ServiceFeatures,ServiceAdvantages,ServiceCandidateCondition
from jalali_date.admin import ModelAdminJalaliMixin
from django_admin_listfilter_dropdown.filters import DropdownFilter
from django.contrib.admin import SimpleListFilter
from django.db.models import Q

# Register your models here.

# manual-custom filter
class ServicesFilter(SimpleListFilter):
    title = 'فیلتر خدمات'
    parameter_name = 'service'
    
    def lookups(self, request, model_admin):
        all_services = Services.objects.filter(Q(is_available=True))
        return [(service.id,service.service_title) for service in all_services]
    
    def queryset(self,request,queryset):
        if self.value() != None:
            return queryset.filter(Q(is_available=self.value))
        return queryset
            


# creating action
@admin.display(description='غیر فعال کردن خدمات')
def de_active_service(modeladmin,request,queryset):
    number_of_selected_records = queryset.update(is_available=False)
    message= f'تعداد {number_of_selected_records} سرویس غیرفعال شد.'
    modeladmin.message_user(request,message)
    
@admin.display(description='فعال کردن خدمات')
def active_service(modeladmin,request,queryset):
    number_of_selected_records = queryset.update(is_available=True)
    message= f'تعداد {number_of_selected_records} سرویس فعال شد.'
    modeladmin.message_user(request,message)
    

class ServiceFeatureInline(admin.StackedInline):
    model = ServiceFeatures
    extra = 3
    
class ServiceAdvantageline(admin.StackedInline):
    model = ServiceAdvantages
    extra = 3
    
class ServiceConditionInline(admin.StackedInline):
    model = ServiceCandidateCondition
    extra = 3


@admin.register(Services)
class ServicesAdmin(ModelAdminJalaliMixin , admin.ModelAdmin):
    list_display = ['service_title','slug','is_available']
    list_filter = [('service_title',DropdownFilter),('slug',DropdownFilter),('updated_at',DropdownFilter)]
    search_fields = ['service_title','slug']
    ordering = ['updated_at']
    list_editable = ['is_available',]
    actions = [de_active_service , active_service]
    inlines = [ServiceFeatureInline,ServiceAdvantageline,ServiceConditionInline]
    
# ------------------------------------------------------------------------------------------

@admin.register(ServiceFeatures)  
class ServiceFeatureAdmin(admin.ModelAdmin):
    list_display = ['service','feature_name','feature_value',]
    list_filter = [('feature_name',DropdownFilter),('feature_value',DropdownFilter)]
    search_fields = ['feature_value','feature_name']
    
    
# ------------------------------------------------------------------------------------------    

@admin.register(ServiceAdvantages)  
class ServiceAdvantagesAdmin(admin.ModelAdmin):
    list_display = ['service','advantage_name','advantage_value',]
    list_filter = [('advantage_name',DropdownFilter),('advantage_value',DropdownFilter)]
    search_fields = ['advantage_name','advantage_value']
    
# ------------------------------------------------------------------------------------------   

@admin.register(ServiceCandidateCondition)  
class ServiceCandidateConditionAdmin(admin.ModelAdmin):
    list_display = ['service','condition']
    list_filter = [('condition',DropdownFilter)]
    search_fields = ['condition']