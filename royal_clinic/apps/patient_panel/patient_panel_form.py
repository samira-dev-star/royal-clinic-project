
from django import forms
from .models import CustomPatient, Allergy, MedicalHistoryItem
from django.forms import inlineformset_factory

class CustomPatientForm(forms.ModelForm):
    class Meta:
        model = CustomPatient
        fields = ['address', 'birth_date', 'blood_type', 'height', 'weight', 'emergency_contact', 'image_name']
        
        
class AllergyForm(forms.ModelForm):
    class Meta:
        model = Allergy
        fields = ['title']


class MedicalHistoryItemForm(forms.ModelForm):
    class Meta:
        model = MedicalHistoryItem
        fields = ['title', 'description']


AllergyFormSet = inlineformset_factory(
    CustomPatient, Allergy, form=AllergyForm,
    extra=2, can_delete=True
)

MedicalHistoryItemFormSet = inlineformset_factory(
    CustomPatient, MedicalHistoryItem, form=MedicalHistoryItemForm,
    extra=2, can_delete=True
)
