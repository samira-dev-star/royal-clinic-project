from django.contrib import admin
from .models import ServiceVideo,ServiceImage

from django.utils.html import format_html


class ServiceVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'service', 'is_active', 'upload_date', 'video_with_thumbnail')
    list_filter = ('is_active', 'upload_date', 'service')
    search_fields = ('title', 'description')

    def video_with_thumbnail(self, obj):
        if obj.video_file:
            poster_url = obj.thumbnail.url if obj.thumbnail else ''
            return format_html(
                '<video width="200" controls {}>'
                '<source src="{}" type="video/mp4">'
                'Your browser does not support the video tag.'
                '</video>',
                f'poster="{poster_url}"' if poster_url else '',
                obj.video_file.url
            )
        return "ویدیو موجود نیست"
    video_with_thumbnail.short_description = "پیش نمایش ویدیو"
    video_with_thumbnail.allow_tags = True


admin.site.register(ServiceVideo, ServiceVideoAdmin)

# در HTML5 تگ <video> می‌تواند یک ویژگی به اسم poster داشته باشد که آدرس تصویر کاور را می‌گیرد و هنگام بارگذاری ویدیو آن تصویر نمایش داده می‌شود تا وقتی ویدیو پخش نشود.

# اگر می‌خوای سریع بنویسی و مطمئنی ورودی‌ها امن هستند، mark_safe بد نیست.
# اگر می‌خوای کدت ایمن‌تر و به‌روزتر باشه، بهتره از format_html استفاده کنی.


@admin.register(ServiceImage)
class ServiceImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'service', 'is_active', 'upload_date')
    list_filter = ('is_active', 'upload_date', 'service')
    search_fields = ('title', 'description')