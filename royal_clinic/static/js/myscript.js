
// Mobile menu toggle
const mobileMenuButton = document.getElementById('mobile-menu-button');
const mobileMenu = document.getElementById('mobile-menu');

mobileMenuButton.addEventListener('click', () => {
    mobileMenu.classList.toggle('hidden');
});

// Auto slider
let currentSlide = 0;
const slides = document.querySelectorAll('.slider-item');
const dots = document.querySelectorAll('.slider-dot');
const totalSlides = slides.length;

function showSlide(index) {
    // Hide all slides
    slides.forEach(slide => {
        slide.classList.remove('active');
    });
    
    // Remove active class from all dots
    dots.forEach(dot => {
        dot.classList.remove('active');
    });
    
    // Show current slide
    slides[index].classList.add('active');
    dots[index].classList.add('active');
}

function nextSlide() {
    currentSlide = (currentSlide + 1) % totalSlides;
    showSlide(currentSlide);
}

// Add click event to dots
dots.forEach((dot, index) => {
    dot.addEventListener('click', () => {
        currentSlide = index;
        showSlide(currentSlide);
    });
});

// Auto slide every 5 seconds
setInterval(nextSlide, 5000);

// Show first slide initially
showSlide(currentSlide);
    

// ----------------------------------------------------------------
// service detail js


// Tab functionality
const tabButtons = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

tabButtons.forEach(button => {
    button.addEventListener('click', () => {
        const tabId = button.getAttribute('data-tab');
        
        // Remove active class from all buttons and contents
        tabButtons.forEach(btn => {
            btn.classList.remove('border-amber-500', 'text-gray-800');
            btn.classList.add('border-transparent', 'text-gray-500');
        });
        
        tabContents.forEach(content => {
            content.classList.remove('active');
        });
        
        // Add active class to clicked button and corresponding content
        button.classList.add('border-amber-500', 'text-gray-800');
        button.classList.remove('border-transparent', 'text-gray-500');
        
        document.getElementById(tabId).classList.add('active');
    });
});

// FAQ accordion
const faqButtons = document.querySelectorAll('.faq-btn');

faqButtons.forEach(button => {
    button.addEventListener('click', () => {
        const answer = button.nextElementSibling;
        const icon = button.querySelector('i');
        
        // Toggle answer visibility
        answer.classList.toggle('hidden');
        
        // Rotate icon
        icon.classList.toggle('rotate-180');
    });
});


// -------------------------------------------------------------------
// reservation js


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
                console.error('Success:', error);

                alert('نوبت شما ثبت شد در اولین فرصت با شما تماس گرفته میشود');
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
    

// -------------------------------------------------------------------------------