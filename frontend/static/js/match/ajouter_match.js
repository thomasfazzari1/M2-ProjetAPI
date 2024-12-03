document.addEventListener("DOMContentLoaded", function () {
    const coteFields = document.querySelectorAll("#valeur_cote_domicile, #valeur_cote_exterieure, #valeur_cote_match_nul");

    // Valeurs négatives côtes
    coteFields.forEach(field => {
        field.addEventListener("input", function () {
            const value = parseFloat(this.value);
            if (value < 0) {
                this.value = Math.abs(value).toFixed(2);
            } else if (isNaN(value)) {
                this.value = "";
            }
        });
    });

    // Filtrage dynamique du formulaire en fonction du sport
    const sportSelect = document.getElementById("id_sport");
    const evenementSelect = document.getElementById("id_evenement");
    const eqDomicileSelect = document.getElementById("id_eq_domicile");
    const eqExterieureSelect = document.getElementById("id_eq_exterieure");

    const filterOptions = (selectElement, sportId) => {
        Array.from(selectElement.options).forEach(option => {
            const optionSportId = option.getAttribute("data-sport-id");
            const shouldShow = optionSportId === sportId || option.value === "";
            option.style.display = shouldShow ? "" : "none";
        });
        selectElement.value = "";
    };

    if (sportSelect) {
        sportSelect.addEventListener("change", function () {
            const selectedSportId = this.value;

            filterOptions(evenementSelect, selectedSportId);
            filterOptions(eqDomicileSelect, selectedSportId);
            filterOptions(eqExterieureSelect, selectedSportId);
        });

        sportSelect.dispatchEvent(new Event("change"));
    }

    // Même équipe en domicile / extérieur
    const handleTeamSelection = () => {
        const selectedDomicile = eqDomicileSelect.value;
        const selectedExterieure = eqExterieureSelect.value;

        Array.from(eqExterieureSelect.options).forEach(option => {
            option.disabled = option.value === selectedDomicile && option.value !== "";
        });

        Array.from(eqDomicileSelect.options).forEach(option => {
            option.disabled = option.value === selectedExterieure && option.value !== "";
        });
    };

    if (eqDomicileSelect && eqExterieureSelect) {
        eqDomicileSelect.addEventListener("change", handleTeamSelection);
        eqExterieureSelect.addEventListener("change", handleTeamSelection);
    }

    // Date passée
    const dateField = document.getElementById("date");
    if (dateField) {
        const today = new Date().toISOString().split("T")[0];
        dateField.setAttribute("min", today);

        dateField.addEventListener("input", function () {
            if (this.value < today) {
                this.value = "";
                alert("Vous ne pouvez pas sélectionner une date déjà passée.");
            }
        });
    }

    // Filtrage des matchs existants
    document.getElementById('sport_filtre').addEventListener('change', function () {
        const selectedSportId = this.value;
        console.log("Sport sélectionné :", selectedSportId);

        const rows = document.querySelectorAll('tbody tr');
        rows.forEach(row => {
            console.log("ID du sport de la ligne :", row.dataset.sportId);
            if (selectedSportId === 'all' || row.dataset.sportId === selectedSportId) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });
});
