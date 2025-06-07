from locale import currency
from multiprocessing import context
from django.shortcuts import render,get_object_or_404,redirect
from .csf_forms import CommentForm
from django.views import View
from apps.services.models import Services
from .models import Comment,AddScore
from django.contrib import messages
from apps.accounts.models import Customuser

# Create your views here.

class CommentView(View):
    def get(self, request, *args, **kwargs):
        ServiceId = request.GET.get("ServiceId")
        commentId = request.GET.get("commentId")
        commentingUser = request.GET.get("commentingUser")
        slug = kwargs['slug']
        
        # مقدار دهی اولیه فرم - کلید ها باید هم نام با فیلد های فرم باشن میریزشون تو اینپوت مخفیا
        initial_dict = {
            "service_id": ServiceId,
            "comment_id": commentId,
            "commenting_user" : commentingUser,
        }
        
        form = CommentForm(initial=initial_dict)
        
        context = {
            "form": form,
            "slug": slug,
        }
        
        return render(request, "csf/partials/create_comment.html", context)
        
    
    
    def post(self, request, *args, **kwargs):
        
        slug = kwargs.get("slug")
        service = get_object_or_404(Services, slug=slug)
        
        form = CommentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            
            
            # check if it is comment to post or replay to a comment
            parent = None
            if(cd['comment_id']):
                parentId = cd['comment_id']  
                parent = Comment.objects.get(id=parentId)
            

                
            comment = Comment.objects.create(
                service = service,
                commenting_user = request.user,
                comment_text = cd['comment_text'],
                comment_parent = parent,
                is_admin_comment = request.user.is_staff
            )
            
            if request.user.is_staff:
                comment.is_active = True
                comment.save()
                
            
            messages.success(request, "نظر شما با موفقیت ثبت شد", "success")
            return redirect("services:service_detail", service.slug)
        messages.error(request, "خطا در ثبت نظر", "danger")
        return redirect("services:service_detail", service.slug)
    
# -----------------------------------------------------------------

def testimonials(request):
    testimonials = AddScore.objects.select_related('user', 'service').all()
    return render(request, 'csf/partials/users_ideas.html', {'testimonials': testimonials})


# -----------------------------------------------------------------

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@login_required
def add_score(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        score = request.POST.get('score')
        idea = request.POST.get('idea')
        service_id = request.POST.get('service_id')

        if score is None or score == '':
            return JsonResponse({'success': False, 'message': 'امتیاز ارسال نشده است'}, status=400)

        try:
            service = Services.objects.get(id=service_id)
        except Services.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'سرویس پیدا نشد'}, status=404)

        # Check if user has already scored this service
        if AddScore.objects.filter(user=request.user, service=service).exists():
            return JsonResponse({'success': False, 'message': 'شما قبلاً به این سرویس امتیاز داده‌اید'}, status=400)

        add_score_obj = AddScore.objects.create(
            user=request.user,
            service=service,
            score=int(score),
            idea=idea
        )

        # Return user's score to keep stars highlighted
        return JsonResponse({'success': True, 'message': 'امتیاز با موفقیت ثبت شد', 'user_score': add_score_obj.score})

    return JsonResponse({'success': False, 'message': 'درخواست نامعتبر'}, status=400)

# -----------------------------------------------------------------

class ScoringServicesView(View):
    def get(self, request):
        services = Services.objects.all()
        return render(request, 'csf/score_services.html', {'services': services})