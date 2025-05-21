from django.views import View
from django.shortcuts import render, redirect
from .models import ReserveAppointment
from .reservation_forms import ReserveAppointmentForm,ReserveAppointmentForm2
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from apps.services.models import Services
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages

from jdatetime import date as jdate
from datetime import timedelta,datetime

from django.urls import reverse
from django.http import JsonResponse, HttpResponse


def reservation(request, *args, **kwargs):
    template_name = 'appointment_reservation/partials/appointment_form.html'
    service = None
    date_choices = []
    service_id = request.POST.get('service') if request.method == 'POST' else request.GET.get('service_id')

    if service_id:
        try:
            service = Services.objects.get(id=service_id)
            start = service.start_reservation_date
            end = service.finish_reservation_date
            if start and end and start <= end:
                current_date = start.date() if isinstance(start, datetime) else start
                end_date = end.date() if isinstance(end, datetime) else end
                while current_date <= end_date:
                    date_choices.append((
                        current_date.strftime("%Y-%m-%d"),
                        jdate.fromgregorian(date=current_date).strftime("%Y-%m-%d")
                    ))
                    current_date += timedelta(days=1)
            else:
                messages.warning(request, "محدوده تاریخ معتبر نیست.")
        except Services.DoesNotExist:
            messages.error(request, "سرویس یافت نشد.")
            service = None

    if request.method == 'POST':
        form = ReserveAppointmentForm(request.POST, user_instance=request.user, date_choices=date_choices)
        if form.is_valid():
            try:
                reservation_obj = form.save(commit=False)
                reservation_obj.user = request.user
                reservation_obj.save()
                
                # در صورت درخواست Ajax، به جای بازگرداندن فرم جدید، یک redirect_url ارسال می‌کنیم.
                if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'success',
                        'redirect_url': reverse('main:index')
                    })
                
                messages.success(request, "✅ نوبت شما با موفقیت ثبت شد.")
                return redirect('main:index')
            except Exception as e:
                if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'error', 'message': f'❌ خطا در ذخیره‌سازی: {str(e)}'})
                messages.error(request, f"❌ خطا در ذخیره‌سازی: {str(e)}")
        else:
            # ارسال خطاها به صورت JSON در درخواست Ajax
            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                errors = {field: error_list for field, error_list in form.errors.items()}
                return JsonResponse({'status': 'error', 'errors': errors})
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    if request.method == 'POST':
        try:
            # ... کد پردازش فرم و ذخیره داده‌ها ...
            return JsonResponse({
                'status': 'success',
                'message': '✅ اطلاعات با موفقیت ثبت شد!',
                'redirect_url': reverse('main:index')
            }, status=200)  # کد وضعیت 200 برای موفقیت
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'❌ خطا: {str(e)}'
            }, status=400)
    else:
        # sending data to frorms from view
        form = ReserveAppointmentForm(user_instance=request.user, initial={'service': service_id}, date_choices=date_choices)

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        rendered_html = render_to_string('appointment_reservation/partials/date_dropdown.html', {
            'form': form,
            'date_choices': date_choices
        }, request=request)
        return JsonResponse({'form_html': rendered_html})

    return render(request, template_name, {'form': form, 'service': service})



# --------------------------------------------------------------------------------------------------------------------------------
from django.contrib.auth.mixins import LoginRequiredMixin


# class AppointmentReservationView(LoginRequiredMixin, View):
#     template_name = 'appointment_reservation/appointment_reservation_page.html'
    
#     def get(self, request, *args, **kwargs):
#         # take data from ajax
#         service_id = request.GET.get('service_id')
#         date_choices=[]
        
#         if service_id:
#             try:
#                 service = Services.objects.get(id=service_id)
#                 start = service.start_reservation_date
#                 end = service.finish_reservation_date
#                 if start and end and start <= end:
#                     current_date = start.date() if isinstance(start, datetime) else start
#                     end_date = end.date() if isinstance(end, datetime) else end
#                     while current_date <= end_date:
#                         date_choices.append((
#                             current_date.strftime("%Y-%m-%d"),
#                             jdate.fromgregorian(date=current_date).strftime("%Y-%m-%d")
#                         ))
#                         current_date += timedelta(days=1)
#             except Services.DoesNotExist:
#                 messages.error(request, "سرویس یافت نشد.")
#                 service = None
#         else:
#             service = None
        
        
        
