from django.shortcuts import render,redirect
from .models import Contact,WorkingTimesType1,WorkingTimeType2,ContactMessage
from .contact_forms import ContactForm
from django.contrib import messages
from apps.accounts.models import Customuser
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


def show_working_times2(request):
    template_name = 'contacts/partials/working_times2.html'
    
    working_times_data = WorkingTimesType1.objects.all()
    
    context = {
        'working_times': working_times_data,
    }
    return render(request, template_name, context)


# -----------------------------------------------------------------------

def public_user_messages(request):
    template_name = 'contacts/partials/public_user_messages.html'
    
    initial_data = {}
    if request.user.is_authenticated:
        try:
            current_user_if_logged_in = request.user
            user = Customuser.objects.get(id=current_user_if_logged_in.id)
    
            initial_data = {
                'name': user.name,
                'email': user.email,
            }
        except Customuser.DoesNotExist:
            initial_data = {}
    
     
    contact_form = ContactForm(initial=initial_data)
    context = {
        'contact_form' : contact_form,
    }
    
    
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
    
        if contact_form.is_valid():
            ContactMessage.objects.create(
                name = contact_form.cleaned_data['name'],
                email = contact_form.cleaned_data['email'],
                phone = contact_form.cleaned_data['phone'],
                message = contact_form.cleaned_data['message'],
            )

            context = {
                'contact_form' : contact_form,
            }

            messages.success(request,'پیام شما با موفقیت ثبت شد،اپراتور های ما در اولین فرصت پاسخ شما را خواهند داد')
            return redirect('main:index')

        else:
            context = {
                'contact_form' : contact_form,
            }
            messages.error(request,'یکی از اطلاعات شما نامعتبر است',context)
            return redirect('main:index')
    return render(request, template_name, context)