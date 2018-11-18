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