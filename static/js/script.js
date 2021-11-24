let container = document.querySelector("#form-container")
const addButton = document.querySelector("#add-form")

addButton.addEventListener('click', addForm)

function addForm(e) {
    if (e) {
        e.preventDefault();
    }
    console.log('add button clicked')
    const currentForms = document.getElementsByClassName('formset-row')
    const currentFormCount = currentForms.length
    const copyEmptyForm = document.getElementById("empty-form").cloneNode(true)
    copyEmptyForm.setAttribute('class', 'formset-row')
    copyEmptyForm.setAttribute('id', `form-${currentFormCount}`)
    const regex = new RegExp('__prefix__', 'g')
    copyEmptyForm.innerHTML = copyEmptyForm.innerHTML.replace(regex, currentFormCount)
    totalNewForms.setAttribute('value', currentFormCount + 1 + '')
    container.insertBefore(copyEmptyForm, addButton)
}

// container.addEventListener("click", function (event) {
//     if (event.target.classList.contains("delete-image-form")) {
//         // const currentForms = document.getElementsByClassName('personalDetail-name')
//         // let currentFormCount = currentForms.length //+ 1
//         event.preventDefault();
//         // event.target.parentElement.remove();
//         // currentFormCount--;
//         // updateForms();
//         // totalNewForms.setAttribute('value', `${currentFormCount + 1}`);
//         console.log(event)
//     }
// });


container.addEventListener("click", deleteForm)

function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}

function deleteForm(event) {
    if (event.target.classList.contains("delete-image-form")) {
        if (event) {
            event.preventDefault();
        }
        console.log('delete button clicked')
        prefix = 'educationdetails_set'
        const currentForms = document.getElementsByClassName('formset-row')
        let total = currentForms.length //+ 1
        event.target.parentElement.parentElement.parentElement.remove();
        // var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
        if (total > 1) {
            // btn.closest('.formset-row').remove();
            var forms = $('.formset-row');
            $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
            for (var i = 0, formCount = forms.length; i < formCount; i++) {
                $(forms.get(i)).find(':input').each(function () {
                    updateElementIndex(this, prefix, i);
                });
            }
        }
    }
}

// function updateForms() {
//     let count = 0;
//     for (let form of container) {
//         console.log(form.classList)
//         const formRegex = RegExp(`form-(\\d){1}-`, 'g');
//         form.innerHTML = form.innerHTML.replace(formRegex, `form-${count++}-`)
//     }
// }
//
// function deleteForm(event)
// {
//     if (event.target.classList.contains("delete-image-form")) {
//         const currentForms = document.getElementsByClassName('personalDetail-name')
//         let currentFormCount = currentForms.length //+ 1
//         console.log(currentFormCount)
//         event.preventDefault();
//         event.target.parentElement.parentElement.remove();
//         currentFormCount--;
//         updateForms();
//         totalNewForms.setAttribute('value', `${currentFormCount}`);
//     }
// }


