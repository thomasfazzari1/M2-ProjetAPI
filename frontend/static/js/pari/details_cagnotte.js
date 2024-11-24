const montantInput = document.getElementById('montant');

montantInput.addEventListener('input', () => {
    let value = montantInput.value;

    value = value.replace(/[^0-9.]/g, '');

    const parts = value.split('.');
    if (parts.length > 2) {
        value = parts[0] + '.' + parts[1];
    }

    montantInput.value = value;
});

montantInput.addEventListener('blur', () => {
    let value = parseFloat(montantInput.value);

    if (!isNaN(value)) {
        if (value < 10) {
            montantInput.value = "10.00";
        } else if (value > 5000) {
            montantInput.value = "5000.00";
        } else {
            montantInput.value = value.toFixed(2);
        }
    } else {
        montantInput.value = '';
    }
});

document.querySelector('form').addEventListener('submit', (e) => {
    const value = parseFloat(montantInput.value);

    if (isNaN(value) || value < 10 || value > 5000) {
        alert('Le montant doit être un nombre compris entre 10.00 et 5000.00.');
        e.preventDefault();
    }
});
