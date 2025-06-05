
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




// ----------------------------------------------------------------------
// comment
function showCreateCommentForm(ServiceId, commentId, commentingUser, slug) {
    $.ajax({
        type: "GET",
        url: "/csf/create_comment/" + slug,
        data: {
            ServiceId: ServiceId,
            commentId: commentId,
            commentingUser : commentingUser,
        },
        success: function(res) {
            $("#btn_" + commentId).hide(); // دکمه پاسخ مخفی بشه

            // نمایش فرم همراه با ضربدر
            $("#comment_form_" + commentId).html(`
                <div style="position: relative;">
                    <button onclick="hideCommentForm(${commentId})" class="close-button">×</button>
                    ${res}
                </div>
            `);
            

            console.log("FORM LOADED:", res);
        }
    });
}



function hideCommentForm(commentId) {
    $("#comment_form_" + commentId).html("");     // پاک کردن فرم
    $("#btn_" + commentId).show();                // دکمه "پاسخ" دوباره نمایش داده بشه
}

// --------------------------------------------------------------------------------------

