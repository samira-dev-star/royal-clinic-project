from django import views
from django.shortcuts import render
from .models import ServiceDiscount
from django.views import View
from apps.services.models import Services

# Create your views here.

def offers_partials(request):
    
    template_name = 'offers/partials/discount_partials.html'
    
   
    offers = ServiceDiscount.objects.all()
    
    

    context = {
        'discounts': offers,
        
    }
    return render(request, template_name, context)