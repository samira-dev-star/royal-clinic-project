from django.views import View
from django.shortcuts import render, redirect
from .reservation_forms import ReserveAppointmentForm
from apps.services.models import Services
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages

# from jdatetime import date as jdate
# from datetime import timedelta,datetime

from django.urls import reverse
# from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin


# from django.shortcuts import render, redirect
# from django.views import View
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib import messages
# from datetime import datetime, timedelta
# from django.http import JsonResponse # Import JsonResponse

# def reservation(request, *args, **kwargs):
#     template_name = 'appointment_reservation/partials/appointment_form.html'
#     service = None
#     date_choices = []
#     service_id = request.POST.get('service') if request.method == 'POST' else request.GET.get('service_id')

#     today = datetime.now().date()  # Get current date

#     if service_id:
#         try:
#             service = Services.objects.get(id=service_id)
#             start = service.start_reservation_date
#             end = service.finish_reservation_date
#             if start and end and start <= end:
#                 current_date = start.date() if isinstance(start, datetime) else start
#                 end_date = end.date() if isinstance(end, datetime) else end
#                 # Only include dates that are today or in the future
#                 while current_date <= end_date:
#                     if current_date >= today:
#                         date_choices.append((
#                             current_date.strftime("%Y-%m-%d"),
#                             jdate.fromgregorian(date=current_date).strftime("%Y-%m-%d")
#                         ))
#                     current_date += timedelta(days=1)
#             else:
#                 messages.warning(request, "محدوده تاریخ معتبر نیست.")
#         except Services.DoesNotExist:
#             messages.error(request, "سرویس یافت نشد.")
#             service = None

#     if request.method == 'POST':
#         form = ReserveAppointmentForm(request.POST, user_instance=request.user, date_choices=date_choices)
#         if form.is_valid():
#             try:
#                 reservation_obj = form.save(commit=False)
#                 reservation_obj.user = request.user
#                 reservation_obj.save()
                
#                 # در صورت درخواست Ajax، به جای بازگرداندن فرم جدید، یک redirect_url ارسال می‌کنیم.
#                 if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
#                     return JsonResponse({
#                         'status': 'success',
#                         'redirect_url': reverse('main:index')
#                     })
                
#                 messages.success(request, "✅ نوبت شما با موفقیت ثبت شد.")
#                 return redirect('main:index')
#             except Exception as e:
#                 if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
#                     return JsonResponse({'status': 'error', 'message': f'❌ خطا در ذخیره‌سازی: {str(e)}'})
#                 messages.error(request, f"❌ خطا در ذخیره‌سازی: {str(e)}")
#         else:
#             # ارسال خطاها به صورت JSON در درخواست Ajax
#             if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
#                 errors = {field: error_list for field, error_list in form.errors.items()}
#                 return JsonResponse({'status': 'error', 'errors': errors})
#             for field, errors in form.errors.items():
#                 for error in errors:
#                     messages.error(request, f"{field}: {error}")
#     if request.method == 'POST':
#         try:
#             # ... کد پردازش فرم و ذخیره داده‌ها ...
#             return JsonResponse({
#                 'status': 'success',
#                 'message': '✅ اطلاعات با موفقیت ثبت شد!',
#                 'redirect_url': reverse('main:index')
#             }, status=200)  # کد وضعیت 200 برای موفقیت
#         except Exception as e:
#             return JsonResponse({
#                 'status': 'error',
#                 'message': f'❌ خطا: {str(e)}'
#             }, status=400)
#     else:
#         # sending data to frorms from view
#         form = ReserveAppointmentForm(user_instance=request.user, initial={'service': service_id}, date_choices=date_choices)

#     if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
#         rendered_html = render_to_string('appointment_reservation/partials/date_dropdown.html', {
#             'form': form,
#             'date_choices': date_choices
#         }, request=request)
#         return JsonResponse({'form_html': rendered_html})

#     return render(request, template_name, {'form': form, 'service': service})


# --------------------------------------------------------------------------------------------------------------------------------


# class AppointmentReservationView(LoginRequiredMixin, View):
#     template_name = 'appointment_reservation/appointment_reservation_page.html'

#     def get(self, request, *args, **kwargs):
#         service_id = request.GET.get('service_id')
#         date_choices = []
#         service = None