#         form = ReserveAppointmentForm(
#             user_instance = request.user,
#             initial={'service': service_id}, 
#             date_choices=date_choices
#         )
#         context = {
#             'form':form,
#             'date_choices': date_choices,
#             'service': service,

#         }
#         return render(request, self.template_name, context)
    
#     def post(self, request, *args, **kwargs):
#         form = ReserveAppointmentForm(request.POST, user_instance=request.user, date_choices=kwargs.get('date_choices') or [])

        
#         context = {
#             'form':form,
            
#         }
        
#         if form.is_valid():
#             reservation_obj = form.save(commit=False)
#             reservation_obj.user = request.user
#             reservation_obj.save()
        
#             form.save()
#             messages.success(request, "رزرو با موفقیت انجام شد.", 'success')
#             return render(request, self.template_name, {'form':form})
#         else:
            
            
            
#             messages.error(request, "رزرو با خطا مواجه شد.", 'error')
#             return render(request, self.template_name, context)
        
# --------------------------------------------------------------------------------------------------------

# class AppointmentReservationView(LoginRequiredMixin, View):
#     template_name = 'appointment_reservation/appointment_reservation_page.html'

#     def get(self, request, *args, **kwargs):
#         # take data from ajax
#         service_id = request.GET.get('service_id')
#         date_choices = []
#         service = None # Initialize service

#         if service_id:
#             try:
#                 service = Services.objects.get(id=service_id)
#                 start = service.start_reservation_date
#                 end = service.finish_reservation_date
#                 if start and end and start <= end:
#                     current_date = start.date() if isinstance(start, datetime) else start
#                     end_date = end.date() if isinstance(end, datetime) else end
#                     while current_date <= end_date:
#                         date_choices.append((
#                             current_date.strftime("%Y-%m-%d"),
#                             jdate.fromgregorian(date=current_date).strftime("%Y-%m-%d")
#                         ))
#                         current_date += timedelta(days=1)
#             except Services.DoesNotExist:
#                 messages.error(request, "سرویس یافت نشد.")
#                 service = None # Ensure service is None on error
#         # else: service remains None

#         form = ReserveAppointmentForm(
#             user_instance=request.user,
#             initial={'service': service_id},
#             date_choices=date_choices # Pass date_choices to form
#         )
#         context = {
#             'form': form,
#             'date_choices': date_choices,
#             'service': service,
#         }
#         return render(request, self.template_name, context)

#     def post(self, request, *args, **kwargs):
#         # Need to regenerate date_choices and fetch service for form validation and context
#         service_id = request.POST.get('service') # Get service_id from POST data
#         date_choices = []
#         service = None # Initialize service

#         if service_id:
#             try:
#                 service = Services.objects.get(id=service_id)
#                 start = service.start_reservation_date
#                 end = service.finish_reservation_date
#                 if start and end and start <= end:
#                     current_date = start.date() if isinstance(start, datetime) else start
#                     end_date = end.date() if isinstance(end, datetime) else end
#                     while current_date <= end_date:
#                         date_choices.append((
#                             current_date.strftime("%Y-%m-%d"),
#                             jdate.fromgregorian(date=current_date).strftime("%Y-%m-%d")
#                         ))
#                         current_date += timedelta(days=1)
#             except Services.DoesNotExist:
#                 # Handle case where service ID from POST is invalid
#                 messages.error(request, "سرویس ارسالی نامعتبر است.")
#                 service = None # Ensure service is None on error
#                 # date_choices will remain empty

#         # Initialize form with POST data, user, and generated date_choices
#         form = ReserveAppointmentForm(
#             request.POST,
#             user_instance=request.user,
#             date_choices=date_choices # Pass generated date_choices
#         )

#         context = {
#             'form': form,
#             'date_choices': date_choices, # Include in context
#             'service': service, # Include in context
#         }

#         if form.is_valid():
#             # commit=False: A powerful option in ModelForm.save() that allows modification of the model instance before saving.
#             reservation_obj = form.save(commit=False)
#             # In essence, it's a standard pattern for handling form submissions where you need to add data (like the user) to the model instance that isn't directly coming from the form fields themselves.
#             reservation_obj.user = request.user
#             reservation_obj.save()

#             # Removed the second form.save() call
#             if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
#                 # ذخیره فرم و بررسی اعتبار و ...
#                 return HttpResponse({'message': 'با موفقیت ثبت شد!'})
#             messages.success(request, "رزرو با موفقیت انجام شد.", 'success')
#             # Consider redirecting on success instead of rendering the same page for better UX
#             # return redirect('some_success_url')
#             # For now, render the page with the form (which might be empty or reset depending on form logic)
#             return render(request, self.template_name, context) # Use full context
            

