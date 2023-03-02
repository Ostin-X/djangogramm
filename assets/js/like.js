$('.likin').click(function () {
    const token = $('.likin').data('token')

    $.ajax({
        type: "POST",
        data: {
            'operation': 'like_submit',
            'csrfmiddlewaretoken': token
        },
        dataType: "json",
        success: function (response) {
            selector = $('.likin');
            if (response.liked == true) {
                $('.likin span').text(response.total_likes)
                $(selector).removeClass('btn-secondary')
                $(selector).addClass('btn-primary')
            } else {
                $('.likin span').text(response.total_likes)
                $(selector).removeClass('btn-primary')
                $(selector).addClass('btn-secondary')
            }
        }
    });
})