#         if service_id:
#             try:
#                 service = Services.objects.get(id=service_id)
#                 start = service.start_reservation_date
#                 end = service.finish_reservation_date
#                 today = datetime.now().date()
#                 if start and end and start <= end:
#                     current_date = start.date() if isinstance(start, datetime) else start
#                     end_date = end.date() if isinstance(end, datetime) else end
#                     while current_date <= end_date:
#                         if current_date >= today:
#                             date_choices.append((
#                                 current_date.strftime("%Y-%m-%d"),
#                                 jdate.fromgregorian(date=current_date).strftime("%Y-%m-%d")
#                             ))
#                         current_date += timedelta(days=1)
#             except Services.DoesNotExist:
#                 messages.error(request, "سرویس یافت نشد.")
#                 service = None

#         form = ReserveAppointmentForm(
#             user_instance=request.user,
#             initial={'service': service_id},
#             date_choices=date_choices
#         )
#         context = {
#             'form': form,
#             'date_choices': date_choices,
#             'service': service,
#         }
#         return render(request, self.template_name, context)

#     def post(self, request, *args, **kwargs):
#         service_id = request.POST.get('service')
#         date_choices = []
#         service = None

#         if service_id:
#             try:
#                 service = Services.objects.get(id=service_id)
#                 start = service.start_reservation_date
#                 end = service.finish_reservation_date
#                 today = datetime.now().date()
#                 if start and end and start <= end:
#                     current_date = start.date() if isinstance(start, datetime) else start
#                     end_date = end.date() if isinstance(end, datetime) else end
#                     while current_date <= end_date:
#                         if current_date >= today:
#                             date_choices.append((
#                                 current_date.strftime("%Y-%m-%d"),
#                                 jdate.fromgregorian(date=current_date).strftime("%Y-%m-%d")
#                             ))
#                         current_date += timedelta(days=1)
#             except Services.DoesNotExist:
#                 messages.error(request, "سرویس ارسالی نامعتبر است.")
#                 service = None

#         form = ReserveAppointmentForm(
#             request.POST,
#             user_instance=request.user,
#             date_choices=date_choices
#         )

#         context = {
#             'form': form,
#             'date_choices': date_choices,
#             'service': service,
#         }

#         if form.is_valid():
#             reservation_obj = form.save(commit=False)
#             reservation_obj.user = request.user
#             reservation_obj.save()

#             if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#                 return JsonResponse({
#                     'status': 'success',
#                     'message': 'رزرو شما با موفقیت ثبت شد.',
#                     'redirect_url': reverse('reservation:reservation_main_page')
#                 })
#             else:
#                 messages.success(request, "رزرو با موفقیت انجام شد.", 'success')
#                 return redirect('reservation:reservation_main_page')

#         if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#             return JsonResponse({
#                 'status': 'error',
#                 'message': 'برخی فیلدها صحیح نیستند.',
#                 'errors': form.errors.get_json_data()
#             }, status=400)

#         else:
#             messages.error(request, "رزرو با خطا مواجه شد.", 'error')
#             return render(request, self.template_name, context)



# ----------------------------

# class ReservationForm(View):
#     def get(self, request):
#         form = ReserveAppointmentForm(user_instance=request.user)
#         return render(request, 'appointment_reservation/partials/appointment_form.html', {'form': form})

from django.views.generic import View
from django.http import JsonResponse
from .reservation_forms import ReserveAppointmentForm
from .models import Services

# def reservation_partial_view(request):
#     if request.method == 'GET':
#         service_id = request.GET.get('service_id')  # از GET بگیر چون از طریق AJAX قراره ارسال بشه
#         service_instance = None
#         if service_id:
#             try:
#                 service_instance = Services.objects.get(id=service_id)
#                 print("Service ID:", service_id)
#                 print(service_instance)
                
#             except Services.DoesNotExist:
#                 pass  # یا می‌تونی هندل کنی

#         form = ReserveAppointmentForm(user_instance=request.user, service_instance=service_instance)
#         return render(request, 'appointment_reservation/partials/appointment_form.html', {'form': form, 'service': service_instance})
        

# def reservation_partial_view(request):
#     if request.method == 'GET':
#         service_id = request.GET.get('service_id')
#         print("🔵 Service ID from AJAX:", service_id)  # بررسی دریافت آی‌دی

#         service_instance = None
#         if service_id:
#             service_instance = Services.objects.get(id=service_id)
                
#         form = ReserveAppointmentForm(user_instance=request.user, service_instance=service_instance , initial={'service': service_id})
#         return render(request, 'appointment_reservation/partials/appointment_form.html', {
#             'form': form,
#             'service': service_instance,
#         })
        
#     if request.method == 'POST':
#         form = ReserveAppointmentForm(request.POST, user_instance=request.user,service_instance=service_instance)
#         if form.is_valid():
#             try:
#                 reservation_obj = form.save(commit=False)
#                 reservation_obj.user = request.user
#                 reservation_obj.save()

