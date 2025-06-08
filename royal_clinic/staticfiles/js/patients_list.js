        // Sample JavaScript for search functionality
        document.addEventListener('DOMContentLoaded', function() {
            const searchInput = document.querySelector('.search-input');
            
            searchInput.addEventListener('input', function() {
                const searchTerm = this.value.toLowerCase();
                const patientCards = document.querySelectorAll('.patient-card');
                
                patientCards.forEach(card => {
                    const patientName = card.querySelector('h3').textContent.toLowerCase();
                    if (patientName.includes(searchTerm)) {
                        card.style.display = 'block';
                    } else {
                        card.style.display = 'none';
                    }
                });
            });
            
            // You can add more interactive features here
        });

        // حذف پارامتر از URL (در این قالب استفاده نشده اما می‌تواند مفید باشد)
        function removeURLParameter(url, parameter) {
            var urlparts = url.split('?');
            if (urlparts.length >= 2) {
                var prefix = encodeURIComponent(parameter) + '=';
                var parts = urlparts[1].split(/[&;]/g);
                for (var i = parts.length; i-- > 0;) {
                    if (parts[i].lastIndexOf(prefix, 0) !== -1) {
                        parts.splice(i, 1);
                    }
                }
                url = urlparts[0];
                if (parts.length > 0) {
                    url += '?' + parts.join('&');
                }
                return url;
            } else {
                return url;
            }
        }

        // تابع انتخاب نوع مرتب‌سازی
        function select_sort() {
            // اگر از jQuery استفاده نمی‌کنید، به جای $("#select_sort").val() از document.getElementById استفاده کنید:
            // const select_sort_value = document.getElementById("select_sort").value;
            const select_sort_value = document.getElementById("select_sort").value;
            const url = new URL(window.location.href);
            url.searchParams.set("sort_type", select_sort_value);
            url.searchParams.set("page", "1"); // ریست صفحه به شماره 1
            window.location = url.toString();
        }
