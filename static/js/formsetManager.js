(function ($, window) {
    /**
     * Formset Manager Libs By Jaime Negrete
     */

    $.fn.formsetManager = function () {
        let $owner = this;
        return this.each(function () {
            let item_id = $($owner).attr('id');
            let id = 'add_' + item_id;
            $($owner).append(
                "<span id='" + id + "' style='float: right'><i class='hvr-buzz-out fa fa-plus-square fa-2x'></i></span><br />"
            );
            // Handle Click Event
            $('span#' + id).click(function () {
                add_one_more(item_id);
            });
        });
    }

    function add_one_more(prefix) {
        let parent_div = $('div#' + prefix);
        let total_forms_selector = "input[name='" + prefix + "-TOTAL_FORMS']";
        let prev_value = parseInt(parent_div.children(total_forms_selector).val());
        let new_text = prefix + '-' + prev_value.toString();
        let prev_text_regex = new RegExp(prefix + '-\\d+', 'g');
        let last_normal_form_reference = parent_div.children('div.last_form');  // Get last formset load normally
        let new_id = last_normal_form_reference.attr('id').replace(prev_text_regex, new_text);  // Make new id

        $("<br id='br_" + new_id + "'/><div id='" + new_id + "' class='form_insert'></div>").insertAfter(parent_div.children('div').last());
        // Update total forms
        parent_div.children(total_forms_selector).val(prev_value + 1);
        let new_element = parent_div.children('div#' + new_id);
        // Create del buttom
        let del_id = 'del_' + new_id;
        new_element.append("<button class='btn btn-xs btn-danger' style='float: right' id='" + del_id + "'>Borrar</button>");
        $('button#' + del_id).click(function () {
            $('div#' + new_id).remove();
            $('br#br_' + new_id).remove();
            clean_formset(prefix);
        });
        // End create del buttom
        // Fill new element (inputs, labels)
        last_normal_form_reference.children().each(function () {
            let element = $(this).prop('outerHTML');
            let element_new = element.replace(prev_text_regex, new_text); // Asign new identity
            let element_without_values = element_new.replace(new RegExp("value=\"(\\w|_)+\"", 'g'), "value=\"\"");  // Clean values
            new_element.append(element_without_values.replace(new RegExp(">(\\w|_)+</textarea>", 'g'), "</textarea>")); // clean textarea
        });
    }

    function clean_formset(prefix) {
        let parent = $('div#' + prefix);
        $("input[name='" + prefix + "-TOTAL_FORMS']").val($(parent).children('div').length);  // Update total forms
    }
})(jQuery, window);