#         else:
#             # Form is invalid, messages.error already added by form or view logic
#             messages.error(request, "رزرو با خطا مواجه شد.", 'error')
#             return render(request, self.template_name, context) # Use full context


# ----------------------------------------

# File: royal_clinic/apps/reservation/views.py
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from datetime import datetime, timedelta
from django.http import HttpResponse, JsonResponse # Import JsonResponse

# Assuming Services model and ReserveAppointmentForm are imported elsewhere
# Assuming jdate is imported elsewhere

# from .models import Services # Example import
# from .forms import ReserveAppointmentForm # Example import
# import jdate # Example import


class AppointmentReservationView(LoginRequiredMixin, View):
    template_name = 'appointment_reservation/appointment_reservation_page.html'

    def get(self, request, *args, **kwargs):
        # take data from ajax
        service_id = request.GET.get('service_id')
        date_choices = []
        service = None # Initialize service

        if service_id:
            try:
                service = Services.objects.get(id=service_id)
                start = service.start_reservation_date
                end = service.finish_reservation_date
                if start and end and start <= end:
                    current_date = start.date() if isinstance(start, datetime) else start
                    end_date = end.date() if isinstance(end, datetime) else end
                    while current_date <= end_date:
                        date_choices.append((
                            current_date.strftime("%Y-%m-%d"),
                            jdate.fromgregorian(date=current_date).strftime("%Y-%m-%d")
                        ))
                        current_date += timedelta(days=1)
            except Services.DoesNotExist:
                messages.error(request, "سرویس یافت نشد.")
                service = None # Ensure service is None on error
        # else: service remains None

        form = ReserveAppointmentForm(
            user_instance=request.user,
            initial={'service': service_id},
            date_choices=date_choices # Pass date_choices to form
        )
        context = {
            'form': form,
            'date_choices': date_choices,
            'service': service,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # Need to regenerate date_choices and fetch service for form validation and context
        service_id = request.POST.get('service') # Get service_id from POST data
        date_choices = []
        service = None # Initialize service

        if service_id:
            try:
                service = Services.objects.get(id=service_id)
                start = service.start_reservation_date
                end = service.finish_reservation_date
                if start and end and start <= end:
                    current_date = start.date() if isinstance(start, datetime) else start
                    end_date = end.date() if isinstance(end, datetime) else end
                    while current_date <= end_date:
                        date_choices.append((
                            current_date.strftime("%Y-%m-%d"),
                            jdate.fromgregorian(date=current_date).strftime("%Y-%m-%d")
                        ))
                        current_date += timedelta(days=1)
            except Services.DoesNotExist:
                # Handle case where service ID from POST is invalid
                messages.error(request, "سرویس ارسالی نامعتبر است.")
                service = None # Ensure service is None on error
                # date_choices will remain empty

        # Initialize form with POST data, user, and generated date_choices
        form = ReserveAppointmentForm(
            request.POST,
            user_instance=request.user,
            date_choices=date_choices # Pass generated date_choices
        )

        context = {
            'form': form,
            'date_choices': date_choices, # Include in context
            'service': service, # Include in context
        }

        if form.is_valid():
            # commit=False: A powerful option in ModelForm.save() that allows modification of the model instance before saving.
            reservation_obj = form.save(commit=False)
            # In essence, it's a standard pattern for handling form submissions where you need to add data (like the user) to the model instance that isn't directly coming from the form fields themselves.
            reservation_obj.user = request.user
            reservation_obj.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': 'رزرو شما با موفقیت ثبت شد.',
                    'redirect_url': reverse('reservation:reservation_main_page')
                })
            else:
                messages.success(request, "رزرو با موفقیت انجام شد.", 'success')
                # Consider redirecting on success instead of rendering the same page for better UX (Post/Redirect/Get pattern)
                # return redirect('some_success_url')
                # For now, render the page with the form (which might be empty or reset depending on form logic)
                return redirect('reservation:reservation_main_page') 
            

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'message': 'برخی فیلدها صحیح نیستند.',
                'errors': form.errors.get_json_data()
            }, status=400)
            
    
        else:
            # Form is invalid, messages.error already added by form or view logic
            messages.error(request, "رزرو با خطا مواجه شد.", 'error')
            return render(request, self.template_name, context) # Use full context