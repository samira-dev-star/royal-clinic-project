from django.shortcuts import render
from django.conf import settings
from apps.services.models import Services
from apps.contact.models import Contact
from .models import Sliders,SocialMediaAddresses
from django.db.models import Q


# Create your views here.

def media_admin(request):
    return {"media_url" : settings.MEDIA_URL}


def index(request):
    services = Services.objects.all()
    contacts = Contact.objects.all()
    sliders = Sliders.objects.filter(Q(is_active=True))
    
    context = {
        "services" : services,
        "contacts" : contacts,
        "sliders" : sliders,
    }
    return render(request,'main/index.html',context)



def social_media_links(request):
    social_media = SocialMediaAddresses.objects.filter(is_active=True)
    return {'social_media': social_media}



def contact_with_us(request):
    contacts = Contact.objects.all()
    return {'contacts': contacts}
