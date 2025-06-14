from django.shortcuts import render,get_object_or_404
from .models import Services,ServiceFeatures,ServiceAdvantages,ServiceCandidateCondition,ServiceProcedures,ServiceRecurringQuestion
from django.db.models import Q
from django.views import View
from django.core.paginator import Paginator
from apps.comments_scores_favourites.models import AddScore
# Create your views here.

def render_service_related_partial(request, slug, model, template_name, context_key):
    specific_service = get_object_or_404(Services, slug=slug)
    related_objects = model.objects.filter(service=specific_service)
    return render(request, template_name, {context_key: related_objects})



# show services
def ShowServices(request):
    template_name = 'services/partials/sevices.html'
    
    services = Services.objects.filter(Q(is_available=True))[:6]
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
    
    

    
def show_service_procedures(request,slug):
    template_name = 'services/partials/service_procedures.html'
    
    service = get_object_or_404(Services,slug=slug)
    service_procedures = ServiceProcedures.objects.filter(service=service)
    
    context = {
        'service' : service,
        'service_procedures' : service_procedures,
    }
    return render(request,template_name,context)

    
# find other related services:
def show_other_services(request, slug):
    template_name = 'services/partials/sevices.html'
    current_service = get_object_or_404(Services, slug=slug)
    
    related_services = Services.objects.filter(Q(is_available=True) & ~Q(slug=current_service.slug))[:3]
    
    context = {
        'services': related_services,
    }
    
    return render(request, template_name, context)



def service_repetative_questions(request,slug):
    return render_service_related_partial(
        request,
        slug,
        ServiceRecurringQuestion,
        'services/partials/service_recurring_questions.html',
        'service_questions',
    )



class ShowSpecificServiceDetailsView(View):
    template_name = 'services/service_details.html'
    def get(self,request,slug):
        specific_service_clicked = get_object_or_404(Services,slug=slug)
        
        if request.user.is_authenticated:
            scores_and_ideas = AddScore.objects.filter(Q(user=request.user) & Q(service=specific_service_clicked)).first()
        else:
            scores_and_ideas = AddScore.objects.filter(Q(service=specific_service_clicked)).first()
        
        
        if specific_service_clicked.is_available:
            return render(request,self.template_name,{'specific_service_clicked':specific_service_clicked,'scores_and_ideas':scores_and_ideas})
            
    
    
class ShowAllServicesView(View):
    template_name = 'services/all_services.html'
    
    def get(self,request):
        services = Services.objects.filter(is_available=True)
        
        paginator = Paginator(Services.objects.filter(is_available=True), 9)
        current_page = request.GET.get('page')
        page_obj = paginator.get_page(current_page)
        
        
        context = {
            'services':page_obj.object_list,
            'page_obj':page_obj,
        }
        
        return render(request,self.template_name,context)
    
    
# --------------------------------------------------------------

class ShowDiscounts(View):
    template_name = 'offers/discounts.html'
    def get(self, request):
        services = Services.objects.all()
        discounts = [services for services in services if services.has_discount]
        context = {
            'discounts': discounts
        }
        return render(request, self.template_name, context)