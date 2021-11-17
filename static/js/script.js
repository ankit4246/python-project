let container = document.querySelector("#form-container")
const addButton = document.querySelector("#add-form")

addButton.addEventListener('click', addForm)

function addForm(e) {
    if (e) {
        e.preventDefault();
    }
    const currentForms = document.getElementsByClassName('personalDetail-name')
    const currentFormCount = currentForms.length //+ 1
    const copyEmptyForm = document.getElementById("empty-form").cloneNode(true)
    copyEmptyForm.setAttribute('class', 'personalDetail-name')
    copyEmptyForm.setAttribute('id', `form-${currentFormCount}`)
    const regex = new RegExp('__prefix__', 'g')
    copyEmptyForm.innerHTML = copyEmptyForm.innerHTML.replace(regex, currentFormCount)
    totalNewForms.setAttribute('value', currentFormCount + 1 + '')
    container.insertBefore(copyEmptyForm, addButton)
}

// container.addEventListener("click", function (event) {
//     if (event.target.classList.contains("delete-image-form")) {
//         const currentForms = document.getElementsByClassName('personalDetail-name')
//         let currentFormCount = currentForms.length //+ 1
//         event.preventDefault();
//         event.target.parentElement.remove();
//         currentFormCount--;
//         updateForms();
//         totalNewForms.setAttribute('value', `${currentFormCount + 1}`);
//     }
// });
//
// function updateForms() {
//     let count = 0;
//     for (let form of container) {
//         const formRegex = RegExp(`form-(\\d){1}-`, 'g');
//         form.innerHTML = form.innerHTML.replace(formRegex, `form-${count++}-`)
//     }
// }