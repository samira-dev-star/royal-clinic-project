from django.contrib import admin
from django.contrib.admin.filters import SimpleListFilter
from .models import Comment
from django_admin_listfilter_dropdown.filters import DropdownFilter
from django.db.models import Q
# Register your models here.

class DateFilter(SimpleListFilter):
    title = 'کامنت‌ها بر اساس کاربر'
    parameter_name = 'comment_user'
    
    def lookups(self, request, model_admin):
        comments = Comment.objects.order_by('-registerdate')
        return [(comment.id, str(comment.commenting_user)) for comment in comments]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(pk=self.value())
        return queryset


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['service','commenting_user','is_active','registerdate']
    list_filter = [('is_active',DropdownFilter),DateFilter]
    search_fields = ['registerdate']
    ordering = ['-registerdate']
    list_editable = ['is_active']