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

function make_consult(id) {

    $.ajax({
        method: "POST",
        url: "/consult/",
        data: {
            'patiend_id': id,
            'csrfmiddlewaretoken': getCookie('csrftoken')
        },
        success: (resp) => {
            console.log(resp)
        },
        error: (error) => {
            console.log(error)
        }
    })
}

function assing_consult(id) {

    $.ajax({
        method: "POST",
        url: "/assign_consult/",
        data: {
            'consult_id': id,
            'csrfmiddlewaretoken': getCookie('csrftoken')
        },
        success: (resp) => {
            console.log(resp)
            $('#exampleModal').modal('hide')
        },
        error: (error) => {
            console.log(error)
            $('#exampleModal').modal('hide')
        }
    })
}

function finish_consult(id) {

    $.ajax({
        method: "POST",
        url: "/end_consult/",
        data: {
            'consult_id': id,
            'csrfmiddlewaretoken': getCookie('csrftoken')
        },
        success: (resp) => {
            console.log(resp)
            $('#exampleModal').modal('hide')
        },
        error: (error) => {
            console.log(error)
            $('#exampleModal').modal('hide')
        }
    })
}

