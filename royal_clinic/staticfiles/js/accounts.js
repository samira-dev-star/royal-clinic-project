
// تیک خوردن دکمه ی تایید قوانین و ارجاع مجدد به صفحه ی ثبت نام
function handleAcceptRules() {
    const checkbox = document.getElementById('rule');
    if (checkbox.checked) {
        window.location.href = '/accounts/register/?accept=1';
    }
}


window.addEventListener('DOMContentLoaded', function () {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('accept') === '1') {
        const checkbox = document.getElementById('terms');
        if (checkbox) {
            checkbox.checked = true;
        }
    }
});
// -------------------------------------------------------------------
