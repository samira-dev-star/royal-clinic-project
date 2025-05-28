from django.shortcuts import render,redirect
from django.views import View
from django.db.models import Q
from apps.patient_panel.models import CustomPatient

# Create your views here.

class SearchResultsView(View):
    def get(self,request,*args, **kwargs):
        query = request.GET.get("q")
        patients = CustomPatient.objects.filter(
            Q(emergency_contact__icontains=query)
        )
        context = {
            "patients":patients,
        }
        
        return render(request,"search/search.html",context)