const montantInput = document.getElementById('montant');

    montantInput.addEventListener('input', (e) => {
        let value = montantInput.value;

        value = value.replace(/[^0-9.]/g, '');

        const parts = value.split('.');
        if (parts.length > 2) {
            value = parts[0] + '.' + parts[1];
        }

        if (value !== '') {
            const numericValue = parseFloat(value);
            if (numericValue < 10) {
                value = '10';
            } else if (numericValue > 5000) {
                value = '5000';
            }
        }

        montantInput.value = value;
    });

    document.querySelector('form').addEventListener('submit', (e) => {
        const value = parseFloat(montantInput.value || '0');
        if (isNaN(value) || value < 10 || value > 5000) {
            alert('Le montant doit être compris entre 10 et 5000.');
            e.preventDefault();
        }
    });