from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from .models import CustomPatient
from .patient_panel_form import CustomPatientForm, AllergyFormSet, MedicalHistoryFormSet
from django.contrib.auth.mixins import LoginRequiredMixin     
        
class CompletePatientProfileView(LoginRequiredMixin,View):
    template_name = 'patient_panel/patient_profile.html'
    def get(self, request):
        patient, created = CustomPatient.objects.get_or_create(user=request.user)
    
        form = CustomPatientForm(instance=patient)
        allergy_formset = AllergyFormSet(
            instance=patient,
            prefix='allergy'
        )
        history_formset = MedicalHistoryFormSet(
            instance=patient,
            prefix='history'
        )
    
        return render(request, self.template_name, {
            'form': form,
            'allergy_formset': allergy_formset,
            'history_formset': history_formset,
        })

    def post(self, request):
        patient, created = CustomPatient.objects.get_or_create(user=request.user)
        form = CustomPatientForm(
            request.POST,
            request.FILES,
            instance=patient
        )
        allergy_formset = AllergyFormSet(
            request.POST,
            instance=patient,
            prefix='allergy'
        )
        history_formset = MedicalHistoryFormSet(
            request.POST,
            instance=patient,
            prefix='history'
        )

        if form.is_valid() and allergy_formset.is_valid() and history_formset.is_valid():
            with transaction.atomic():
                patient = form.save()
                allergy_formset.instance = patient
                allergy_formset.save()
                history_formset.instance = patient
                history_formset.save()
                messages.success(request, 'تغییرات با موفقیت ذخیره شد')
                return redirect('patient:patient_profile')

        messages.error(request, 'خطا در ذخیره اطلاعات')
        return render(request, self.template_name, {
            'form': form,
            'allergy_formset': allergy_formset,
            'history_formset': history_formset,
        })