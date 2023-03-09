const $statusButton = $('[button_status]')
$statusButton.click(function () {
    const currentButtonStatus = $(this).attr('button_status')
    const token = $statusButton.data('token')
    let newButtonStatus = currentButtonStatus === 'inactive' ? 'activate' : 'inactivate'

    $.ajax({
        type: "POST",
        data: {
            'operation': newButtonStatus,
            'csrfmiddlewaretoken': token
        },
        dataType: "json",
        success: function (response) {
            newButtonStatus = response.button_status
            $statusButton.attr('button_status', newButtonStatus)
            $statusButton.toggleClass('btn-primary').toggleClass('btn-secondary')
            $('[button_status] span').text(response.button_value)
        }
    });
})
