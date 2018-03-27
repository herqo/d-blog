$(document).ready(function () {
    $('#visible_form').submit(function (e) {
        e.preventDefault();
        var _this_ = $(this);
        var visible_url = _this_.attr('action');

        $.ajax({
            url: visible_url,
            type: 'json',
            data: _this_.serialize(),
            method:"POST",
            success:function (data) {
                console.log(data)
            }
        });

    })
});