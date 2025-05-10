from django.shortcuts import render,get_object_or_404,redirect
from .csf_forms import CommentForm
from django.views import View
from apps.services.models import Services
from .models import Comment
from django.contrib import messages

# Create your views here.

class CommentView(View):
    def get(self, request, *args, **kwargs):
        ServiceId = request.GET.get("ServiceId")
        commentId = request.GET.get("commentId")
        slug = kwargs['slug']
        
        # مقدار دهی اولیه فرم - کلید ها باید هم نام با فیلد های فرم باشن میریزشون تو اینپوت مخفیا
        initial_dict = {
            "service_id": ServiceId,
            "comment_id": commentId,
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
                
            Comment.objects.create(
                service = service,
                commenting_user = request.user,
                comment_text = cd['comment_text'],
                comment_parent = parent
            )
            
            messages.success(request, "نظر شما با موفقیت ثبت شد", "success")
            return redirect("services:service_detail", service.slug)
        messages.error(request, "خطا در ثبت نظر", "danger")
        return redirect("services:service_detail", service.slug)