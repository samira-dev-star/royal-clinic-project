
// Mobile sidebar toggle
const sidebarToggle = document.getElementById('sidebarToggle');
const mobileSidebar = document.getElementById('mobileSidebar');
const closeSidebar = document.getElementById('closeSidebar');

sidebarToggle.addEventListener('click', () => {
    mobileSidebar.classList.toggle('translate-x-full');
});

closeSidebar.addEventListener('click', () => {
    mobileSidebar.classList.add('translate-x-full');
});

// Back to top button
const backToTopButton = document.querySelector('.back-to-top');

window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
        backToTopButton.classList.remove('hidden');
    } else {
        backToTopButton.classList.add('hidden');
    }
});

backToTopButton.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

// --------------------------------------------------

    window.$crisp = [];
    window.CRISP_WEBSITE_ID = "5d6dc27b-5aa5-4012-b153-84b03621eb93";

    (function () {
        var d = document;
        var s = d.createElement("script");
        s.src = "https://client.crisp.chat/l.js";
        s.async = 1;
        s.onload = function () {
            console.log("Crisp Loaded ✅");
            // فعال کردن دکمه بعد از لود کامل
            const chatBtn = document.getElementById("crisp-chat-btn");
            if (chatBtn) {
                chatBtn.addEventListener("click", function () {
                    $crisp.push(["do", "chat:open"]);
                });
            }
        };
        d.getElementsByTagName("head")[0].appendChild(s);
    })();

