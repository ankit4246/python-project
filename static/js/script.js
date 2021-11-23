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

function updateForms() {
    let count = 0;
    // console.log('before')
    for (let form of container) {
        // console.log(form)
        const formRegex = RegExp(`form-(\\d){1}-`, 'g');
        console.log(formRegex)
        form.innerHTML = form.innerHTML.replace(formRegex, `form-${count++}-`)
        // console.log(form.innerHTML)
    }
}

container.addEventListener("click", deleteForm) 

function deleteForm(event) 
{
    if (event.target.classList.contains("delete-image-form")) {
        const currentForms = document.getElementsByClassName('personalDetail-name')
        let currentFormCount = currentForms.length //+ 1
        event.preventDefault();
        event.target.parentElement.parentElement.remove();
        // console.log(currentFormCount)
        currentFormCount--;
        updateForms();
        totalNewForms.setAttribute('value', `${currentFormCount + 1}`);
        // console.log(event)
        // console.log(event.target.parentElement.parentElement.remove())
    }
}

// const delete_form = document.getElementByClassName('delete-image-form')
// delete_form.addEventListener("click", someFunction)
// function someFunction(event) {
//     event.preventDefault();
//     console.log('clicked')
// }


