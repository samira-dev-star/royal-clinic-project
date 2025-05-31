from django import views
from django.shortcuts import render
from .models import ServiceDiscount
from django.views import View

# Create your views here.

# class ShowDiscounts(View):
#     template_name = 'offers/discounts.html'
#     def get(self, request):
#         discounts = ServiceDiscount.objects.all()
#         context = {
#             'discounts': discounts
#         }
#         return render(request, self.template_name, context)