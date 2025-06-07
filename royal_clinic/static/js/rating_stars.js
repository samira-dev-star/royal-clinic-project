$(document).ready(function () {
    let selectedRating = 0;

    $('.star').on('mouseover', function () {
        const value = $(this).data('value');
        $('.star').each(function () {
            $(this).toggleClass('hovered', $(this).data('value') <= value);
        });
    });

    $('.star').on('mouseout', function () {
        $('.star').removeClass('hovered');
    });

    $('.star').on('click', function () {
        selectedRating = $(this).data('value');
        $('#rating-value').val(selectedRating);
        $('.star').each(function () {
            $(this).toggleClass('selected', $(this).data('value') <= selectedRating);
        });
    });

    $('#rating-form').on('submit', function (e) {
        e.preventDefault();

        const score = $('#rating-value').val();
        const idea = $('#idea-text').val();
        const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        const serviceId = $('#service-id').val();

        if (!score || score < 1 || score > 5) {
            $('#confirm-box').text('لطفا یک امتیاز معتبر انتخاب کنید.');
            return;
        }

        if (!idea.trim()) {
            $('#confirm-box').text('لطفا نظر خود را وارد کنید.');
            return;
        }

        $.ajax({
            type: 'POST',
            url: addScoreURL,  // 👈 اینجا با متغیر global که تو template تعریف شده جایگزین شد
            data: {
                'score': score,
                'idea': idea,
                'service_id': serviceId,
                'csrfmiddlewaretoken': csrfToken,
            },
            success: function (response) {
                if (response.success) {
                    $('#confirm-box').text('✅ امتیاز شما با موفقیت ثبت شد!');
                    $('#avg_score').text(response.avg_score || "—");
                    $('#rating-form')[0].reset();
                    $('.star').removeClass('selected');
                    selectedRating = 0;
                }
            },
            error: function (xhr) {
                let msg = '❌ خطایی در ثبت امتیاز رخ داد.';
                if (xhr.responseJSON && xhr.responseJSON.message) {
                    msg = xhr.responseJSON.message;
                }
                $('#confirm-box').text(msg);
            }
        });
    });
});
