

$('.likin').click(function () {
    const token = $('.likin').data('token')

    $.ajax({
        type: "POST",
        data: {
            'operation': 'like',
            'csrfmiddlewaretoken': token
        },
        dataType: "json",
        success: function (response) {
            selector = $('.likin');
            if (response.liked === true) {
                $('.likin span').text(response.total_likes)
                $(selector).removeClass('btn-secondary').addClass('btn-primary')
            } else {
                $('.likin span').text(response.total_likes)
                $(selector).removeClass('btn-primary').addClass('btn-secondary')
            }
        }
    });
})
