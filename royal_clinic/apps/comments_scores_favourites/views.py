from django.shortcuts import render,get_object_or_404,redirect
from .csf_forms import CommentForm
from django.views import View
from apps.services.models import Services
from .models import Comment,UsersIdeaAndScores
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
    testimonials = UsersIdeaAndScores.objects.select_related('user', 'service').all()
    return render(request, 'csf/partials/users_ideas.html', {'testimonials': testimonials})


# -----------------------------------------------------------------
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied
from .models import UsersIdeaAndScores, Services

@login_required
@require_POST
def add_score(request):
    # دریافت داده‌های ارسالی از فرم
    service_id = request.POST.get('service_id')
    score = request.POST.get('score')
    idea = request.POST.get('idea', '').strip()

    # اعتبارسنجی داده‌های ورودی
    if not service_id or not score:
        return JsonResponse({
            'status': 'error',
            'message': 'درخواست نامعتبر: اطلاعات ضروری ارسال نشده'
        }, status=400)

    try:
        service = get_object_or_404(Services, id=service_id)
        score = int(score)
    except (ValueError, TypeError):
        return JsonResponse({
            'status': 'error',
            'message': 'امتیاز باید یک عدد معتبر باشد'
        }, status=400)
    
    # بررسی محدوده مجاز امتیاز (1 تا 5)
    if score < 1 or score > 5:
        return JsonResponse({
            'status': 'error',
            'message': 'امتیاز باید بین ۱ تا ۵ باشد'
        }, status=400)

    # بررسی وجود امتیاز قبلی کاربر برای این سرویس
    existing_score = UsersIdeaAndScores.objects.filter(
        user=request.user,
        service=service
    ).exists()
    
    if existing_score:
        return JsonResponse({
            'status': 'error',
            'message': 'شما قبلاً به این سرویس امتیاز داده‌اید'
        }, status=403)

    # ایجاد رکورد جدید در دیتابیس
    try:
        new_score = UsersIdeaAndScores.objects.create(
            user=request.user,
            service=service,
            idea=idea,
            score=score
        )
        new_score.save()
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'خطا در ذخیره‌سازی داده‌ها: {str(e)}'
        }, status=500)

    # محاسبه میانگین جدید امتیازهای سرویس
    avg_score = service.calculate_average_score()
    
    return JsonResponse({
        'status': 'success',
        'message': 'امتیاز و نظر شما با موفقیت ثبت شد',
        'avg_score': avg_score
    })
# -----------------------------------------------------------------
    

# نصب tailwind
# settings > 'tailwind','theme',
# python manage.py tailwind init