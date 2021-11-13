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
            totalNewForms.setAttribute('value', currentFormCount+1+'')
            container.insertBefore(copyEmptyForm, addButton)
        }