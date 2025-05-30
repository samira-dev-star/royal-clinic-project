from django import template
from django.shortcuts import render
from django.views import View
from .models import Personel
from django.core.paginator import Paginator

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
        
        paginator = Paginator(personels, 9)  # Show 4 contacts per 
        current_page = request.GET.get('page')
        page_obj = paginator.get_page(current_page)
        
        context = {
            'personels': page_obj.object_list,
            'page_obj': page_obj,
        }
        return render(request, self.template_name, context)