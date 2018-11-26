/* Some utils require jQuery */

function load_modal(title, level, link, modal_id){
    if (!modal_id) modal_id = '#base_modal';
    const levels = {
        success: 'modal fade modal-success',
        warning: 'modal fade modal-warning',
        danger: 'modal fade modal-danger',
    };

    if (!levels[level]) level = "success";

    const modal = $(modal_id);
    modal.find('.modal-title').html(title);
    modal.removeClass();
    modal.addClass(levels[level]);
    modal.modal('show').find('.modal-body').load(link);
}

// Ajax configuration from https://docs.djangoproject.com/en/2.1/ref/csrf/
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});