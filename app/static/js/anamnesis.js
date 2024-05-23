function handleFormSubmission(event) {
    event.preventDefault();
    const formData = new FormData(document.getElementById('anamneseForm'));
    const formValues = {};
    formData.forEach((value, key) => {
        formValues[key] = value;
    });
    showNextFields(formValues);
}

function showNextFields(data) {
    // Perform operations with the collected form data
    // For example, console.log(data) to see the collected values
    console.log("Form Data: ", data);
    // Further logic to handle the next steps
}

// passar uma lista com os valores desse form para a função `showNextFields()` dentro de um dict {"info": info_pac}
// no showNextFields() pegar os valores de metabolico e adicionar no dict {"info": info_pac, "metabolico": metabolico}
// entao retornar para uma rota e fazer a inserção no banco