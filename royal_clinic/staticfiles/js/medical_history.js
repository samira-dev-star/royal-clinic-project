
// Simple script to toggle print button visibility on mobile
document.addEventListener('DOMContentLoaded', function() {
    const printBtn = document.createElement('button');
    printBtn.className = 'md:hidden fixed bottom-24 right-6 bg-white text-blue-600 w-14 h-14 rounded-full shadow-lg flex items-center justify-center';
    printBtn.innerHTML = '<i class="fas fa-print text-xl"></i>';
    printBtn.addEventListener('click', function() {
        window.print();
    });
    document.body.appendChild(printBtn);
});
// ----------------------------------------------------------------
// download pdf
function downloadPDF() {
    const element = document.getElementById('print-area');

    const opt = {
        margin: [0.3, 0.3, 0.3, 0.3],  // [top, left, bottom, right] margin in inches
        filename: 'profile.pdf',
        image: { type: 'jpeg', quality: 1 },
        html2canvas: {
            scale: 3, // کیفیت بالاتر
            useCORS: true, // اگر تصاویر از دامنه دیگه هستن
            logging: true, // برای دیباگ در کنسول
            allowTaint: false,
        },
        jsPDF: {
            unit: 'mm',
            format: 'a4',
            orientation: 'portrait'
        },
        pagebreak: { mode: ['avoid-all', 'css', 'legacy'] }
    };

    html2pdf().set(opt).from(element).save();
}


// ----------------------------------------------------------------
// print

function printProfile() {
    var originalContents = document.body.innerHTML;
    var printContents = document.getElementById('print-area').innerHTML;
    document.body.innerHTML = printContents;
    window.print();
    document.body.innerHTML = originalContents;
    location.reload(); // صفحه رو بعد از پرینت رفرش کن
}

