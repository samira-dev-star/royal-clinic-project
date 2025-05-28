from django.contrib import admin
from .models import CustomPatient,ShowPatientPanelForAdmin
from django_admin_listfilter_dropdown.filters import DropdownFilter
from django.http import HttpResponse
# Register your models here.



@admin.register(CustomPatient)
class CustomPatientAdmin(admin.ModelAdmin):
    list_display = ('user','emergency_contact','get_age','height','weight','blood_type','address')
    search_fields = ('get_age','height','weight','blood_type')
    list_filter = (('height',DropdownFilter),('weight',DropdownFilter),('blood_type',DropdownFilter))
    

@admin.register(ShowPatientPanelForAdmin)
class ShowPatientPanelForAdminAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        return super().changelist_view(request, extra_context=extra_context)
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def changelist_view(self, request, extra_context=None):
        return HttpResponse('''
                            <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Patient Panel Button</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        .btn-pulse:hover {
            animation: pulse 1.5s infinite;
        }
        
        @keyframes pulse {
            0% {
                box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.7);
            }
            70% {
                box-shadow: 0 0 0 10px rgba(99, 102, 241, 0);
            }
            100% {
                box-shadow: 0 0 0 0 rgba(99, 102, 241, 0);
            }
        }
        
        .btn-tilt {
            transition: transform 0.3s ease;
        }
        
        .btn-tilt:hover {
            transform: rotate(-2deg) scale(1.02);
        }
    </style>
</head>
<body class="bg-gray-100 min-h-screen flex items-center justify-center p-4">
    <div class="text-center">
        <h1 class="text-3xl font-bold text-lime-800 mb-6">پنل مدیریت</h1>
        
        <div class="relative inline-block group">
            <div class="absolute -inset-1 bg-gradient-to-r from-green-600 to-blue-500 rounded-lg blur opacity-25 group-hover:opacity-75 transition duration-200"></div>
            
            <a href="http://127.0.0.1:8000/patient_panel/patients_list/" 
               class="relative flex items-center justify-center px-8 py-4 bg-gradient-to-br from-green-600 to-lime-500 text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transition-all duration-300 btn-pulse btn-tilt">
                <i class="fas fa-users mr-3 text-lg"></i>
                <span class="text-lg">لیست زیبا جویان</span>
                <i class="fas fa-arrow-right ml-3 transition-transform group-hover:translate-x-1"></i>
            </a>
        </div>
        
        <p class="mt-6 text-gray-600 max-w-md mx-auto">
           برای مشاهده ی اطلاعات بیماران روی دکمه ی بالا کلیک کنید
        </p>
        
        <div class="mt-8 flex justify-center space-x-4">
            <div class="w-12 h-12 rounded-full bg-green-100 flex items-center justify-center text-green-600">
                <i class="fas fa-user-md"></i>
            </div>
            <div class="w-12 h-12 rounded-full bg-green-100 flex items-center justify-center text-green-600">
                <i class="fas fa-file-medical"></i>
            </div>
            <div class="w-12 h-12 rounded-full bg-green-100 flex items-center justify-center text-green-600">
                <i class="fas fa-chart-line"></i>
            </div>
        </div>
    </div>
</body>
</html>
                            ''')