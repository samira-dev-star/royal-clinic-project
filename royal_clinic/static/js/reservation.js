// // reservation js


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
                const messageBox = document.getElementById('message-box');
                if (messageBox) {
                    messageBox.textContent = '';
                }

                // دوباره eventها را برای فرم جدید ست کنید
                bindServiceChangeEvent();
                bindFormSubmission();
            })
            .catch(() => {
                alert('خطا در دریافت تاریخ‌ها. لطفاً مجدداً تلاش کنید.');
            });
    }

    // پیاده‌سازی event listener برای ارسال فرم
    function bindFormSubmission() {
        const form = document.getElementById('reservationForm');
        if (!form) return;
    
        form.removeEventListener('submit', form._submitHandler);
        form._submitHandler = function (e) {
            e.preventDefault();
            const formData = new FormData(form);
    
            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {'X-Requested-With': 'XMLHttpRequest'}
            })
            .then(response => response.json())
            .then(data => {
                const messageBox = document.getElementById('message-box');
                
                // مدیریت پاسخ موفق
                if (data.status === 'success') {
                    if (messageBox) {
                        messageBox.style.color = 'green';
                        messageBox.textContent = data.message;
                        
                        // ریدایرکت پس از 2 ثانیه
                        setTimeout(() => {
                            if (data.redirect_url) {
                                window.location.href = data.redirect_url;
                            }
                        }, 2000);
                    }
                }
                // مدیریت خطاها
                else if (data.status === 'error') {
                    if (messageBox) {
                        messageBox.style.color = 'red';
                        messageBox.textContent = data.message || '❌ خطایی رخ داده است.';
                    }
    
                    // نمایش خطاهای فیلدها
                    if (data.errors) {
                        Object.entries(data.errors).forEach(([field, errors]) => {
                            const input = document.getElementById(`id_${field}`);
                            const errorContainer = input.closest('.mb-4').querySelector('.text-red-600');
                            if (errorContainer) {
                                errorContainer.textContent = errors.map(e => e.message).join(', ');
                            }
                        });
                    }
                }
            })
                .catch(error => {
                console.error('Error:', error);

                if (isAuthenticated) {
                    Swal.fire({
                        icon: 'success',
                        title: 'ثبت موفق!',
                        text: 'نوبت شما ثبت شد. در اولین فرصت با شما تماس گرفته می‌شود.',
                        confirmButtonText: 'باشه',
                        confirmButtonColor: '#3085d6'
                    });
                } 
                else {
                    Swal.fire({
                        icon: 'warning',
                        title: 'نیاز به ورود یا ثبت‌نام',
                        text: 'برای ثبت نوبت ابتدا باید وارد شوید یا ثبت‌نام کنید.',
                        showCancelButton: true,
                        confirmButtonText: 'ورود',
                        cancelButtonText: 'ثبت‌نام',
                        confirmButtonColor: '#3085d6',
                        cancelButtonColor: '#d33'
                    }).then((result) => {
                        if (result.isConfirmed) {
                            window.location.href = '/accounts/login/';  // آدرس صفحه ورود
                        } else if (result.dismiss === Swal.DismissReason.cancel) {
                            window.location.href = '/accounts/register/'; // آدرس صفحه ثبت‌نام
                        }
                    });
                }
            });


        };
    
        form.addEventListener('submit', form._submitHandler);
    }
    
    document.addEventListener('DOMContentLoaded', function () {
        bindServiceChangeEvent();
        bindFormSubmission();
    });
    

    document.addEventListener('DOMContentLoaded', function () {
        bindServiceChangeEvent();
        bindFormSubmission();
    });
    

// // -------------------------------------------------------------------------------

