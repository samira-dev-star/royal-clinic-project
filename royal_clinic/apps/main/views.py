from django.shortcuts import render
from django.conf import settings
from apps.services.models import Services

# Create your views here.

def media_admin(request):
    return {"media_url" : settings.MEDIA_URL}


def index(request):
    services = Services.objects.all()
    context = {
        "services" : services
    }
    return render(request,'main/index.html',context)

