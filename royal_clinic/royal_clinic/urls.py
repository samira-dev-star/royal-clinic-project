"""
URL configuration for royal_clinic project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('apps.main.main_urls' , namespace='main')),
    path('accounts/',include('apps.accounts.account_urls', namespace='account')),
    path('services/',include('apps.services.services_urls', namespace='services')),
    path('user_services/',include('apps.user_services.user_services_urls', namespace='user_services')),
    path('csf/', include('apps.comments_scores_favourites.csf_urls' , namespace='csf')),
    path('contact/', include('apps.contact.contact_urls' , namespace='contact')),
    path('patient_panel/', include('apps.patient_panel.patient_panel_urls' , namespace='patient')),
    path('reservation/', include('apps.reservation.reservation_urls' , namespace='reservation')),
    path('realtime_chat/', include('apps.realtime_chat.realtime_chat_urls' , namespace='realtime_chat')),
    path('search/',include('apps.search.search_urls' , namespace='search')),
    path('personel/',include('apps.personel.personel_urls',namespace='personel')),
    path('offers/',include('apps.offers.offers_urls',namespace='offers')),
    path('gallery/',include('apps.gallery.gallery_urls',namespace='gallery')),
    # path('error_handlers/',include('apps.error_handlers.urls',namespace='error_handlers')),
    
    
    path('ckeditor/', include('ckeditor_uploader.urls')),
    
    
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)






admin.site.site_header = 'پنل مدیریت کلینیک رویال'
admin.site.site_title = 'Royal Clinic'
admin.site.index_title = 'Royal Clinic'


handler404 = 'apps.error_handlers.views.error_404'
handler400 = 'apps.error_handlers.views.error_400'
handler403 = 'apps.error_handlers.views.error_403'
handler500 = 'apps.error_handlers.views.error_500'