from django.shortcuts import render

# Create your views here.


def error_404(request, exception=None):
    return render(request, 'errors/404.html')