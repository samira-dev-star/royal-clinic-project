from django import forms
from .models import CustomPatient, Allergy, MedicalHistoryItem,CurrentMedications
from django.forms import inlineformset_factory

# --------------------------------------
# jalali date picker in forms
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget




class CustomPatientForm(forms.ModelForm):
    class Meta:
        model = CustomPatient
        fields = [
            'image_name', 'birth_date', 'blood_type', 
            'height', 'weight', 'emergency_contact', 'address'
        ]
        
        
        widgets = {
            
            'image_name': forms.FileInput(attrs={
                'class': 'hidden',
                'id': 'id_image_name',
                'accept': 'image/*',
                # 'name': 'image_name'
                
            }),
            
            'birth_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-input w-full'
            }),
            'blood_type': forms.Select(attrs={
                'class': 'form-input w-full'
            }),
            'height': forms.NumberInput(attrs={
                'class': 'form-input w-full',
                'step': '0.1'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'form-input w-full',
                'step': '0.1'
            }),
            'emergency_contact': forms.TextInput(attrs={
                'class': 'form-input w-full',
                'dir': 'ltr'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-input w-full',
                'rows': '3'
            }),
        }

    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input w-full',
            'placeholder': 'نام خود را وارد کنید'
        })
    )
    
    family = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input w-full',
            'placeholder': 'نام خانوادگی خود را وارد کنید'
        })
    )
    
    mobile_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input w-full',
            'dir': 'ltr',
            'placeholder': '09xxxxxxxxx'
        })
    )
    
    gender = forms.ChoiceField(
        choices=CustomPatient.user.field.related_model.GENDER,
        widget=forms.Select(attrs={'class': 'form-input w-full'})
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input w-full',
            'placeholder': 'ایمیل خود را وارد کنید'
        })
    )
    
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['name'].initial = self.instance.user.name
            self.fields['family'].initial = self.instance.user.family
            self.fields['mobile_number'].initial = self.instance.user.mobile_number
            self.fields['gender'].initial = self.instance.user.gender
            self.fields['email'].initial = self.instance.user.email


    
    def save(self, commit=True):
        patient = super().save(commit=False)
        user = patient.user
        user.name = self.cleaned_data['name']
        user.family = self.cleaned_data['family']
        user.mobile_number = self.cleaned_data['mobile_number']
        user.gender = self.cleaned_data['gender']
        user.email = self.cleaned_data['email']

        # اگر تصویری آپلود شده بود، آن را به مدل اعمال کن
        if self.cleaned_data.get('image_name'):
            patient.image_name = self.cleaned_data['image_name']

        if commit:
            user.save()
            patient.save()
        return patient

    
    

class AllergyForm(forms.ModelForm):
    class Meta:
        model = Allergy
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input w-full',
                'placeholder': 'مثال: پنی‌سیلین'
            })
        }
        

class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistoryItem
        fields = ['title', 'diagnosis_year', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input w-full',
                'placeholder': 'شرایط پزشکی'
            }),
            'diagnosis_year': forms.NumberInput(attrs={
                'class': 'form-input w-full',
                'placeholder': 'سال تشخیص'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input w-full',
                'rows': '2',
                'placeholder': 'توضیحات'
            }),
        }
        

class CurrentMedicationsForm(forms.ModelForm):

    class Meta:
        model = CurrentMedications
        fields = ['medication_name', 'dosage', 'priscribed_at', 'using_state']
        widgets = {
            'medication_name': forms.TextInput(attrs={
                'class': 'form-input w-full',
                'placeholder': 'نام دارو'
            }),
            'dosage': forms.TextInput(attrs={
                'class': 'form-input w-full',
                'placeholder': 'دوز مصرف'
            }),
            'using_state': forms.Select(attrs={
                'class': 'form-input w-full'
            }),
            # 'priscribed_at': forms.TextInput(attrs={
            # 'class': 'form-input w-full jalali-datepicker',
            # 'placeholder': '01/02/1404',
            # 'autocomplete': 'off'
            # })
        }
        
    def __init__(self, *args, **kwargs):
        super(CurrentMedicationsForm,self).__init__(*args, **kwargs)
        self.fields['priscribed_at']=JalaliDateField(widget=AdminJalaliDateWidget(attrs={'placeholder': '01/02/1404',}))
        

AllergyFormSet = inlineformset_factory(
    CustomPatient, Allergy, form=AllergyForm,
    extra=0, can_delete=True
)

MedicalHistoryFormSet = inlineformset_factory(
    CustomPatient, MedicalHistoryItem, form=MedicalHistoryForm,
    extra=0, can_delete=True 
)



CurrentMedicationsFormSet = inlineformset_factory(
    CustomPatient, CurrentMedications, form=CurrentMedicationsForm,
    extra=0, can_delete=True
)