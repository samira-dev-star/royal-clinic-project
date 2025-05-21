from django import forms
from .models import ReserveAppointment
from apps.services.models import Services
from django.utils import timezone
from datetime import timedelta,datetime    


class ReserveAppointmentForm(forms.ModelForm):
    name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500',
            'placeholder': 'نام خود را وارد کنید',
        })
    )

    family = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500',
            'placeholder': 'نام خانوادگی خود را وارد کنید',
        })
    )

    mobile_number = forms.CharField(
        max_length=13,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500',
            'placeholder': 'شماره موبایل خود را وارد کنید',
            'dir': 'ltr',
        })
    )

    service = forms.ModelChoiceField(
        queryset=Services.objects.all(),
        required=True,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500',
            
        })
    )

    selected_date = forms.ChoiceField(
        required=True,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500',
        }),
        choices=[]
    )
    
    class Meta:
        model = ReserveAppointment
        fields = ['name', 'family', 'mobile_number', 'service', 'selected_date']

    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.pop('user_instance', None)
        
        # دریافت date_choices از ویو
        self.date_choices = kwargs.pop('date_choices', [])  # مقدار پیش‌فرض: لیست خالی
        super().__init__(*args, **kwargs)

        self.fields['selected_date'].choices = getattr(self.fields['selected_date'], 'choices', []) + self.date_choices
            
        if self.user_instance:
            self.fields['name'].initial = getattr(self.user_instance, 'name', '')
            self.fields['family'].initial = getattr(self.user_instance, 'family', '')
            self.fields['mobile_number'].initial = getattr(self.user_instance, 'mobile_number', '')
    
       
       
    
    def clean_selected_date(self):
        selected_date_str = self.cleaned_data['selected_date']
        service = self.cleaned_data.get('service')
    
        if not service:
            raise forms.ValidationError("لطفاً ابتدا یک سرویس انتخاب کنید")
    
        # تبدیل به تاریخ
        try:
            selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
        except ValueError:
            raise forms.ValidationError("فرمت تاریخ نامعتبر است")
    
        # بررسی محدوده سرویس
        start_date = service.start_reservation_date.date()
        end_date = service.finish_reservation_date.date()
    
        if not (start_date <= selected_date <= end_date):
            raise forms.ValidationError("تاریخ خارج از محدوده مجاز است")
    
        return selected_date_str
    

    def clean_mobile_number(self):
        mobile = self.cleaned_data['mobile_number'].strip().replace(" ", "")
        if mobile.startswith('0'):
            mobile = mobile[1:]
        if not mobile.startswith('98') and not mobile.startswith('+98'):
            mobile = '+98' + mobile
        elif mobile.startswith('98'):  # بدون + اگر وارد شده باشه
            mobile = '+' + mobile
        return mobile
    
    
    
# -------------------------------------------------------

class ReserveAppointmentForm2(forms.ModelForm):
    name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500',
            'placeholder': 'نام خود را وارد کنید',
        })
    )

    family = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500',
            'placeholder': 'نام خانوادگی خود را وارد کنید',
        })
    )

    mobile_number = forms.CharField(
        max_length=13,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500',
            'placeholder': 'شماره موبایل خود را وارد کنید',
            'dir': 'ltr',
        })
    )

    service = forms.ModelChoiceField(
        queryset=Services.objects.all(),
        required=True,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500',
            "onchange" : "ReservePageServiceIdSender(this.value)",
        })
    )

    selected_date = forms.ChoiceField(
        required=True,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500',
        }),
        choices=[]
    )
    
    class Meta:
        model = ReserveAppointment
        fields = ['name', 'family', 'mobile_number', 'service', 'selected_date']

    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.pop('user_instance', None)
        
        # دریافت date_choices از ویو
        self.date_choices = kwargs.pop('date_choices', [])  # مقدار پیش‌فرض: لیست خالی
        
        super().__init__(*args, **kwargs)  

        # self.fields['selected_date'].choices = getattr(self.fields['selected_date'], 'choices', []) + self.date_choices
        self.fields['selected_date'].choices = list(self.fields['selected_date'].choices or []) + self.date_choices
                
            
        if self.user_instance:
            self.fields['name'].initial = getattr(self.user_instance, 'name', '')
            self.fields['family'].initial = getattr(self.user_instance, 'family', '')
            self.fields['mobile_number'].initial = getattr(self.user_instance, 'mobile_number', '')
    
       
       
    
    def clean_selected_date(self):
        selected_date_str = self.cleaned_data['selected_date']
        service = self.cleaned_data.get('service')
    
        if not service:
            raise forms.ValidationError("لطفاً ابتدا یک سرویس انتخاب کنید")
    
        # تبدیل به تاریخ
        try:
            selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
        except ValueError:
            raise forms.ValidationError("فرمت تاریخ نامعتبر است")
    
        # بررسی محدوده سرویس
        start_date = service.start_reservation_date.date()
        end_date = service.finish_reservation_date.date()
    
        if not (start_date <= selected_date <= end_date):
            raise forms.ValidationError("تاریخ خارج از محدوده مجاز است")
    
        return selected_date_str
    

    def clean_mobile_number(self):
        mobile = self.cleaned_data['mobile_number'].strip().replace(" ", "")
        if mobile.startswith('0'):
            mobile = mobile[1:]
        if not mobile.startswith('98') and not mobile.startswith('+98'):
            mobile = '+98' + mobile
        elif mobile.startswith('98'):  # بدون + اگر وارد شده باشه
            mobile = '+' + mobile
        return mobile