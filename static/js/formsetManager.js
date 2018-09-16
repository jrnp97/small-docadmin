(function ($, window) {
    /**
     * Formset Manager Libs By Jaime Negrete
     */

    $.fn.formsetManager = function () {
        let owner = this;
        return this.each(function () {
            let formset_prefix = $(owner).attr('id');
            let span_add = $("<span id='add_'" + formset_prefix + "' style='float: right'><i class='hvr-buzz-out fa fa-plus-square fa-2x'></i></span>");
            $(owner).append(span_add);
            span_add.on('click', function () { add_one_more(owner, formset_prefix); });
        });
    };

    function add_one_more(parent_div, formset_prefix) {
        let total_forms_selector = "input[name='" + formset_prefix + "-TOTAL_FORMS']";
        let prev_value = parseInt(parent_div.children(total_forms_selector).val());
        let new_formset_text = formset_prefix.concat('-',prev_value);
        let last_formset_text_regex = new RegExp(formset_prefix + '-\\d+', 'g');
        let last_formset_form = parent_div.children('div.last_form');
        let new_formset_id = last_formset_form.attr('id').replace(last_formset_text_regex, new_formset_text);
        let separator = $("<hr class='divider'>");
        let div_formset  = $("<div id='" + new_formset_id + "' class='row form_insert'></div>");

        div_formset.insertAfter(parent_div.children('div').last());
        separator.insertBefore(div_formset);
        parent_div.children(total_forms_selector).val(prev_value + 1); // Update total forms
        // Create del button
        let del_btn = $("<button class='btn btn-xs btn-danger' style='float: right' id=del_'" + new_formset_id + "'>Borrar</button>");
        div_formset.append(del_btn);

        del_btn.on('click', function () {
            separator.remove();
            div_formset.remove();
            $(total_forms_selector).val(parent_div.children('div').length);
        });
        // End create del button

        // Fill new element (inputs, labels)
        last_formset_form.children().each(function () {
            let element_new = $(this).prop('outerHTML').replace(last_formset_text_regex, new_formset_text);
            div_formset.append(clean_element(element_new));
        });
    }

    function clean_element(element){
        let without_values = element.replace(new RegExp("value=\"(\\w|_)+\"", 'g'), "");
        return without_values.replace(new RegExp(">(\\w|_)+</textarea>", 'g'), "</textarea>");  // clean <textarea>
    }
})(jQuery, window);
