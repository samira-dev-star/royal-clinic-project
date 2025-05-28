from django.shortcuts import render,redirect
from django.views import View
from django.db.models import Q
from apps.patient_panel.models import CustomPatient
from apps.services.models import Services


# Create your views here.

class SearchResultsView(View):
    def get(self,request,*args, **kwargs):
        query = request.GET.get("q")
        patients = CustomPatient.objects.filter(
            Q(emergency_contact__icontains=query)
        )
        services = Services.objects.filter(
            Q(service_title__icontains=query)|
            Q(service_short_description__icontains=query)|
            Q(service_description__icontains=query)|
            Q(slug__icontains=query)|
            Q(is_available__icontains=query)|
            Q(procedure_description__icontains=query)
        )
        context = {
            "patients" : patients,
            "services" : services,
        }
        
        return render(request,"search/search.html",context)