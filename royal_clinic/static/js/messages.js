
document.addEventListener('DOMContentLoaded', function () {
    const messages = document.querySelectorAll('.message');
    messages.forEach(function (msg) {
        // حذف خودکار بعد از ۵ ثانیه
        setTimeout(function () {
            msg.style.opacity = '0';
            setTimeout(function () {
                msg.remove();
            }, 500); // بعد از محو شدن کامل حذف میشه
        }, 5000);
    });
});
function dismissMessage(el) {
    el.style.opacity = '0';
    setTimeout(() => el.remove(), 500);
}
