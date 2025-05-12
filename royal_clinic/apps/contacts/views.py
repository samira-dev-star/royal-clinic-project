from django.shortcuts import render
from .models import Contact
# WorkingTimesType1,WorkingTimeType2
# Create your views here.


def show_contacts(request):
    template_name = 'contacts/partials/contacts.html'
    
    contact_data = Contact.objects.all()
    
    context = {
        'contacts': contact_data,
    }
    
    return render(request, template_name, context)


# def show_working_times1(request):
#     template_name = 'contacts/partials/working_times1.html'
    
#     working_times_data = WorkingTimesType1.objects.all()
    
#     context = {
#         'working_times': working_times_data,
#     }
#     return render(request, template_name, context)


# def show_working_times2(request):
#     template_name = 'contacts/partials/working_times2.html'
    
#     working_times_data = WorkingTimesType1.objects.all()
    
#     context = {
#         'working_times': working_times_data,
#     }
#     return render(request, template_name, context)