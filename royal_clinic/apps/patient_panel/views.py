from urllib import request
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from .models import CustomPatient,MedicalHistoryItem,Allergy,CurrentMedications
from .patient_panel_form import CustomPatientForm, AllergyFormSet, MedicalHistoryFormSet,CurrentMedicationsFormSet
from django.contrib.auth.mixins import LoginRequiredMixin     
from django.core.paginator import Paginator

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
        
        medicine_formset = CurrentMedicationsFormSet(
            instance=patient,
            prefix='medicine'
        )
    
        return render(request, self.template_name, {
            'form': form,
            'allergy_formset': allergy_formset,
            'history_formset': history_formset,
            'medicine_formset': medicine_formset,
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
        
        medicine_formset = CurrentMedicationsFormSet(
            request.POST,
            instance=patient,
            prefix='medicine'
        )

        if form.is_valid() and allergy_formset.is_valid() and history_formset.is_valid() and medicine_formset.is_valid():
            with transaction.atomic():
                patient = form.save()
                allergy_formset.instance = patient
                allergy_formset.save()
                history_formset.instance = patient
                history_formset.save()
                medicine_formset.instance = patient
                medicine_formset.save()
                messages.success(request, 'تغییرات با موفقیت ذخیره شد')
                return redirect('patient:patient_profile')

        messages.error(request, 'خطا در ذخیره اطلاعات')
        return render(request, self.template_name, {
            'form': form,
            'allergy_formset': allergy_formset,
            'history_formset': history_formset,
            'medicine_formset': medicine_formset,
        })
        
        
        
# ----------------------------------------------------
# show medical history and allergies of the patient:
# download the patient's medical history and allergies in pdf format using html2pdf

class ShowMedicalHistoryAndAllergiesView(View):
    def get(self,*args, **kwargs):
        current_patient = kwargs['id']
        patient = CustomPatient.objects.filter(user_id=current_patient)
        
        medical_history = MedicalHistoryItem.objects.filter(patient_id=current_patient)
        medicine = CurrentMedications.objects.filter(patient_id=current_patient)
        allergies = Allergy.objects.filter(patient_id=current_patient)
        context = {
            'patient':patient,
            'medical_history':medical_history,
            'medicine':medicine,
            'allergies':allergies,
            
        }
        
        return render(self.request,'patient_panel/medical_history_and_allergies.html',context)
    
# ----------------------------------------------------

class PatientsList(View):
    def get(self,request,*args, **kwargs):
        patients = CustomPatient.objects.all()
        
        sort_type = request.GET.get('sort_type')
        if not sort_type:
            sort_type = "0"
        if sort_type =="1":
            patients = patients.order_by('-user_id')
        elif sort_type =="2":
            patients = patients.order_by('user_id')
        
        paginator = Paginator(patients, 6)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        
        
        context = {
            'patients':page_obj.object_list,
            'page_obj':page_obj,
            'sort_type':sort_type,
        }
        return render(self.request,'patient_panel/patients_list.html',context)
    



