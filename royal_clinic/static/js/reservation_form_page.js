
// پیاده‌سازی event listener برای تغییر سرویس
function bindServiceChangeEvent() {
    const serviceSelect = document.getElementById('id_service');
    if (!serviceSelect) return;
    // اگر قبلاً listener بسته شده باشد، دوباره نبندیم
    serviceSelect.removeEventListener('change', serviceChangeHandler);
    serviceSelect.addEventListener('change', serviceChangeHandler);
}
function serviceChangeHandler() {
    const serviceId = this.value;
    fetch(`?service_id=${serviceId}`)
        .then(response => response.text())
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            // فرم جدید را از HTML پارس‌شده بگیرید
            const newForm = doc.getElementById('reservationForm');
            if (!newForm) return;
            const currentForm = document.getElementById('reservationForm');
            // جایگزینی محتوا (innerHTML) و به‌روز کردن CSRF Token
            currentForm.innerHTML = newForm.innerHTML;
            const newCsrfTokenInput = doc.querySelector('[name=csrfmiddlewaretoken]');
            if (newCsrfTokenInput) {
                // عنصر CSRF token درون فرم جدید
                const currentCsrfInput = currentForm.querySelector('[name=csrfmiddlewaretoken]');
                if (currentCsrfInput) {
                    currentCsrfInput.value = newCsrfTokenInput.value;
                }
            }
            // پاک کردن پیام قبلی هنگام تغییر سرویس
            clearMessages();
            // دوباره eventها را برای فرم جدید ست کنید
            bindServiceChangeEvent();
            bindFormSubmission();
        })
        .catch(() => {
            showMessage('خطا در دریافت تاریخ‌ها. لطفاً مجدداً تلاش کنید.', 'error');
        });
}
// پیاده‌سازی event listener برای ارسال فرم
function bindFormSubmission() {
    const form = document.getElementById('reservationForm');
    if (!form) return;
    form.removeEventListener('submit', form._submitHandler);
    form._submitHandler = function(e) {
        e.preventDefault();
        const formData = new FormData(form);
        // پاک کردن پیام‌های قبلی
        clearMessages();
        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {'X-Requested-With': 'XMLHttpRequest'}
        })
        .then(response => response.json())
        .then(data => {
            // مدیریت پاسخ موفق
            if (data.status === 'success') {
                showMessage(data.message, 'success');
                
                // ریدایرکت پس از 2 ثانیه
                setTimeout(() => {
                    if (data.redirect_url) {
                        window.location.href = data.redirect_url;
                    }
                }, 2000);
            }
            // مدیریت خطاها
            else if (data.status === 'error') {
                showMessage(data.message || '❌ خطایی رخ داده است.', 'error');
                // نمایش خطاهای فیلدها
                if (data.errors) {
                    Object.entries(data.errors).forEach(([field, errors]) => {
                        const input = document.getElementById(`id_${field}`);
                        const errorContainer = document.getElementById(`${field}-error`);
                        
                        if (input && errorContainer) {
                            errorContainer.textContent = errors.map(e => e.message).join(', ');
                            input.classList.add('border-red-500');
                        }
                    });
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showMessage('خطا در برقراری ارتباط با سرور', 'error');
        });
    };
    form.addEventListener('submit', form._submitHandler);
}
// نمایش پیام به کاربر
function showMessage(message, type) {
    const messageBox = document.getElementById('message-box');
    if (!messageBox) return;
    messageBox.textContent = message;
    messageBox.style.display = 'block';
    
    if (type === 'success') {
        messageBox.className = 'message-box bg-green-100 text-green-800';
    } else {
        messageBox.className = 'message-box bg-red-100 text-red-800';
    }
}
// پاک کردن تمام پیام‌ها و خطاها
function clearMessages() {
    const messageBox = document.getElementById('message-box');
    if (messageBox) {
        messageBox.textContent = '';
        messageBox.style.display = 'none';
    }
    // پاک کردن خطاهای فیلدها
    document.querySelectorAll('.error-message').forEach(el => {
        el.textContent = '';
    });
    // حذف کلاس‌های خطا از inputها
    document.querySelectorAll('input, select').forEach(input => {
        input.classList.remove('border-red-500');
    });
}
// فقط یک بار event listener ثبت شود
document.addEventListener('DOMContentLoaded', function() {
    bindServiceChangeEvent();
    bindFormSubmission();
});
    