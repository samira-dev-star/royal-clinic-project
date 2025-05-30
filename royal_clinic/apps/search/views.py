from django.shortcuts import render
from django.views import View
from django.db.models import Q

from apps.services.models import Services
from apps.personel.models import Personel



# Create your views here.

class SearchResultsView(View):
    def get(self,request,*args, **kwargs):
        query = request.GET.get("q")
        
        services = Services.objects.filter(
            Q(service_title__icontains=query)|
            Q(service_short_description__icontains=query)|
            Q(service_description__icontains=query)|
            Q(slug__icontains=query)|
            Q(is_available__icontains=query)|
            Q(procedure_description__icontains=query)
        )
        
        personels = Personel.objects.filter(
            Q(name_and_family__icontains=query)|
            Q(profession__icontains=query)|
            Q(description__icontains=query)
        )
        
        context = {
            
            "services" : services,
            "personels" : personels,
        }
        
        return render(request,"search/search.html",context)