#                 if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
#                     return JsonResponse({
#                         'status': 'success',
#                         'redirect_url': reverse('main:index')
#                     })
                
#                 messages.success(request, "✅ نوبت شما با موفقیت ثبت شد.")
#                 return redirect('main:index')
            
#             except Exception as e:
#                 if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
#                     return JsonResponse({'status': 'error', 'message': f'❌ خطا در ذخیره‌سازی: {str(e)}'})
#                 messages.error(request, f"❌ خطا در ذخیره‌سازی: {str(e)}")
                
#         else:
#             # ارسال خطاها به صورت JSON در درخواست Ajax
#             if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
#                 errors = {field: error_list for field, error_list in form.errors.items()}
#                 return JsonResponse({'status': 'error', 'errors': errors})
#             for field, errors in form.errors.items():
#                 for error in errors:
#                     messages.error(request, f"{field}: {error}")
                    
    
#     if request.method == 'POST':
#         try:
#             # ... کد پردازش فرم و ذخیره داده‌ها ...
#             return JsonResponse({
#                 'status': 'success',
#                 'message': '✅ اطلاعات با موفقیت ثبت شد!',
#                 'redirect_url': reverse('main:index')
#             }, status=200)  # کد وضعیت 200 برای موفقیت
#         except Exception as e:
#             return JsonResponse({
#                 'status': 'error',
#                 'message': f'❌ خطا: {str(e)}'
#             }, status=400)
#     else:
#         # sending data to frorms from view
#         form = ReserveAppointmentForm(user_instance=request.user, initial={'service': service_id})

#     if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
#         rendered_html = render_to_string('appointment_reservation/partials/date_dropdown.html', {
#             'form': form,
#         }, request=request)
#         return JsonResponse({'form_html': rendered_html})

   
            

def reservation_partial_view(request):
    service_id = request.GET.get('service_id') if request.method == 'GET' else request.POST.get('service')
    service_instance = None

    if service_id:
        try:
            service_instance = Services.objects.get(id=service_id)
        except Services.DoesNotExist:
            service_instance = None

    if request.method == 'GET':
        form = ReserveAppointmentForm(user_instance=request.user, service_instance=service_instance, initial={'service': service_id})
        return render(request, 'appointment_reservation/partials/appointment_form.html', {
            'form': form,
            'service': service_instance,
        })

    if request.method == 'POST':
        form = ReserveAppointmentForm(request.POST, user_instance=request.user, service_instance=service_instance)
        if form.is_valid():
            try:
                reservation_obj = form.save(commit=False)
                reservation_obj.user = request.user
                reservation_obj.save()

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
            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                errors = {field: error_list for field, error_list in form.errors.items()}
                return JsonResponse({'status': 'error', 'errors': errors})
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    # حالت fallback
    form = ReserveAppointmentForm(user_instance=request.user, service_instance=service_instance, initial={'service': service_id})
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        rendered_html = render_to_string('appointment_reservation/partials/date_dropdown.html', {
            'form': form,
        }, request=request)
        return JsonResponse({'form_html': rendered_html})


# ---------------------------------------------------------

class AppointmentReservationView(LoginRequiredMixin, View):
    template_name = 'appointment_reservation/appointment_reservation_page.html'

    def get(self, request, *args, **kwargs):
        service_id = request.GET.get('service_id')
        service_instance = None
        if service_id:
            try:
                service_instance = Services.objects.get(id=service_id)
                
            except Services.DoesNotExist:
                messages.error(request, "سرویس یافت نشد.")
                service_instance = None

        form = ReserveAppointmentForm(
            user_instance=request.user,
            service_instance=service_instance,
            initial={'service': service_id},
        )
        context = {
            'form': form,
            'service': service_instance,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        service_id = request.POST.get('service')
        service_instance = None

        if service_id:
            try:
                service_instance = Services.objects.get(id=service_id)
                
            except Services.DoesNotExist:
                messages.error(request, "سرویس ارسالی نامعتبر است.")
                service_instance = None

        form = ReserveAppointmentForm(
            request.POST,
            user_instance=request.user,
            service_instance=service_instance,
            initial={'service': service_id}
        )

        context = {
            'form': form,
            'service_instance': service_instance,
        }

        if form.is_valid():
            reservation_obj = form.save(commit=False)
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
                return redirect('reservation:reservation_main_page')

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'message': 'برخی فیلدها صحیح نیستند.',
                'errors': form.errors.get_json_data()
            }, status=400)

        else:
            messages.error(request, "رزرو با خطا مواجه شد.", 'error')
            return render(request, self.template_name, context)


