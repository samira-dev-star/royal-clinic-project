from django.contrib import admin
from django.utils.html import format_html
from .models import CrispEntryPoint
# HttpResponse: برای اینکه خودمون یه صفحه HTML دستی بسازیم.
from django.http import HttpResponse

# changelist_view : وقتی روی اسم مدل کلیک میکنیم این چیزیه که نشون داده می شد که در حالت عادی رکورد ها مون هستند ولی اینجل یک
# دکمه است


@admin.register(CrispEntryPoint)
class CrispAdmin(admin.ModelAdmin):
    # ما نمی‌خوایم لیست آیتم‌های این مدل رو نشون بدیم (اصلاً آیتمی نداریم )
    # فقط می‌خوایم یه دکمه ساده نشون بدیم که مدیر سایت روش کلیک کنه و بره به صفحه Crisp
    # در پنل ادمین جنگو، وقتی روی اسم یک مدل کلیک می‌کنی، وارد صفحه‌ای می‌شی که لیست رکوردهای اون مدل رو نشون می‌ده
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        return super().changelist_view(request, extra_context=extra_context)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        # به جای نمایش لیست، مستقیم یک دکمه Crisp نشون می‌دیم
        return HttpResponse("""
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Crisp Chat Dashboard</title>
                        <script src="https://cdn.tailwindcss.com"></script>
                        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
                        <style>
                            @keyframes float {
                                0%, 100% {
                                    transform: translateY(0);
                                }
                                50% {
                                    transform: translateY(-10px);
                                }
                            }
                            .floating {
                                animation: float 3s ease-in-out infinite;
                            }
                            .btn-hover {
                                transition: all 0.3s ease;
                                box-shadow: 0 4px 6px rgba(0, 168, 132, 0.3);
                            }
                            .btn-hover:hover {
                                transform: translateY(-2px);
                                box-shadow: 0 6px 12px rgba(0, 168, 132, 0.4);
                            }
                            .btn-hover:active {
                                transform: translateY(0);
                            }
                            .gradient-bg {
                                background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 50%, #bbf7d0 100%);
                            }
                        </style>
                    </head>
                    <body class="gradient-bg min-h-screen flex flex-col items-center justify-center p-6 font-sans">
                        <div class="max-w-2xl w-full bg-white rounded-xl shadow-lg overflow-hidden">
                            <div class="p-8 text-center">
                                
                                <div class="mb-6 flex justify-center">
                                    <div class="floating bg-emerald-100 p-4 rounded-full">
                                        <i class="fas fa-comments text-emerald-600 text-4xl"></i>
                                    </div>
                                </div>

                                <h1 class="text-3xl font-bold text-gray-800 mb-2">پیام های چت آنلاین</h1>
                                <p class="text-gray-600 mb-8">با کاربران خود به صورت آنلاین گفت و گو کنید</p>

                                
                                <div class="mb-6">
                                    <a href="https://app.crisp.chat" 
                                       target="_blank"
                                       class="btn-hover inline-flex items-center justify-center px-8 py-4 border border-transparent text-base                   font-medium rounded-md text-white bg-emerald-500 hover:bg-emerald-600 md:py-4 md:text-lg md:px-10                   transition-all duration-300">
                                        <i class="fas fa-comment-dots mr-3"></i>
                                        View Crisp Messages
                                    </a>
                                </div>

                                
                                
                            </div>

                            
                            <div class="bg-gray-50 px-6 py-4">
                                <div class="flex items-center justify-between text-sm text-gray-500">
                                    <span>© 2023 Crisp Chat Integration</span>
                                    <div class="flex space-x-4">
                                        <a href="https://crisp.chat/en/terms/" class="hover:text-emerald-600">Terms</a>
                                        <a href="https://crisp.chat/en/privacy/" class="hover:text-emerald-600">Privacy</a>
                                    </div>
                                </div>
                            </div>
                        </div>

                        
                        <div class="fixed bottom-6 right-6">
                            <a href="https://app.crisp.chat" 
                               target="_blank"
                               class="floating btn-hover w-16 h-16 flex items-center justify-center rounded-full bg-emerald-500 text-white                  shadow-lg">
                                <i class="fas fa-comment-alt text-2xl"></i>
                            </a>
                        </div>

                        <script>
                            
                            document.querySelectorAll('a').forEach(link => {
                                link.addEventListener('click', function() {
                                    this.classList.add('transform', 'scale-95');
                                    setTimeout(() => {
                                        this.classList.remove('transform', 'scale-95');
                                    }, 200);
                                });
                            });
                        </script>
                    </body>
                    </html>
                    """)
