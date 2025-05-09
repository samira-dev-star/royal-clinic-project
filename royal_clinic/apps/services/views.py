from django.shortcuts import render,get_object_or_404
from .models import Services,ServiceFeatures,ServiceAdvantages,ServiceCandidateCondition,ServiceProcedures
from django.db.models import Q
from django.views import View
# Create your views here.

def render_service_related_partial(request, slug, model, template_name, context_key):
    specific_service = get_object_or_404(Services, slug=slug)
    related_objects = model.objects.filter(service=specific_service)
    return render(request, template_name, {context_key: related_objects})



# show services
def ShowServices(request):
    template_name = 'services/partials/sevices.html'
    
    services = Services.objects.filter(Q(is_available=True))
    context = {
        'services' : services
    }
    return render(request,template_name,context)




def show_service_features(request,slug):
    return render_service_related_partial(
        request,
        slug,
        ServiceFeatures,
        'services/partials/services_feature_values.html',
        'service_feature_values'
    )
    



def show_service_advantages(request, slug):
    return render_service_related_partial(
        request,
        slug,
        ServiceAdvantages,
        'services/partials/services_advantages.html',
        'service_advantages',
    )



def show_service_conditions(request, slug):
    return render_service_related_partial(
        request,
        slug,
        ServiceCandidateCondition,
        'services/partials/service_conditions.html',
        'service_conditions',
    )
    
    
# def show_service_procedures(request, slug):
#     return render_service_related_partial(
#         request,
#         slug,
#         ServiceProcedures,
#         'services/partials/service_procedures.html',
#         'service_procedures',
#     )
    
def show_service_procedures(request,slug):
    template_name = 'services/partials/service_procedures.html'
    
    service = get_object_or_404(Services,slug=slug)
    service_procedures = ServiceProcedures.objects.filter(service=service)
    
    context = {
        'service' : service,
        'service_procedures' : service_procedures,
    }
    return render(request,template_name,context)

    
    

class ShowSpecificServiceDetailsView(View):
    template_name = 'services/service_details.html'
    def get(self,request,slug):
        specific_service_clicked = get_object_or_404(Services,slug=slug)
        if specific_service_clicked.is_available:
            return render(request,self.template_name,{'specific_service_clicked':specific_service_clicked})
            
    
    
