function addFormset(formset, prefix) {
    // Get the formset and create a new formset
    const element = $(formset);
    const newElement = element.clone(true);

    // Add the new formset to the end
    // element.after(newElement);
    newElement.insertAfter(element);

    // Update the indices
    element.parent().children('tr').each((i, item) => {
        updateIndex(item, prefix, i);
    });

    // Update the total number of forms
    updateTotal(element, prefix, true);
}

function deleteFormset(button, prefix) {
    // Get button in the row to delete
    const deleteElementButton = $(button),
        parent = deleteElementButton.closest('tbody');

    // Remove row find the parent row and delete that
    deleteElementButton.closest('tr').remove();

    // Update the indices
    parent.children('tr').each((i, item) => {
        updateIndex(item, prefix, i)
    });

    // Update the total number of forms
    updateTotal(parent, prefix, false);
}

function updateTotal(element, prefix, addIndex) {
    // Get the Total Form Input
    const subIdx = Number(element.closest('table').attr('id').split('_').pop()),
        totalFormsInput = $('#id_' + prefix + '_' + subIdx + '-TOTAL_FORMS');
    let total = totalFormsInput.val();
    if (addIndex) {
        total++;
    } else {
        total--;
    }

    // Disable delete when there is only one form left
    // Enable when there is more than one
    if (total === 1) {
        $(element).children('tr').find('.delete-me-button').first().attr('disabled', true)
    } else {
        $(element).parent('tbody').children('tr').each((i, index) => {
            $(index).find('.delete-me-button').each((I, Index) => {
                // Don't enable sub-form buttons when there's not more than 1
                if ($(Index).closest('tbody').children('tr').length > 1) $(Index).attr('disabled', false)
            });
        });
    }
    totalFormsInput.val(total);
}

function updateIndex(element, prefix, index) {
    // Define pattern to replace and the replacement
    // regex, replacement match the Parent formset
    // parentIndex is the index of the Parent Formset
    // subRegex, subReplacement match the sub-formset
    // subTotalRegex, subTotalReplacement match the sub-formset Management forms
    const regex = new RegExp(prefix + '_0-\\d+'),
        replacement = prefix + '_0-' + index,
        parentIndex = $(element).closest('table').attr('id').split('_').pop(),
        subRegex = new RegExp(prefix + '_\\d+' + '-\\d+'),
        subReplacement = prefix + '_' + parentIndex + '-' + index,
        subTotalRegex = new RegExp('sample_form_\\d+'),
        subTotalReplacement ='sample_form_' + index;

    // Update sub-formset specific indices
    // Sub-formset total input
    if ($(element).find('#id_fs_sample_form_' + parentIndex + '-TOTAL_FORMS').attr('name')) {
        $(element).find('#id_fs_sample_form_' + parentIndex + '-TOTAL_FORMS')
            .attr('name',
                $(element).find('#id_fs_sample_form_' + parentIndex + '-TOTAL_FORMS')
                    .attr('name').replace(subTotalRegex, subTotalReplacement));
    }
    if ($(element).find('#id_fs_sample_form_' + parentIndex + '-TOTAL_FORMS').attr('id')) {
        $(element).find('#id_fs_sample_form_' + parentIndex + '-TOTAL_FORMS')
            .attr('id',
                $(element).find('#id_fs_sample_form_' + parentIndex + '-TOTAL_FORMS')
                    .attr('id').replace(subTotalRegex, subTotalReplacement));
    }

    // Sub-formset add button
    $(element).find('.sub-form-add-more').attr('data-index', index);
    // Sub-formset table -- where the sub-formset lives
    $(element).find('table.sub-formset').attr('id', 'sample_form_' + index);

    // Replace the indices
    // Vital to make sure none of these elements have repeating names,
    // otherwise the inputs will be removed when formsets are added or deleted

    // Replace different RegEx based on parent or sub-formset
    if (prefix === 'fs_sample_form') {
        replaceIndex(element, subRegex, subReplacement)
    } else{
        // regexSub, replacementSub specifically match the sub-formset
        const regexSub = new RegExp('sample_form_\\d+'),
        replacementSub = 'sample_form_' + index;
        // Replace indices in the parent
        replaceIndex(element, regex, replacement);
        // Replace indices in the sub-formset
        replaceIndex(element, regexSub, replacementSub)
    }
}

function replaceIndex(element, regex, replacement) {
    // Replace indices in the name, id and for attributes in div, select, input, textarea and label
    $(element).find('div,select,input,textarea,label').each((i, item) => {
        if ($(item).attr('name')) $(item).attr('name', $(item).attr('name').replace(regex, replacement));
        if ($(item).attr('id')) $(item).attr('id', $(item).attr('id').replace(regex, replacement));
        if ($(item).attr('for')) $(item).attr('for', $(item).attr('for').replace(regex, replacement));
    });
}