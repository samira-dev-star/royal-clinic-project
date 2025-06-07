from django.shortcuts import render
from django.conf import settings
from apps.services.models import Services
from apps.contact.models import Contact
from .models import Sliders,SocialMediaAddresses
from django.db.models import Q
from apps.offers.models import ServiceDiscount

from apps.comments_scores_favourites.models import AddScore
from apps.patient_panel.models import CustomPatient


# Create your views here.

def media_admin(request):
    return {"media_url" : settings.MEDIA_URL}


def index(request):
    services = Services.objects.all()
    contacts = Contact.objects.all()
    sliders = Sliders.objects.filter(Q(is_active=True))
    
    scores_and_ideas = AddScore.objects.all()
    
    # image_list = []
    
    # for user in scores_and_ideas:
    #    images = CustomPatient.objects.get(user=user.user) 
    #    image_list.append(images.image_name.url)
    
    
    context = {
        "services" : services,
        "contacts" : contacts,
        "sliders" : sliders,
        
        "scores_and_ideas" : scores_and_ideas,
        # "image_list" : image_list
        
    }
    return render(request,'main/index.html',context)



def social_media_links(request):
    social_media = SocialMediaAddresses.objects.filter(is_active=True)
    return {'social_media': social_media}



def contact_with_us(request):
    contacts = Contact.objects.all()
    return {'contacts': contacts}


def discount(request):
    offers = ServiceDiscount.objects.all()
    return {'offers': offers}
