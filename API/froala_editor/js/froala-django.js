function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

if (typeof django !== 'undefined') {
    (function ($) {
        $(document).on('formset:added', function (event, $row, formsetName) {
            $row.find('textarea').each(function () {
                $(this).prev().remove();

                jQuery(this).froalaEditor({
                    imageUploadURL: '/upload_image',
                    imageUploadParams: {
                        id: 'my_editor'
                    },
                })

            });
        });
    })(django.jQuery);
}


