from django.views import View
from django.shortcuts import render, redirect
from .models import ReserveAppointment
from .reservation_forms import ReserveAppointmentForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from apps.services.models import Services
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages


from jdatetime import date as jdate
from datetime import timedelta,datetime

from django.urls import reverse
from django.http import JsonResponse


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
        form = ReserveAppointmentForm(user_instance=request.user, initial={'service': service_id}, date_choices=date_choices)

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        rendered_html = render_to_string('appointment_reservation/partials/date_dropdown.html', {
            'form': form,
            'date_choices': date_choices
        }, request=request)
        return JsonResponse({'form_html': rendered_html})

    return render(request, template_name, {'form': form, 'service': service})
