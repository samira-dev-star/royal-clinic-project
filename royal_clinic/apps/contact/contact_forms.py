from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'نام و نام خانوادگی',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'ایمیل',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500',
                'dir': 'ltr',
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'شماره تماس',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500',
                'dir': 'ltr',
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'متن پیام',
                'rows': 4,
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500'
            }),
        }
