from django import template
from datetime import datetime
from khayyam import JalaliDate

register = template.Library()

@register.filter
def string_to_jalali(value, date_format="%Y-%m-%d"):
    """
    فرض می‌کنیم value یک رشتهٔ تاریخ باشد، مثلاً "2025-05-25" یا "2025-05-25 14:30:00".
    این فیلتر ابتدا رشته را پِارس می‌کند (با فرمت date_format) و بعد خروجی شمسی می‌دهد.
    
    پارامتر date_format:
        الگوی strptime برای پارس کردن value است. به صورت پیش‌فرض "%Y-%m-%d" فرض شده.
        اگر رشتهٔ شما فرمت متفاوتی دارد (مثلاً "YYYY/MM/DD" یا همراه با زمان)،
        باید date_format را هنگام فراخوانی فیلتر مشخص کنید.
    
    خروجی:
        رشتهٔ تاریخ به صورت جلالی در فرمت پیش‌فرض "%Y/%m/%d" برمی‌گرداند.
        اگر بخواهید فرمت دیگری (مانند "روز ماه سال ساعت:دقیقه") داشته باشید،
        می‌توانید بعد از این فیلتر، دوباره از f-string یا جایی دیگر استفاده کنید.
    """
    if not value:
        return ""
    try:
        # اگر رشته دقیقاً شامل تاریخ و زمان باشد، 
        # بهتر است خودتان در date_format آن را بنویسید، مثال: "%Y-%m-%d %H:%M:%S"
        dt = datetime.strptime(value, date_format)
    except ValueError:
        # اگر پارس مستقیم با فرمت پیش‌فرض ممکن نیست، سعی می‌کنیم بخش تاریخ را جدا کنیم
        try:
            # بخشی که قبل از فاصله (space) است را به عنوان "YYYY-MM-DD" در نظر بگیرید
            date_part = value.split()[0]
            dt = datetime.strptime(date_part, "%Y-%m-%d")
        except Exception:
            return value  # اگر نتوانستیم پارس کنیم، خودِ رشتهٔ خام را برگردانیم

    # اکنون dt یک شیء datetime است (بر اساس منطقهٔ زمانی سرور)
    # از JalaliDate برای تبدیل میلادیبه‌شمسی استفاده می‌کنیم
    try:
        jalali_date = JalaliDate(dt.date())
        # خروجی به صورت YYYY/MM/DD است:
        return jalali_date.strftime("%Y/%m/%d")
    except Exception:
        return ""
