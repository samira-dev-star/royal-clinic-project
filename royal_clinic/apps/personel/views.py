from django import template
from django.shortcuts import render
from django.views import View
from .models import Personel

# Create your views here.



def personels(request):
    template_name = 'personel/partials/personel_box.html'
    
    personels = Personel.objects.all()[:4]
    
    context = {
        'personels': personels,
    }
    return render(request,template_name, context)


class ShowPersonel(View):
    template_name = 'personel/personels.html'
    def get(self, request):
        personels = Personel.objects.all()
        context = {
            'personels': personels,
        }
        return render(request, self.template_name, context)