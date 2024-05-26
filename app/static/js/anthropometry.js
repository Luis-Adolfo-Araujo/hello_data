function restrictAlturaInput(event) {
    const input = event.target;
    let value = input.value.replace(/[^0-9]/g, '').replace(',', '');

    if (value.length > 3) {
        value = value.slice(0, 3);
    }

    if (value.length > 1) {
        value = value.slice(0, 1) + ',' + value.slice(1);
    }

    input.value = value;
}

function restrictThreeCharsInput(event) {
    const input = event.target;
    let value = input.value.replace(/[^0-9]/g, '');

    if (value.length > 3) {
        value = value.slice(0, 3);
    }

    input.value = value;
}