from django.contrib import admin
from django.utils.html import format_html
from .models import CrispEntryPoint
from django.http import HttpResponse


@admin.register(CrispEntryPoint)
class CrispAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        return super().changelist_view(request, extra_context=extra_context)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        # به جای نمایش لیست، مستقیم یک دکمه Crisp نشون می‌دیم
        return HttpResponse(f'''
            <div style="padding: 30px;">
                <a href="https://app.crisp.chat"
                   target="_blank"
                   style="display: inline-block; background-color: #00a884; color: white;
                          padding: 14px 28px; border-radius: 8px; text-decoration: none;
                          font-size: 18px; font-weight: bold;">
                    💬 مشاهده پیام‌های Crisp
                </a>
            </div>
        ''')
